# lambda_image_to_video
This AWS Lambda function create time-plus video from images.

## Overview

This is a Lambda function for creating time-plus video from images.
Input image must stored in s3 bucket with key like "yyyy/mm/dd/sequence_id.jpg".
Output video type is mp4. The video created by lambda function is placed to bucket with key "yyyy/mm/yyyymmdd.mp4".
All image with same key "yyyy/mm/dd", are stored in same video.

## Installation

```
git clone https://github.com/sparkgene/lambda_image_to_video
pip install -r requirements.txt -t /path/to/lambda_image_to_video
```

## Configuration

```
image_bucket = "set the input image bucket name"
video_bucket = "set the output video bucket name"
```

## deploy
### Pack function

  ``` shell
  zip -r func.zip . -x .git/**/*
  ```
  details
  http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

### Upload to your lambda function
  See details createing scheduled lambda function.
  http://docs.aws.amazon.com/lambda/latest/dg/getting-started-scheduled-events.html

## Caution

Using this scripts on AWS is not free.

[AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
