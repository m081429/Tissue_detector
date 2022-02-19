set -x


#gray
python ./src/Tissue_detector_wrapper.py -i /projects/shart/digital_pathology/data/test/tiff/1_WT.tiff -o ./images/1_WT.gray.mask.png -m gray -p 235

#otsu
python ./src/Tissue_detector_wrapper.py -i /projects/shart/digital_pathology/data/test/tiff/1_WT.tiff -o ./images/1_WT.otsu.mask.png -m otsu

#rgb2lab
python ./src/Tissue_detector_wrapper.py -i /projects/shart/digital_pathology/data/test/tiff/1_WT.tiff -o ./images/1_WT.lab.mask.png -m rgb2lab -p 80

#rgb2hed
python ./src/Tissue_detector_wrapper.py -i /projects/shart/digital_pathology/data/test/tiff/1_WT.tiff -o ./images/1_WT.hed.mask.png -m rgb2hed -p 0.008
