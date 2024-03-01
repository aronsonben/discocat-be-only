from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from algorithm import ArtistScraper

spapi = FastAPI()

origins = [
    "*",
]

spapi.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@spapi.get("/")
def read_root():
    return {"Root Request": 200}

@spapi.get("/test")
def test():
    return {"Test Request": 200, "Info": "testing"}

@spapi.get("/grab/{uri}")
def grab_listeners(uri: Optional[str] = None):
    urilisteners = ArtistScraper("https://open.spotify.com/artist/" + uri)
    urilisteners.get_html()
    return urilisteners.get_monthlyListeners()
