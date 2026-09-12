"""탐색 지원용 규칙 기반 추천. 점수는 적성 확률이 아니다."""
from dataclasses import asdict, dataclass
from pathlib import Path
import math

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@dataclass(frozen=True)
class RecommendationConfig:
    exposure_relevance: float = 0.3
    # 검증 전 프로토타입 정책값. 사용자 실험 후 조정한다.
    direct_relevance: float = 0.5
    min_direct_courses: int = 2
    min_direct_relevance: float = 1.2
    min_recommendation_score: float = 0.6
    candidate_relevance: float = 0.5
    top_k: int = 3
    early_interest: float = 4.0

    def __post_init__(self):
        if not math.isfinite(self.early_interest) or not 0 <= self.early_interest <= 5:
            raise ValueError("초기 관심 기준은 0~5여야 합니다.")
        if not 0 < self.exposure_relevance <= self.direct_relevance:
            raise ValueError("탐색 기준은 0 초과 직접 관련 기준 이하여야 합니다.")
        for value in (self.direct_relevance, self.candidate_relevance):
            if not math.isfinite(value) or not 0 < value <= 1:
                raise ValueError("연관도 기준은 0 초과 1 이하여야 합니다.")
        if not 0 <= self.min_recommendation_score <= 1:
            raise ValueError("추천 점수 기준은 0~1이어야 합니다.")
        if not math.isfinite(self.min_direct_relevance) or self.min_direct_relevance <= 0:
            raise ValueError("최소 연관도 합은 양수여야 합니다.")
        for value in (self.min_direct_courses, self.top_k):
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError("과목 수와 Top K는 양의 정수여야 합니다.")


def load_data(data_dir=DATA_DIR):
    directory = Path(data_dir)
    courses = pd.read_csv(directory / "courses.csv")
    matrix = pd.read_csv(directory / "course_field_matrix.csv")
    if not {"course_code", "course_name", "department"} <= set(courses.columns):
        raise ValueError("courses.csv 필수 열이 없습니다.")
    if "course_code" not in matrix or len(matrix.columns) < 2:
        raise ValueError("분야 행렬 형식을 확인하세요.")
    for frame in (courses, matrix):
        if frame.isna().any().any():
            raise ValueError("CSV에 누락된 값이 있습니다.")
        if frame.course_code.duplicated().any():
            raise ValueError("CSV에 중복된 과목 코드가 있습니다.")
    if set(courses.course_code) != set(matrix.course_code):
        raise ValueError("두 CSV의 과목 코드 목록이 일치하지 않습니다.")
    values = matrix.drop(columns="course_code").apply(pd.to_numeric, errors="raise")
    if not ((values >= 0) & (values <= 1)).all().all():
        raise ValueError("분야 연관도는 유한한 0~1 값이어야 합니다.")
    matrix[values.columns] = values
    return courses, matrix


def load_representative_courses(courses, matrix, data_dir=DATA_DIR,
                                direct_relevance=0.5):
    """분야별 대표 탐색 과목을 읽고 데이터 간 일관성을 검증한다."""
    directory = Path(data_dir)
    path = directory / "RepresentSubject.csv"
    if not path.exists():
        path = directory / "field_representative_courses.csv"
    representatives = pd.read_csv(path)
    required = {"field", "representative_course_code"}
    if not required <= set(representatives.columns):
        raise ValueError("대표 과목 CSV 필수 열이 없습니다.")
    if representatives[list(required)].isna().any().any():
        raise ValueError("대표 과목 CSV에 누락된 값이 있습니다.")
    if representatives.field.duplicated().any():
        raise ValueError("한 분야에 대표 과목이 여러 개 등록되어 있습니다.")

    matrix_fields = set(matrix.columns) - {"course_code"}
    representative_fields = set(representatives.field)
    if matrix_fields != representative_fields:
        missing = sorted(matrix_fields - representative_fields)
        extra = sorted(representative_fields - matrix_fields)
        raise ValueError(f"대표 과목 분야 목록이 일치하지 않습니다. 누락={missing}, 초과={extra}")

    course_codes = set(courses.course_code)
    unknown = sorted(set(representatives.representative_course_code) - course_codes)
    if unknown:
        raise ValueError("등록되지 않은 대표 과목 코드: " + ", ".join(unknown))

    weights = matrix.set_index("course_code")
    for row in representatives.itertuples(index=False):
        relevance = float(weights.loc[row.representative_course_code, row.field])
        if relevance < direct_relevance:
            raise ValueError(
                f"{row.field} 대표 과목 {row.representative_course_code}의 연관도가 "
                f"직접 관련 기준({direct_relevance})보다 낮습니다."
            )
    return representatives


def calculate_course_score(grade, interest):
    if isinstance(grade, bool) or isinstance(interest, bool):
        raise ValueError("성적과 흥미는 숫자로 입력하세요.")
    grade, interest = float(grade), float(interest)
    if not math.isfinite(grade) or not 0 <= grade <= 4.5:
        raise ValueError("성적은 0~4.5여야 합니다.")
    if not math.isfinite(interest) or not 0 <= interest <= 5:
        raise ValueError("흥미는 0~5여야 합니다.")
    return 0.2 * grade / 4.5 + 0.8 * interest / 5


def recommend(student_courses, config=None, data_dir=DATA_DIR):
    """JSON 직렬화 가능한 결과. AI 설명에 전달할 근거도 포함한다."""
    config = config or RecommendationConfig()
    courses, matrix = load_data(data_dir)
    representatives = load_representative_courses(
        courses, matrix, data_dir, config.direct_relevance
    )
    names = courses.set_index("course_code").course_name.to_dict()
    weights = matrix.set_index("course_code")
    selected, seen = [], set()
    for item in student_courses:
        code = item["course_code"]
        if code not in names:
            raise ValueError(f"등록되지 않은 과목: {code}")
        if code in seen:
            raise ValueError(f"중복 입력 과목: {code}")
        score = calculate_course_score(item["grade"], item["interest"])
        seen.add(code)
        selected.append(dict(course_code=code, course_name=names[code],
                             grade=float(item["grade"]), interest=float(item["interest"]),
                             course_score=score))

    fields = []
    for field in weights.columns:
        evidence = []
        for item in selected:
            relevance = float(weights.loc[item["course_code"], field])
            if relevance > 0:
                evidence.append({**item, "relevance": relevance,
                                 "contribution": relevance * item["course_score"],
                                 "direct": relevance >= config.direct_relevance})
        relevance_sum = sum(e["relevance"] for e in evidence)
        score = (sum(e["contribution"] for e in evidence) / relevance_sum
                 if relevance_sum else None)
        direct = [e for e in evidence if e["direct"]]
        sufficient = (len(direct) >= config.min_direct_courses and
                      sum(e["relevance"] for e in direct) >= config.min_direct_relevance)
        early_candidate = (not sufficient and any(
            e["interest"] >= config.early_interest
            and e["course_score"] >= config.min_recommendation_score for e in direct))
        exposed = any(e["relevance"] >= config.exposure_relevance for e in evidence)
        status = "sufficient" if sufficient else "limited" if exposed else "unexplored"
        for e in evidence:
            e["weight_share"] = e["relevance"] / relevance_sum
        evidence.sort(key=lambda e: (-e["relevance"], e["course_code"]))
        explanation = (
            f"직접 관련 수강 과목 {len(direct)}개, 직접 연관도 합 "
            f"{sum(e['relevance'] for e in direct):.2f}. "
            + (f"성적 20%·흥미 80%의 연관도 가중평균은 {score * 100:.1f}점입니다. "
               if score is not None else "점수를 계산할 관련 경험이 없습니다. ")
            + ("설정된 근거 기준을 충족합니다." if sufficient else
               "직접 관련 수강 경험이 부족합니다. 낮은 선호를 뜻하지 않습니다.")
        )
        fields.append(dict(field=field, score=score,
                           score_points=round(score * 100, 2) if score is not None else None,
                           evidence_status=status, early_candidate=early_candidate, direct_course_count=len(direct),
                           direct_relevance_sum=sum(e["relevance"] for e in direct),
                           evidence=evidence, explanation=explanation))

    fields.sort(key=lambda f: (-(f["score"] if f["score"] is not None else -1), f["field"]))
    eligible = [f for f in fields if (f["evidence_status"] == "sufficient" or f["early_candidate"])
                and f["score"] >= config.min_recommendation_score]
    # 표시 점수가 같은 분야는 공동 순위. Top 3 경계 동점은 별도로 반환한다.
    for f in eligible:
        f["rank"] = 1 + sum(g["score_points"] > f["score_points"] for g in eligible)
    top_fields = eligible[:config.top_k]
    boundary_ties = ([f for f in eligible[config.top_k:]
                      if f["score_points"] == top_fields[-1]["score_points"]]
                     if top_fields else [])
    supported = []
    for code in sorted(set(names) - seen):
        related = [f for f in eligible if float(weights.loc[code, f["field"]])
                   >= config.candidate_relevance]
        base = dict(course_code=code, course_name=names[code],
                    prerequisites_status="unknown", course_level_status="unknown")
        if related:
            matches = [dict(field=f["field"], relevance=float(weights.loc[code, f["field"]]),
                            field_score=f["score"],
                            evidence_course_codes=[e["course_code"] for e in f["evidence"]
                                                   if e["direct"]]) for f in related]
            supported.append({**base, "matched_fields": matches,
                              "priority": max(m["relevance"] * m["field_score"] for m in matches)})
    supported.sort(key=lambda c: (-c["priority"], c["course_code"]))

    representative_by_field = representatives.set_index("field")[
        "representative_course_code"
    ].to_dict()
    unexplored_fields = []
    for field_result in sorted(fields, key=lambda f: f["field"]):
        if field_result["evidence_status"] != "unexplored":
            continue
        code = representative_by_field[field_result["field"]]
        # 검증상 보통 일어날 수 없지만, 수강한 대표 과목은 중복 추천하지 않는다.
        if code in seen:
            continue
        unexplored_fields.append({
            "field": field_result["field"],
            "representative_course": {
                "course_code": code,
                "course_name": names[code],
                "relevance": float(weights.loc[code, field_result["field"]]),
                "prerequisites_status": "unknown",
                "course_level_status": "unknown",
            },
            "reason": "직접 관련 수강 경험이 없어 선호를 아직 판단하지 않은 분야입니다.",
        })
    notices = []
    if not selected:
        notices.append("수강 과목을 입력하면 개인화 추천이 시작됩니다.")
    if len(top_fields) < config.top_k:
        notices.append("추천 점수와 근거 기준을 충족한 분야가 3개 미만입니다. 후보를 억지로 채우지 않습니다.")
    if boundary_ties or len({f["score_points"] for f in top_fields}) < len(top_fields):
        notices.append("동점 분야는 적합도 차이를 판단할 수 없습니다. 동점 내 표시는 분야명 순입니다.")
    unmapped = [s["course_code"] for s in selected if weights.loc[s["course_code"]].sum() == 0]
    if unmapped:
        notices.append("분야 연관도가 아직 등록되지 않아 판단에 반영되지 않은 과목: " + ", ".join(unmapped))
    return dict(policy=asdict(config), fields=fields, top_fields=top_fields,
                boundary_ties=boundary_ties, supported_courses=supported,
                unexplored_fields=unexplored_fields, notices=notices,
                roadmap_status="not_configured", explanation_source="rule_based")


def calculate_student_profile(student_courses, data_dir=DATA_DIR):
    """기존 호출 호환용. percentage는 확률이 아닌 100점 환산값이다."""
    result = recommend(student_courses, data_dir=data_dir)
    return pd.DataFrame([dict(field=f["field"], score=f["score"],
                              percentage=f["score_points"]) for f in result["fields"]])


if __name__ == "__main__":
    import json
    print(json.dumps(recommend([]), ensure_ascii=False, indent=2, allow_nan=False))

