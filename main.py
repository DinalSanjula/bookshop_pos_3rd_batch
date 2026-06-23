from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.book_routers import router as book_router

app = FastAPI(title="Book Shop POS System")


app.add_middleware(CORSMiddleware,
                   allow_origins=["*"], allow_credentials=True,allow_methods =["*"],allow_headers=["*"])

app.include_router(book_router)