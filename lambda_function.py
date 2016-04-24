# -*- coding: utf-8 -*-

import os
import stat
import shutil
import boto3
from datetime import datetime as dt
import logging

print('Loading function')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

lambda_tmp_dir = '/tmp' # Lambda fuction can use this directory.
image_path = "{0}/{1}".format(lambda_tmp_dir, "images")
video_path = "{0}/{1}".format(lambda_tmp_dir, "video")
video_name = "video.mp4"

# ffmpeg is stored with this script.
# When executing ffmpeg, execute permission is requierd.
# But Lambda source directory do not have permission to change it.
# So move ffmpeg binary to `/tmp` and add permission.
ffmpeg_bin = "{0}/ffmpeg.linux64".format(lambda_tmp_dir)
shutil.copyfile('/var/task/ffmpeg.linux64', ffmpeg_bin)
os.environ['IMAGEIO_FFMPEG_EXE'] = ffmpeg_bin
os.chmod(ffmpeg_bin, os.stat(ffmpeg_bin).st_mode | stat.S_IEXEC)

from moviepy.editor import *

s3 = boto3.client('s3')

image_bucket = ""
video_bucket = ""

def prepare_path(target):
  if os.path.exists(target):
    logger.info("{0} exists".format(target))
    shutil.rmtree(target)

  os.mkdir(target)

def copy_object(bucket, source, dest):
  name = source.split('/')[-1]
  local_file = "{0}/{1}".format(dest, name)
  logger.debug("{0} to {1}".format(source, local_file))
  s3.download_file(bucket, source, local_file)
  if os.path.exists(local_file):
      b = open(local_file,"r")

  return local_file

def create_video(images, video_file):
  images.sort()
  logger.info("create video from {0} images.".format(len(images)))
  clip = ImageSequenceClip(images, fps=1)
  clip.write_videofile(video_file)
  logger.info("video: {0}".format(video_file))

def move_video(video_file, bucket, dest_key):
  video = open(video_file,"r")

  s3.put_object(
    Bucket=bucket,
    ACL='public-read',
    Body=video,
    Key=dest_key,
    ContentType="video/mp4"
  )
  logger.info("video moved to {0}/{1}".format(bucket, dest_key))

def lambda_handler(event, context):
  tdatetime = dt.now()
  prefix = tdatetime.strftime('%Y/%m/%d/')
  result = s3.list_objects(
        Bucket=image_bucket,
        Prefix=prefix
    )


  images = []
  if 'Contents' in result:
    prepare_path(image_path)
    for item in result['Contents']:
      images.append(copy_object(image_bucket, item['Key'], image_path))
  else:
    return

  if len(images) > 0:
    prepare_path(video_path)
    video_file = "{0}/{1}".format(video_path, video_name)
    create_video(images, video_file)
    ymd = prefix.split('/')
    video_key = "{0}/{1}/{2}.mp4".format(ymd[0], ymd[1],"".join(ymd))
    move_video(video_file, video_bucket, video_key)
  else:
    return
