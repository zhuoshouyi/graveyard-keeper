#!/usr/bin/env python3
"""Graveyard Keeper Guide — Standalone FastAPI App"""
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Graveyard Keeper Guide")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BASE = Path(__file__).parent

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")

# Preload guide page
GUIDE_PAGE = (BASE / "templates" / "graveyard-keeper.html").read_text(encoding="utf-8")


@app.get("/game/graveyard-keeper/data.json")
def guide_data():
    """Serve the structured game data as JSON."""
    data_path = BASE / "static" / "graveyard-keeper-data.json"
    if data_path.exists():
        content = data_path.read_text(encoding="utf-8")
        return Response(content=content, media_type="application/json")
    raise HTTPException(404)


@app.get("/game/graveyard-keeper", response_class=HTMLResponse)
def graveyard_keeper_guide():
    return HTMLResponse(
        content=GUIDE_PAGE,
        headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    )


@app.get("/", response_class=HTMLResponse)
def index():
    """Redirect or show a landing page."""
    return HTMLResponse("""
    <html><head><meta http-equiv="refresh" content="0;url=/game/graveyard-keeper"></head>
    <body><p><a href="/game/graveyard-keeper">前往守墓人攻略</a></p></body>
    </html>
    """)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8898)
