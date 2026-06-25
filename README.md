# Download youtube a video or audio via youtube-downloader

1. Host the service on the machine that to want to download the videos or audios.
2. Put the directory where you want to download media in .env file at the top level of the project (key: MNT_MEDIA_DOWNLOAD_DIR)
3. Open a youtube video.
4. Substitude the host name from youtube the the service's host name.
5. Then you will see the downloader UI!

# Local Development

## 1. Build frontend

The frontend supports three build environments, each reading from a different env file:

| Command | Env file | Intended use |
|---|---|---|
| `npm run build` / `npm run build:production` | `.env.production` | Production deployment |
| `npm run build:preview` | `.env.preview` | Staging / preview deployment |
| `npm run build:dev` | `.env` | Local development |

Set `VITE_BACKEND_URL` in the corresponding env file before building, then run:

```bash
cd app/frontend
npm install
npm run build:dev   # or build:preview / build:production
```

This will emit to `app/backend/frontend-dist`. The website will later be served by backend server.

Note that the backend URL will be hardcoded in the build result. So make sure to rebuild when the backend URL is changed.

## 2. Start backend server

First enter backend directory

```bash
cd app/backend
```

Install dependencies

```bash
uv sync
```

Then start the server

```bash
source .venv/bin/activate
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

Then the system will be hosted on http://0.0.0.0:8000
