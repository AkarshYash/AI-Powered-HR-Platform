from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine

# Import routers
from routers import auth, hr, ai, analytics

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="IntelliHire API", description="Enterprise AI-Powered HR Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow frontend to access API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(hr.router)
app.include_router(ai.router)
app.include_router(analytics.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to IntelliHire API"}
