import os
import subprocess
from enum import Enum
from pydantic import BaseModel, Field

class MediaType(Enum):
    VIDEO = "video"
    AUDIO = "audio"

class DownloadRequest(BaseModel):
    dir: str = Field(..., description="The directory to download the media file")
    type: MediaType = Field(..., description="The type of media to download")
    url: str = Field(..., description="The URL of the media file")

def download(request: DownloadRequest):
    dir = request.dir
    type = request.type
    url = request.url

    # Check if the media directory exists
    if not os.path.exists(dir):
        print(f"Directory {dir} does not exist.")
        return

    if type == MediaType.VIDEO:
        # Download the video using yt-dlp
        video_encoding = "vcodec:av01,vcodec:vp9,vcodec:h264,res,fps,acodec:opus,acodec:aac,br,filesize"
        subprocess.run(cwd=dir, args=["yt-dlp", 
                                      "--ignore-config",
                                      "--output", "%(title)s.%(ext)s", "-f", "bv*+ba/b", "-S", video_encoding,"--merge-output-format","mkv","--remux-video", "mkv",
                                      "--embed-thumbnail", "--embed-metadata", "--write-info-json", "--write-thumbnail", "--write-subs", "--sub-langs", "zh-Hant,zh-TW,zh-Hans,zh-CN,zh,en,en-US,ja,-live_chat", "--compat-options", "no-live-chat",
                                      url])
    
    elif type == MediaType.AUDIO:
        # Download the audio using yt-dlp
        audio_encoding = "acodec:opus,acodec:aac,br,filesize"
        subprocess.run(cwd=dir, args=["yt-dlp", 
                                      "--ignore-config",
                                      "--output", "%(title)s.%(ext)s", "-f", "ba/bestaudio", "-S", audio_encoding, "-x", "--audio-format", "m4a",
                                      "--embed-thumbnail", "--embed-metadata", "--write-info-json", "--write-thumbnail", "--write-subs", "--sub-langs", "zh-Hant,zh-TW,zh-Hans,zh-CN,zh,en,en-US,ja,-live_chat", "--compat-options", "no-live-chat",
                                      url])
