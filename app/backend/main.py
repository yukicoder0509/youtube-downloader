# yt-dlp usage reference 
# https://ivonblog.com/posts/yt-dlp-usage/ 
# https://www.cnblogs.com/woden3702/p/18227001/ytdlp-guide-chinese-version-1awurp
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from media import download, MediaType, DownloadRequest
from file import scan_dir

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/scan")
def scan(depth: int | None = None):
    tree = scan_dir(os.getcwd(), depth=depth)
    return tree

@app.post("/download")
def download_media(req: DownloadRequest):
    download(req)

