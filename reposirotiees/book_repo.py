from typing import Optional, List

from psycopg2.extras import RealDictCursor

from models.book_models import BookResponse, BookCreate, BookPatch
from reposirotiees.database_config import get_db_connection


class BookRepository:

    def get_by_id(self, book_id: int) -> Optional[BookResponse]:

        connection = get_db_connection()

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            "Select * FROM books where id =%s",(book_id,)
        )

        book = cursor.fetchone()
        cursor.close()
        connection.close()

        return BookResponse(**book) if book else None
        # BookResponse(**book) = {id:1,title: "Atomic habit"} -> BookResponse(id = 1, title = "Atomic..")

    def get_all(self,offset:int,limit:int) -> List[BookResponse]:

        connection = get_db_connection()

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            " Select * FROM books OFFSET %s LIMIt %s",(offset,limit)
        )

        books = cursor.fetchall()
        cursor.close()
        connection.close()

        return [BookResponse(**book) for book in books]


    def create_book(self, book: BookCreate) -> BookResponse:

        connection = get_db_connection()

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        query = """
        Insert into books 
        (title,author,isbn,price,updated_at)
        Values(%s,%s,%s,%s,NULL)
        RETURNING * """

        try:
            cursor.execute(query,(book.title,book.author,book.isbn,book.price))

            new_book = cursor.fetchone()

            connection.commit()

            return BookResponse(**new_book)

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            cursor.close()
            connection.close()

    def delete_book(self,book_id: int) -> bool:

        connection = get_db_connection()

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(
                "DELETE FROM books where id = %s",
                (book_id,)
            )

            connection.commit()
            return cursor.rowcount > 0

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            cursor.close()
            connection.close()

    def update_book(self,book_id:int, book: BookCreate) -> Optional[BookResponse]:

        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        query = """UPDATE books SET title =%s,
        author = %s,
        isbn = %s,
        price = %s,
        updated_at = CURRENT_TIMESTAMP
        WHERE id =%s
        RETURNING *"""

        try:
            cursor.execute(query,(book.title,book.author,book.isbn,book.price,book_id))

            updated_book = cursor.fetchone()
            connection.commit()

            return BookResponse(**updated_book) if updated_book else None

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            cursor.close()
            connection.close()

    def patch_book(self,book_id: int,book: BookPatch) -> Optional[BookResponse]:

        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        try:
            update_data = book.model_dump(exclude_none=True)

            if not update_data:
                return self.get_by_id(book_id)

            set_clause = ", ".join(
                [f"{field} = %s" for field in update_data.keys()]
            )

            set_clause += ", updated_at = CURRENT_TIMESTAMP"

            values = list(update_data.values())
            values.append(book_id)

            query = f"""
                UPDATE books
                SET {set_clause}
                WHERE id = %s
                RETURNING *
            """

            cursor.execute(query, tuple(values))

            patched_book = cursor.fetchone()
            connection.commit()

            return BookResponse(**patched_book) if patched_book else None

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            cursor.close()
            connection.close()



