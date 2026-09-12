from .catalog import CATALOG, FIELD_DESCRIPTIONS, CAREER_DESCRIPTIONS
from .schemas import AnalyzeRequest, AnalyzeResponse, GRADE_POINTS
from .scoring import load_data, recommend, DATA_DIR
from .explanations import generate_reason


def student_profile(request):
    return [{"course_code": c.course_code, "grade": GRADE_POINTS[c.grade],
             "interest": c.interest_score} for c in request.courses]


def learning_description(course):
    interest = ("높은 흥미를 표현한 과목이에요" if course.interest_score >= 4 else
                "보통 정도의 흥미를 표현한 과목이에요" if course.interest_score == 3 else
                "흥미가 크지 않았던 과목이에요")
    achievement = ("학업 성취도도 좋은 편이에요" if GRADE_POINTS[course.grade] >= 4 else
                   "학습 경험과 성취를 함께 돌아볼 수 있어요" if GRADE_POINTS[course.grade] >= 2 else
                   "학습 과정에서 어려웠던 부분도 함께 돌아보면 좋아요")
    return interest + ". " + achievement + "."


def analyze(request: AnalyzeRequest, data_dir=DATA_DIR):
    profile = recommend(student_profile(request), data_dir=data_dir)
    courses, matrix = load_data(data_dir)
    catalog = courses.set_index("course_code").to_dict("index")
    inputs = {c.course_code: c for c in request.courses}
    weights = matrix.set_index("course_code")
    # 충분한 근거 또는 직접 관련 과목에서 확인된 높은 초기 관심을 추천한다.
    ranked = profile["top_fields"]
    fields, sources = [], []
    for f in ranked:
        field_id = f["field"]
        if field_id not in CATALOG:
            raise ValueError(f"분야 표시명 매핑 없음: {field_id}")
        english, korean, _ = CATALOG[field_id]
        evidence = []
        for e in sorted(f["evidence"], key=lambda e: (not e["direct"], -e["contribution"], e["course_code"]))[:3]:
            c = inputs[e["course_code"]]
            evidence.append(dict(course_code=c.course_code, course_name=e["course_name"],
                                 grade=c.grade, interest_score=c.interest_score,
                                 contribution=learning_description(c)))
        candidates = [(code, float(weights.loc[code, field_id])) for code in catalog
                      if code not in inputs and float(weights.loc[code, field_id]) > 0]
        candidates.sort(key=lambda pair: (-pair[1], pair[0]))
        explore = [dict(course_code=code, course_name=catalog[code]["course_name"],
                        department=catalog[code]["department"],
                        why=f"{korean} 분야를 더 알아볼 수 있는 미수강 과목이에요. 수업에서 다루는 주제가 궁금하다면 다음 탐색 후보로 살펴보세요.")
                   for code, weight in candidates[:2]]
        names = ", ".join(e["course_name"] for e in evidence)
        warning = "현재 수강 경험을 바탕으로 한 추천이므로, 새로운 과목을 경험하면서 관심 분야가 달라질 수 있어요."
        if sum(g["score_points"] == f["score_points"] for g in profile["fields"]) > 1:
            warning += " 비슷하게 추천된 분야도 함께 살펴보세요."
        if f["early_candidate"]:
            warning += " 아직 관련 수강 경험이 적어 초기 관심 후보로 소개해요. 다른 관련 수업을 통해 관심을 더 확인해보세요."
        interested = [e["course_name"] for e in evidence if e["interest_score"] >= 4]
        fallback = ((f"{', '.join(interested)}에서 표현한 흥미가 {korean} 분야를 탐색할 단서가 되었어요. "
                     if interested else f"{names}의 학습 경험을 바탕으로 {korean} 분야를 탐색 후보로 제안해요. ")
                    + "좋아했던 학습 경험을 중심으로 성취도도 함께 살펴 추천했어요.")
        context = dict(field_name_kr=korean,
                       evidence_courses=[dict(course_name=e["course_name"], description=e["contribution"])
                                         for e in evidence])
        reason, source = generate_reason(context, fallback)
        sources.append(source)
        fields.append(dict(field_id=field_id, field_name=english, field_name_kr=korean,
                           score=f["score_points"], ai_reason=reason + " " + warning,
                           field_description=FIELD_DESCRIPTIONS[field_id],
                           related_careers=CAREER_DESCRIPTIONS[field_id],
                           evidence_courses=evidence, explore_courses=explore))
    unexplored = []
    for item in profile["unexplored_fields"]:
        field_id = item["field"]
        english, korean, _ = CATALOG[field_id]
        course = item["representative_course"]
        reason = FIELD_DESCRIPTIONS[field_id]
        unexplored.append(dict(
            field_id=field_id, field_name=english, field_name_kr=korean,
            reason=reason,
            representative_course=dict(
                course_code=course["course_code"], course_name=course["course_name"],
                department=catalog[course["course_code"]]["department"],
                why="이 분야가 어떤 내용을 다루는지 알아보기 위한 대표 과목이에요.",
            ),
        ))
    return AnalyzeResponse(top_fields=fields, unexplored_fields=unexplored), ("mixed" if len(set(sources)) > 1 else sources[0] if sources else "rules")

