#!/projects/shart/digital_pathology/scripts/tensorflow_2/bin/python
__author__ = "Naresh Prodduturi"
__email__ = "prodduturi.naresh@mayo.edu"
__status__ = "Dev"

import os
import argparse
import sys
import pwd
import time
import subprocess
import re
import shutil
import openslide
import numpy as np
from PIL import Image, ImageDraw
import io
import glob	
import logging
from  skimage.color  import *
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu



class TissueDetector:


	def __init__(self, logger, input_file, output_file, method, param):
		self.logger = logger
		self.input_file = input_file
		self.output_file = output_file
		self.method = method
		self.params = None
		if param is not None: 
			self.params = param.split(',')
		self.list_methods=['gray','otsu','grey','rgb2lab','rgb2hed']# other methods: 'rgb2hsv','rgb2luv','rgb2rgbcie','rgb2xyz','rgb2ycbcr','rgb2ydbdr','rgb2yiq','rgb2ypbpr','rgb2yuv','gnb_model'
		self.rescale_factor = 100

		method_index = -1
		'''checking the params before calling method'''
		if not method in self.list_methods:
			raise Exception("Specified method cannot be handled by this scrip")
		else:
			method_index = self.list_methods.index(method)

		if self.method == 'gray' and len(self.params) != 1:
			raise Exception("Specified method cannot be handled by this scrip")


	'''Get thumbnail'''
	def get_thumbnail(self):
		'''opening openslide'''
		OSobj = openslide.OpenSlide(self.input_file)
		width,height = OSobj.dimensions
		rescale_factor = self.rescale_factor
		width=int(width/rescale_factor)
		height=int(height/rescale_factor)
		size=(width,height)

		'''getting thumbmnail image with specified width and height'''
		img=OSobj.get_thumbnail(size)

		return img

	'''QC function to plot original and mask image'''
	def qc_gen(self, img, mask):

		outputfile = self.output_file

		'''Qc code for testing method:Original'''
		img.save(outputfile+'.original.png', "png")

		'''Qc code for testing method:mask'''
		'''Convert the image into numpy array'''
		np_img = np.array(img)
		np_mask = np.array(mask)

		np_mask_idx = np.where(np_mask == 0)
		np_img[np_mask_idx] = (0, 0, 0)
		mask_img = Image.fromarray(np_img)
		mask_img.save(outputfile + '.mask_img.png', "png")




	'''histogram to plot distributions'''
	def create_hist(self, img):
		output_file = self.output_file
		'''coverting the thunbnail image to RGB'''
		img = img.convert('RGB')
		grey_img = img.convert('L')
		np_grey = np.array(grey_img)
		list_grey= np_grey.tolist()

		with PdfPages(output_file+'.hist.pdf') as pdf:
			plt.figure(figsize=(3, 3))
			plt.plot(range(len(list_grey)),list_grey, 'r-o')
			plt.title('Grey Scale')
			pdf.savefig()  # saves the current figure into a pdf page
			plt.close()


	'''grey function'''
	def call_gray(self, img):

		params = self.params

		'''Change to grey scale'''
		grey_img = img.convert('L')
		thres_hold=int(params[0])

		if len(params) != 1:
			raise Exception("Specified method need atleast one param")
			
		'''Convert the image into numpy array'''
		np_grey = np.array(grey_img)

		'''creating mask'''
		np_mask=np.zeros((np_grey.shape[0], np_grey.shape[1]), dtype='int8')
		#np_mask = np.where(((np_grey < thres_hold) & (np_grey > 100)), 1, np_mask)
		np_mask = np.where((np_grey < thres_hold) , 1, np_mask)

		mask_img = Image.fromarray(np_mask)
		return mask_img

	'''otsu function'''
	def call_otsu(self, img):

		'''Change to grey scale'''
		grey_img = img.convert('L')
		
		'''Convert the image into numpy array'''
		np_grey = np.array(grey_img)
		
		thres_hold = threshold_otsu(np_grey)
		
		
		'''creating mask'''
		np_mask=np.zeros((np_grey.shape[0], np_grey.shape[1]), dtype='int8')
		np_mask = np.where((np_grey < thres_hold) , 1, np_mask)

		mask_img = Image.fromarray(np_mask)
		return mask_img
		
	''' call method(lab)'''
	def call_scikit_rgb2lab(self, img):
		params = self.params		
		method = self.method
		if len(params) != 1:
			raise Exception("Specified method need atleast one param")
		thres_hold=float(params[0])

		'''Convert the image into numpy array'''
		np_img = np.array(img)

		'''transform to requested method value(lab)'''
		metd = eval(method)
		np_trans_img = metd(np_img)
		np_trans_img_l = np_trans_img[:,:,0]

		'''creating mask'''
		np_mask=np.zeros((np_img.shape[0], np_img.shape[1]), dtype='int8')
		np_mask = np.where((np_trans_img_l < thres_hold) , 1, np_mask)
		mask_img = Image.fromarray(np_mask)
		return mask_img

	''' call method(hed)'''
	def call_scikit_rgb2hed(self, img):
		params = self.params		
		method = self.method
		if len(params) != 1:
			raise Exception("Specified method need atleast one param")
		thres_hold=float(params[0])

		'''Convert the image into numpy array'''
		np_img = np.array(img)

		'''transform to requested method value(lab)'''
		metd = eval(method)
		np_trans_img = metd(np_img)
		np_trans_img_l = np_trans_img[:,:,2]
       
		'''creating mask'''
		np_mask=np.zeros((np_img.shape[0], np_img.shape[1]), dtype='int8')
		np_mask = np.where((np_trans_img_l > thres_hold) , 1, np_mask)
		mask_img = Image.fromarray(np_mask)
		return mask_img
		
	'''function to call appropriate method'''
	def create_mask(self, img):
		method =self.method
		if self.params is not None:
			params = self.params
		logger = self.logger

		'''coverting the thunbnail image to RGB'''
		img = img.convert('RGB')

		'''Calling the appropriate method with params'''
		if method == 'gray' or method == 'grey':
			mask = self.call_gray(img)
		elif  method.startswith('rgb2lab'):
			mask = self.call_scikit_rgb2lab(img)
		elif  method.startswith('rgb2hed'):
			mask = self.call_scikit_rgb2hed(img)
		elif  method == 'otsu':
			mask = self.call_otsu(img)
		else:
			raise Exception("No matching method")

		return mask


	'''function to calculate tissue area'''
	def calc_tissue_area(self, mask):

		'''Convert the image into numpy array'''
		np_mask = np.array(mask)
		'''Calculate tissue are'''		
		binary_mask_tissue_area = round(100*(np.sum(np_mask)/(np_mask.size)),2)
		return str(binary_mask_tissue_area)

	'''write mask to the file'''
	def write_mask(self, img, mask):

		output_file = self.output_file


		'''Qc code for testing method:mask'''
		'''Convert the image into numpy array'''
		np_img = np.array(img)
		np_mask = np.array(mask)

		np_img[np_mask == 0] = [0, 0, 0]
		np_img[np_mask == 1] = [255, 255, 255]
		mask_img = Image.fromarray(np_img)
		if output_file.endswith('.png'):
			mask_img.save(output_file, "png")
		elif output_file.endswith('.jpeg') or output_file.endswith('.jpeg'):
			mask_img.save(output_file, "JPEG")
		elif output_file.endswith('.tiff') or output_file.endswith('.tif'):
			mask_img.save(output_file, format="TIFF")
		else:
			raise Exception("Cannot support this format")
