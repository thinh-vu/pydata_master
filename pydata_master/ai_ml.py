# I. Transcribe Youtube Videos
### !pip install git+https://github.com/openai/whisper.git -q
import os
from .util import lmt_detect, ROOT_DIR
import pytube
from pytube import YouTube
import whisper

def transcribe(link, model='medium'):
  lmt = lmt_detect()
  yt = YouTube(link)
  yt.streams.filter(only_audio=True)[0]\
          .download(output_path='') # save audio file to current directory
  file_path = lmt.join([ROOT_DIR, video_title(link)]) + '.mp4'
  os.system('whisper "{}" --model {}'.format(file_path, model))
  return file_path + '.txt'

def video_title(link):
  yt = YouTube(link)
  name = yt.title
  return name

## Free up memory from large model data
def free_memory():
    import gc
    import torch
    gc.collect()
    torch.cuda.empty_cache()
