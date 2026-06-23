from fastapi import FastAPI

from routers.book_routers import router as book_router

app = FastAPI(title="Book Shop POS System")

app.include_router(book_router)