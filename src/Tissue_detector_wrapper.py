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
from utils import *


'''Create thumnail and mask'''
'''function to check if input files exists and valid''' 	
def input_file_validity(file):
	'''Validates the input files'''
	if os.path.exists(file)==False:
		raise argparse.ArgumentTypeError( '\nERROR:Path:\n'+file+':Does not exist')
	if os.path.isfile(file)==False:
		raise argparse.ArgumentTypeError( '\nERROR:File expected:\n'+file+':is not a file')
	if os.access(file,os.R_OK)==False:
		raise argparse.ArgumentTypeError( '\nERROR:File:\n'+file+':no read access ')
	return file


def argument_parse():
	'''Parses the command line arguments'''
	parser=argparse.ArgumentParser(description='')
	parser.add_argument("-i","--input_file",help="input file",required="True")
	parser.add_argument("-o","--output_file",help="output file name",required="True")
	parser.add_argument("-m", "--method", help="method type", required="True")
	parser.add_argument("-p", "--param", help="method param")
	return parser
	
def main():

	'''Create Looger'''
	logging.basicConfig()
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	'''reading the config filename'''
	parser=argument_parse()
	arg=parser.parse_args()

	'''printing the config param'''
	logger.info("Entered INPUT Filename "+arg.input_file)
	logger.info("Entered Output File "+arg.output_file)
	logger.info("Entered Method "+arg.method)
	if arg.param is not None :
		logger.info("Entered Method Params " + arg.param)

	input_file=arg.input_file
	output_file=arg.output_file
	method=arg.method
	param=arg.param

	tissue_detector = TissueDetector(logger,input_file, output_file, method, param)

	'''get thumbnail'''
	img = tissue_detector.get_thumbnail()


	'''Get mask'''
	mask = tissue_detector.create_mask(img)

	'''Calc tissue area'''
	tissue_area = tissue_detector.calc_tissue_area(mask)
	logger.info("% Tissue area "+tissue_area)
	
	'''Qc code for testing method:mask'''
	tissue_detector.qc_gen(img, mask)

	'''Write output to the file'''
	tissue_detector.write_mask(img, mask)


if __name__ == "__main__":
	main()
