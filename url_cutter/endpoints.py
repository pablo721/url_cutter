# import datetime
# import validators
# from fastapi import APIRouter, Depends, Response, status
# from fastapi.responses import RedirectResponse
#
# from dependency_injector.wiring import inject, Provide
# from sqlalchemy.orm import Session
# from .db import DbClient
# from .containers import Container
# from .utils import get_hash
# from .repositories import NotFoundError
# from .models import Link
#
# router = APIRouter()
#
#
# def raise_not_found(request):
#     message = f"URL '{request.url}' not found"
#     raise HTTPException(status_code=404, detail=message)
#
#
# def raise_bad_request(message):
#     raise HTTPException(status_code=400, detail=message)
#
#
# @router.post('/url')
# def create_url(url, expire_time=None, db_client: DbClient = Depends(DbClient)):
#     if not validators.url(url):
#         raise_bad_request('Invalid URL.')
#
#     short_url_suffix = get_hash(url)
#     with Session(db_client.engine) as session:
#         link = Link(url=url, short_url_suffix=short_url_suffix)
#         if expire_time:
#             link.expire_date = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp() + expire_time)
#         session.add(link)
#         session.commit()
#         session.refresh(link)
#
#
# @router.get("/{url_suffix}")
# def short_link(url_suffix, request, db_client: DbClient = Depends(DbClient)):
#     with Session(db_client.engine) as session:
#         link = session.query(Link).get(url_suffix)
#         if link:
#             return RedirectResponse(link.url)
#         raise_not_found(request)
#
#
# @router.get('/')
# def list_links(db_client: DbClient = Depends(DbClient)):
#     with Session(db_client.engine) as session:
#         links = session.query(Link).all()
#         return links
#
#
#
