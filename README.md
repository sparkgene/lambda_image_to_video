# lambda_image_to_video
This AWS Lambda function create time-plus video from images.

## Overview

This is a Lambda function for creating time-plus video from images.
Input image must stored in s3 bucket with key like "yyyy/mm/dd/sequence_id.jpg".
Output video type is mp4. The video created by lambda function is placed to bucket with key "yyyy/mm/yyyymmdd.mp4".
All image with same key "yyyy/mm/dd", are stored in same video.

### MoviePy
https://pypi.python.org/pypi/moviepy
MoviePy is a python module for video editing.
This download ffmpeg automatically on first MoviePy call.

## Installation

AWS Lambda do not have ffmpeg, so we need to include executable binary with lambda function.
```
sudo yum -y update
sudo yum install -y git
sudo yum -y install gcc-c++
```

clone numpy library
```
git clone https://github.com/vitolimandibhrata/aws-lambda-numpy.git
```

clone repository
```
git clone https://github.com/sparkgene/lambda_image_to_video
```

copy numpy and library in to work directory.
```
cp -R aws-lambda-numpy/lib lambda_image_to_video/
cp -R aws-lambda-numpy/numpy lambda_image_to_video/
```

download freeimage binary
```
wget https://github.com/imageio/imageio-binaries/raw/master/freeimage/libfreeimage-3.16.0-linux64.so -O lambda_image_to_video/lib/libfreeimage.so
```

download ffmpeg binary
```
wget https://github.com/imageio/imageio-binaries/raw/master/ffmpeg/ffmpeg.linux64 -O lambda_image_to_video/ffmpeg.linux64
```

install python library
```
cd lambda_image_to_video
pip install -r requirements.txt -t /path/to/lambda_image_to_video
```

set bucket name
```
cd lambda_image_to_video
vi lambda_function.py

image_bucket = "set the input image bucket name"
video_bucket = "set the output video bucket name"
```

install MoviePy
```
pip install -r requirements.txt -t ./
```

compress all files in to zip.
```
zip -r func.zip . -x *.git*
```
http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

### Upload to your lambda function
  See details createing scheduled lambda function.
  http://docs.aws.amazon.com/lambda/latest/dg/getting-started-scheduled-events.html

## Caution

Using this scripts on AWS is not free.

[AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
