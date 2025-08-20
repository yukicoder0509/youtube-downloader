# yt-dlp usage reference 
# https://ivonblog.com/posts/yt-dlp-usage/ 
# https://www.cnblogs.com/woden3702/p/18227001/ytdlp-guide-chinese-version-1awurp
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from media import download, DownloadRequest
from file import scan_dir
from dotenv import load_dotenv
from pathlib import Path

DIST_DIR = Path(__file__).parent / "frontend-dist"
ENV_DIR = Path(__file__).parent.parent.parent.parent / ".env"
load_dotenv(ENV_DIR) # for local machine development

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scan")
def scan(depth: int | None = None):
    tree = scan_dir(os.environ["MEDIA_DOWNLOAD_DIR"], depth=depth)
    return tree

@app.post("/download")
def download_media(req: DownloadRequest):
    req.dir = os.environ["MEDIA_DOWNLOAD_DIR"] + "/" + req.dir
    download(req)


@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str, request: Request):
    path = DIST_DIR / full_path
    if path.is_file():
        return FileResponse(path)
    return FileResponse(DIST_DIR / "index.html")