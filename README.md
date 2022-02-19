# Tissue Detector

## Purpose: Identify the foreground tissue using various methods

## 0. How to run
```
python Tissue_detector_wrapper.py -i <Input tiff file> -o <Output Mask Image> -m <method> -p <Parameters for methods>

supported methods: 'gray','otsu','rgb2lab','rgb2hed'

'gray' : Traditional way  (Threshold value unique to each slide)
'otsu' : Scikit Image Otsu method (Dynamic Threshold)
'rgb2lab' : Scikit Image RGB2LAB (Threshold value unique to each slide)
'rgb2hed' : Scikit Image RGB2HED (Threshold value unique to each slide)
```

## 1. Examples 
```
#gray
python Tissue_detector_wrapper.py -i /projects/shart/digital_pathology/data/test/tiff/1_WT.tiff -o 1_WT.gray.mask.png -m gray -p 235

#otsu
python Tissue_detector_wrapper.py -i /projects/shart/digital_pathology/data/test/tiff/1_WT.tiff -o 1_WT.otsu.mask.png -m otsu

#rgb2lab
python Tissue_detector_wrapper.py -i /projects/shart/digital_pathology/data/test/tiff/1_WT.tiff -o 1_WT.lab.mask.png -m rgb2lab -p 80

#rgb2hed
python Tissue_detector_wrapper.py -i /projects/shart/digital_pathology/data/test/tiff/1_WT.tiff -o 1_WT.hed.mask.png -m rgb2hed -p 0.008

```

## 1. QC images
```

Thumbnail : Original
```
<img src="./images/1_WT.otsu.mask.png.original.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
	 

```

Thumbnail : hed
```
<img src="./images/1_WT.hed.mask.png.mask_img.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
	 

```

Thumbnail : lab
```
<img src="./images/1_WT.lab.mask.png.mask_img.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
	 

```

Thumbnail : otsu
```
<img src="./images/1_WT.otsu.mask.png.mask_img.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
	 

```

Thumbnail : Traditional
```
<img src="./images/1_WT.gray.mask.png.mask_img.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
	 
	 