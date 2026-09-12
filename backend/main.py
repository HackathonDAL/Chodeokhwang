import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from .schemas import AnalyzeRequest, AnalyzeResponse
from .scoring import DATA_DIR, load_data, recommend
from .service import analyze, student_profile


def create_app(data_dir=None):
    directory = Path(data_dir or os.getenv("SOADAL_DATA_DIR", str(DATA_DIR)))
    app = FastAPI(title="KU Compass Result API", version="1.0.0")
    origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000")
    app.add_middleware(CORSMiddleware, allow_origins=[s.strip() for s in origins.split(",") if s.strip()],
                       allow_methods=["GET", "POST"], allow_headers=["Content-Type"],
                       expose_headers=["X-Explanation-Source"])

    def checked(request):
        try:
            courses, _ = load_data(directory)
            unknown = sorted({c.course_code for c in request.courses} - set(courses.course_code))
            if unknown:
                raise HTTPException(422, detail={"code": "UNKNOWN_COURSE", "course_codes": unknown})
        except (OSError, ValueError):
            raise HTTPException(503, detail={"code": "DATA_UNAVAILABLE", "message": "CSV 데이터 구성을 확인하세요."})

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/api/analyze", response_model=AnalyzeResponse)
    def result(request: AnalyzeRequest, response: Response):
        checked(request)
        try:
            body, source = analyze(request, directory)
        except (ValueError, OSError):
            raise HTTPException(503, detail={"code": "DATA_UNAVAILABLE", "message": "분야·대표 과목 CSV를 확인하세요."})
        response.headers["X-Explanation-Source"] = source
        response.headers["Cache-Control"] = "no-store"
        return body

    @app.post("/api/unexplored")
    def unexplored(request: AnalyzeRequest, response: Response):
        checked(request)
        try:
            result = recommend(student_profile(request), data_dir=directory)
        except (ValueError, OSError):
            raise HTTPException(503, detail={"code": "DATA_UNAVAILABLE"})
        response.headers["Cache-Control"] = "no-store"
        return {"unexplored_fields": result["unexplored_fields"]}

    return app


app = create_app()
