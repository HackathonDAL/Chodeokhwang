import copy
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, Mock
import httpx
from fastapi.testclient import TestClient
from backend.main import create_app
from backend.schemas import AnalyzeRequest, AnalyzeResponse
from backend.explanations import generate_reason
from backend.scoring import calculate_course_score
#살려주세요 ㅠㅠ
BODY = {"courses": [
    {"course_code": "STAT221", "grade": "B+", "interest_score": 3},
    {"course_code": "STAT342", "grade": "A+", "interest_score": 4},
    {"course_code": "COSE213", "grade": "A+", "interest_score": 3},
    {"course_code": "COSE361", "grade": "A+", "interest_score": 5},
], "mbti": None, "preferred_field": None}


class APITests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, {"ENABLE_LLM": "false"})
        env.start()
        self.addCleanup(env.stop)
        self.client = TestClient(create_app())
        self.addCleanup(self.client.close)

    def test_contract(self):
        response = self.client.post("/api/analyze", json=BODY)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        AnalyzeResponse.model_validate(data)
        self.assertEqual(set(data), {"top_fields", "unexplored_fields"})
        unexplored = data["unexplored_fields"]
        self.assertEqual({f["field_id"] for f in unexplored}, {"Computer_Architecture", "Embedded_Systems", "HCI", "infoSec"})
        self.assertEqual(len(unexplored), 4)
        self.assertTrue(all(f["representative_course"]["course_code"] not in {c["course_code"] for c in BODY["courses"]} for f in unexplored))
        self.assertEqual(len(data["top_fields"]), 3)
        scores = [f["score"] for f in data["top_fields"]]
        self.assertEqual(scores, sorted(scores, reverse=True))
        for field in data["top_fields"]:
            self.assertEqual(set(field), {"field_id", "field_name", "field_name_kr", "score", "ai_reason",
                                         "career_roadmap", "evidence_courses", "explore_courses", "labs"})
            self.assertEqual(field["labs"], [])
            self.assertEqual(len(field["career_roadmap"]["stages"]), 3)
            selected = {c["course_code"] for c in BODY["courses"]}
            self.assertTrue(all(e["course_code"] in selected for e in field["evidence_courses"]))
            self.assertTrue(all(e["course_code"] not in selected for e in field["explore_courses"]))
            self.assertLessEqual(len(field["explore_courses"]), 2)
        self.assertEqual(response.headers["x-explanation-source"], "rules")

    def test_interest_weight_and_friendly_copy(self):
        self.assertAlmostEqual(calculate_course_score(0, 5), 0.8)
        self.assertAlmostEqual(calculate_course_score(4.5, 0), 0.2)
        data = self.client.post("/api/analyze", json=BODY).json()
        from backend.catalog import FIELD_DESCRIPTIONS, CATALOG
        self.assertTrue(set(CATALOG) <= set(FIELD_DESCRIPTIONS))
        for field in data["top_fields"]:
            prose = [field["ai_reason"]] + [c["contribution"] for c in field["evidence_courses"]] + [c["why"] for c in field["explore_courses"]]
            for sentence in prose:
                self.assertNotRegex(sentence, r"연관도|가중치|점수|강의계획서|\d")
        for field in data["unexplored_fields"]:
            self.assertEqual(field["reason"], FIELD_DESCRIPTIONS[field["field_id"]])

    def test_unexplored_threshold(self):
        data = self.client.post("/api/unexplored", json=BODY).json()
        self.assertEqual({f["field"] for f in data["unexplored_fields"]},
                         {"Computer_Architecture", "Embedded_Systems", "HCI", "infoSec"})

    def test_infosec_recommendation_and_catalog(self):
        from backend.catalog import CATALOG, FIELD_DESCRIPTIONS
        from backend.scoring import load_data, load_representative_courses
        courses, matrix = load_data()
        fields = set(matrix.columns) - {"course_code"}
        reps = load_representative_courses(courses, matrix)
        self.assertEqual(len(fields), 16)
        self.assertEqual(set(reps.field), fields)
        self.assertTrue(fields <= set(CATALOG) & set(FIELD_DESCRIPTIONS))
        for removed in ("Econimics", "Economics", "Finance/Quant"):
            self.assertNotIn(removed, fields)
            self.assertNotIn(removed, CATALOG)
            self.assertNotIn(removed, FIELD_DESCRIPTIONS)
        sample = self.client.post("/api/analyze", json=BODY).json()
        unexplored = next(f for f in sample["unexplored_fields"] if f["field_id"] == "infoSec")
        self.assertEqual(unexplored["representative_course"]["course_code"], "COSE354")
        self.assertEqual(unexplored["reason"], FIELD_DESCRIPTIONS["infoSec"])
        body = {"courses": [{"course_code": code, "grade": "A+", "interest_score": 3 if code == "COSE354" else 5}
                            for code in ("COSE354", "COSE451", "CSAI401")]}
        response = self.client.post("/api/analyze", json=body)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        field = next(f for f in data["top_fields"] if f["field_id"] == "infoSec")
        self.assertEqual(field["field_name_kr"], "정보보안")
        self.assertAlmostEqual(field["score"], 88.97)
        self.assertTrue(field["career_roadmap"]["roles"])
        self.assertEqual(len(field["career_roadmap"]["stages"]), 3)
        self.assertTrue(field["explore_courses"])
        self.assertNotIn("infoSec", {f["field_id"] for f in data["unexplored_fields"]})
        # Indirect experience prevents unexplored classification without guaranteeing recommendation.
        limited = self.client.post("/api/analyze", json={"courses": [
            {"course_code": "COSE342", "grade": "A+", "interest_score": 5}]}).json()
        self.assertNotIn("infoSec", {f["field_id"] for f in limited["unexplored_fields"]})

    def test_unknown_duplicate_empty(self):
        variants = [{"courses": []}, {"courses": [BODY["courses"][0]] * 2},
                    {"courses": [{"course_code": "UNKNOWN", "grade": "A", "interest_score": 3}]}]
        for body in variants:
            self.assertEqual(self.client.post("/api/analyze", json=body).status_code, 422)

    def test_invalid_fields(self):
        for field, value in [("grade", "A0"), ("interest_score", 6), ("interest_score", -1),
                             ("interest_score", True), ("interest_score", 2.5)]:
            body = copy.deepcopy(BODY)
            body["courses"][0][field] = value
            self.assertEqual(self.client.post("/api/analyze", json=body).status_code, 422)

    def test_reserved_fields(self):
        self.assertEqual(self.client.post("/api/analyze", json={**BODY, "mbti": "INTJ"}).status_code, 422)

    def test_zero_interest_and_all_grades(self):
        for grade in ["A+", "A", "B+", "B", "C+", "C", "D", "F"]:
            body = {"courses": [{"course_code": "COSE362", "interest_score": 0, "grade": grade}]}
            self.assertEqual(self.client.post("/api/analyze", json=body).status_code, 200)
        self.assertEqual(calculate_course_score(0, 0), 0)

    def test_all_unmapped(self):
        body = {"courses": [{"course_code": "COSE401", "interest_score": 5, "grade": "A+"}]}
        data = self.client.post("/api/analyze", json=body).json()
        self.assertEqual(data["top_fields"], [])
        self.assertGreater(len(data["unexplored_fields"]), 0)

    def test_no_unexplored(self):
        from backend.scoring import load_data
        courses, _ = load_data()
        body = {"courses": [{"course_code": code, "grade": "A+", "interest_score": 5} for code in courses.course_code]}
        response = self.client.post("/api/analyze", json=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["unexplored_fields"], [])

    def test_cors(self):
        r = self.client.options("/api/analyze", headers={"Origin": "http://localhost:5173",
                                "Access-Control-Request-Method": "POST"})
        self.assertEqual(r.headers["access-control-allow-origin"], "http://localhost:5173")

    def test_missing_data(self):
        with tempfile.TemporaryDirectory() as tmp, TestClient(create_app(tmp)) as client:
            self.assertEqual(client.post("/api/analyze", json=BODY).status_code, 503)

    def test_llm_disabled(self):
        with patch("backend.explanations.httpx.post") as post:
            self.assertEqual(generate_reason({}, "fallback"), ("fallback", "rules"))
            post.assert_not_called()

    def test_llm_mock_success_and_failure(self):
        with patch.dict(os.environ, {"ENABLE_LLM": "true", "GEMINI_API_KEY": "test", "GEMINI_MODEL": "test"}):
            response = Mock()
            response.json.return_value = {"candidates": [
                {"content": {"parts": [{"text": "테스트 설명입니다."}]}}]}
            with patch("backend.explanations.httpx.post", return_value=response):
                self.assertEqual(generate_reason({}, "fallback"), ("테스트 설명입니다.", "llm"))
            with patch("backend.explanations.httpx.post", side_effect=httpx.TimeoutException("timeout")):
                self.assertEqual(generate_reason({}, "fallback"), ("fallback", "rules"))
            response.json.return_value = {"candidates": []}
            with patch("backend.explanations.httpx.post", return_value=response):
                self.assertEqual(generate_reason({}, "fallback"), ("fallback", "rules"))


if __name__ == "__main__":
    unittest.main()
