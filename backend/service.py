from .catalog import CATALOG
from .schemas import AnalyzeRequest, AnalyzeResponse, GRADE_POINTS
from .scoring import load_data, recommend, DATA_DIR
from .explanations import generate_reason


def student_profile(request):
    return [{"course_code": c.course_code, "grade": GRADE_POINTS[c.grade],
             "interest": c.interest_score} for c in request.courses]


def analyze(request: AnalyzeRequest, data_dir=DATA_DIR):
    profile = recommend(student_profile(request), data_dir=data_dir)
    courses, matrix = load_data(data_dir)
    catalog = courses.set_index("course_code").to_dict("index")
    inputs = {c.course_code: c for c in request.courses}
    weights = matrix.set_index("course_code")
    # 적은 간접 경험만으로 높은 점수가 나는 분야를 피하기 위해 근거 기준 충족 후보만 사용한다.
    ranked = profile["top_fields"]
    fields, sources = [], []
    for f in ranked:
        field_id = f["field"]
        if field_id not in CATALOG:
            raise ValueError(f"분야 표시명 매핑 없음: {field_id}")
        english, korean, roles = CATALOG[field_id]
        evidence = []
        for e in sorted(f["evidence"], key=lambda e: (-e["contribution"], e["course_code"]))[:3]:
            c = inputs[e["course_code"]]
            evidence.append(dict(course_code=c.course_code, course_name=e["course_name"],
                                 grade=c.grade, interest_score=c.interest_score,
                                 contribution=(f"학점 {c.grade}, 흥미도 {c.interest_score}/5, "
                                               f"분야 연관도 {e['relevance']:.2f}로 점수 계산에 반영됐어요.")))
        candidates = [(code, float(weights.loc[code, field_id])) for code in catalog
                      if code not in inputs and float(weights.loc[code, field_id]) > 0]
        candidates.sort(key=lambda pair: (-pair[1], pair[0]))
        explore = [dict(course_code=code, course_name=catalog[code]["course_name"],
                        department=catalog[code]["department"],
                        why=(f"{korean} 분야와 연관도 {weight:.2f}인 미수강 과목이에요. "
                             "선수과목과 개설 여부는 강의계획서에서 확인해 주세요."))
                   for code, weight in candidates[:2]]
        names = ", ".join(e["course_name"] for e in evidence)
        warning = ("점수는 적성 확률이 아니라 수강 경험의 가중평균이에요."
                   if f["evidence_status"] == "sufficient" else
                   "직접 관련 수강 경험이 충분하지 않아 확정 추천이 아닌 탐색 후보예요.")
        if f["score"] < .6:
            warning += " 현재 점수가 낮으므로 높은 선호로 해석하지 마세요."
        if sum(g["score_points"] == f["score_points"] for g in profile["fields"]) > 1:
            warning += " 동점 분야 간 우열은 판단하기 어려워요."
        fallback = (f"{names}의 성적과 흥미를 분야 연관도로 가중평균해 "
                    f"{korean} 점수가 {f['score_points']:.2f}점으로 계산됐어요.")
        context = dict(field_name_kr=korean, score=f["score_points"],
                       courses=[dict(course_name=catalog[c.course_code]["course_name"],
                                     grade=c.grade, interest_score=c.interest_score)
                                for c in request.courses], evidence_courses=evidence)
        reason, source = generate_reason(context, fallback)
        sources.append(source)
        next_names = ", ".join(e["course_name"] for e in explore)
        fields.append(dict(field_id=field_id, field_name=english, field_name_kr=korean,
                           score=f["score_points"], ai_reason=reason + " " + warning,
                           career_roadmap=dict(roles=roles, stages=[
                               dict(stage="지금", milestone=f"수강 기록: {names}. 흥미와 학습 경험을 돌아보세요."),
                               dict(stage="다음 학기", milestone=(f"{next_names} 수강 검토. 선수과목·개설 여부 확인 필요."
                                    if explore else "등록된 미수강 후보가 없어 상담·프로젝트 탐색을 검토하세요.")),
                               dict(stage="졸업 후", milestone=f"{roles[0]} 등 관련 직무 또는 대학원 탐색. 별도 역량 준비가 필요해요."),
                           ]), evidence_courses=evidence, explore_courses=explore, labs=[]))
    unexplored = []
    for item in profile["unexplored_fields"]:
        field_id = item["field"]
        english, korean, _ = CATALOG[field_id]
        course = item["representative_course"]
        reason = "입력한 수강 과목 중 이 분야의 탐색 기준(연관도 0.3 이상)을 충족하는 과목이 없어, 아직 선호를 판단하지 않았어요."
        unexplored.append(dict(
            field_id=field_id, field_name=english, field_name_kr=korean,
            reason=reason,
            representative_course=dict(
                course_code=course["course_code"], course_name=course["course_name"],
                department=catalog[course["course_code"]]["department"],
                why="분야를 알아보기 위한 대표 과목이에요. 선수과목과 개설 여부는 강의계획서에서 확인해 주세요.",
            ),
        ))
    return AnalyzeResponse(top_fields=fields, unexplored_fields=unexplored), ("mixed" if len(set(sources)) > 1 else sources[0] if sources else "rules")
