from fastapi import FastAPI
from app.database import Base, engine
from app.routes import user
from app.routes import user, finance
from app.routes import user, finance, dashboard


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router)
app.include_router(finance.router)
app.include_router(dashboard.router)

app.include_router(user.router)
app.include_router(user.router)
app.include_router(finance.router)

@app.get("/")
def home():
    return {"message": "Finance Backend Running 🚀"}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)