from typing import Optional, List

from fastapi import APIRouter

from models.book_models import BookResponse, BookCreate
from reposirotiees.book_repo import BookRepository
from services.book_service import BookService

router = APIRouter(prefix="/books",tags=["books"])

repo = BookRepository()
service = BookService(repo)


@router.get("/{book_id}",response_model=Optional[BookResponse])
def get_book(book_id: int):
    return service.get_by_id(book_id)

@router.get("",response_model=List[BookResponse])
def get_all(offset:int = 0, limit: int = 10):
    return service.get_all_books(offset, limit)


@router.post("/",response_model=BookResponse)
def create_book(request:BookCreate):
    return service.create_book(request)


@router.delete("/{book_id}",response_model=Optional[BookResponse])
def delete_book(book_id:int):
    return service.delete_book(book_id)

