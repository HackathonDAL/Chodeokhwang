from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

GRADE_POINTS = {"A+": 4.5, "A": 4.0, "B+": 3.5, "B": 3.0,
                "C+": 2.5, "C": 2.0, "D": 1.0, "F": 0.0}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CourseInput(StrictModel):
    course_code: str = Field(min_length=1, max_length=40)
    interest_score: int = Field(ge=0, le=5, strict=True)
    grade: Literal["A+", "A", "B+", "B", "C+", "C", "D", "F"]


class AnalyzeRequest(StrictModel):
    courses: list[CourseInput] = Field(min_length=1, max_length=200)
    mbti: str | None = Field(default=None, max_length=4)
    preferred_field: str | None = Field(default=None, max_length=80)

    @field_validator("mbti", "preferred_field")
    @classmethod
    def reserved(cls, value):
        if value is not None:
            raise ValueError("현재 버전에서는 null로 보내주세요. 아직 추천에 반영하지 않습니다.")
        return value

    @model_validator(mode="after")
    def unique_courses(self):
        codes = [c.course_code for c in self.courses]
        if len(codes) != len(set(codes)):
            raise ValueError("동일 과목을 중복 입력할 수 없습니다.")
        return self


class Stage(StrictModel):
    stage: str
    milestone: str


class Roadmap(StrictModel):
    roles: list[str]
    stages: list[Stage]


class Evidence(StrictModel):
    course_code: str
    course_name: str
    grade: str
    interest_score: int
    contribution: str


class Explore(StrictModel):
    course_code: str
    course_name: str
    department: str
    why: str


class Lab(StrictModel):
    professor: str
    lab_name: str
    lab_url: str


class FieldResult(StrictModel):
    field_id: str
    field_name: str
    field_name_kr: str
    score: float = Field(ge=0, le=100)
    ai_reason: str
    career_roadmap: Roadmap
    evidence_courses: list[Evidence]
    explore_courses: list[Explore]
    labs: list[Lab]


class UnexploredField(StrictModel):
    field_id: str
    field_name: str
    field_name_kr: str
    representative_course: Explore
    reason: str


class AnalyzeResponse(StrictModel):
    top_fields: list[FieldResult] = Field(max_length=3)
    unexplored_fields: list[UnexploredField] = Field(default_factory=list)
