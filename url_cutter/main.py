import datetime
import validators
from fastapi import FastAPI, Depends, Response, status, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .db import session_local, engine
from .utils import get_hash
from .models import Link
from .schemas import URLBase, URL, URLInfo
from .models import Base
from .settings import BASE_URL



app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def raise_not_found(request):
    message = f"URL '{request.url}' not found"
    raise HTTPException(status_code=404, detail=message)


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.post('/url')
def create_url(url: URLBase, expire_time: int = None, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request('Invalid URL.')

    short_url_suffix = get_hash(url.target_url)
    link = Link(url=url.target_url, short_url_suffix=short_url_suffix)
    if expire_time:
        link.expire_date = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp() + expire_time)

    db.add(link)
    db.commit()
    db.refresh(link)
    return BASE_URL + link.short_url_suffix


@app.get("/{url_suffix}")
def short_link(url_suffix: str, request: Request, db: Session = Depends(get_db)):
    link = db.query(Link).get(url_suffix)
    if link:
        return RedirectResponse(link.url)
    raise_not_found(request)


@app.get('/')
def list_links(db: Session = Depends(get_db)):
    links = db.query(Link).all()
    return links
