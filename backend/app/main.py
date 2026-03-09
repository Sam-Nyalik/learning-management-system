from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router, workbook_router, worksheet_router, question_router, answer_router, grade_router

app = FastAPI(title="Workbook System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP, allow all. Restrict to Streamlit URL in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router.router)
app.include_router(workbook_router.router)
app.include_router(worksheet_router.router)
app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(grade_router.router)

@app.get("/")
def health():
    return {"status": "running"}