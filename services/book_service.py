from dataclasses import dataclass
from typing import Optional

from starlette import status
from starlette.exceptions import HTTPException

from models.book_models import BookResponse, BookCreate, BookPatch
from reposirotiees.book_repo import BookRepository


class BookService:

    def __init__(self, repo: BookRepository):
        self.repo = repo

    def get_by_id(self, book_id: int) -> Optional[BookResponse]:

        book = self.repo.get_by_id(book_id)

        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book Not Found")

        return book


    def get_all_books(self,offset:int = 0, limit:int = 10):

        books = self.repo.get_all(offset,limit)

        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Books Not Found")

        return books

    def create_book(self, book:BookCreate):

        try:
            return self.repo.create_book(book)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def delete_book(self,book_id:int):

        try:

            deleted = self.repo.delete_book(book_id)

            if not deleted:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

            return True

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def update_book(self, book_id: int, book:BookCreate):

        try:

            updated = self.repo.update_book(book_id,book)

            if not updated:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

            return updated

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def patch_book(self,book_id:int, book:BookPatch):
        try:

            updated = self.repo.patch_book(book_id,book)

            if not updated:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

            return updated

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))




