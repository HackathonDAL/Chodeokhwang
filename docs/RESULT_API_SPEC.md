# 진로 추천 결과 API 명세 (프론트 ↔ 백엔드)

프론트엔드 결과 화면(`ResultPage.jsx`, `FieldDetail`)이 그대로 그릴 수 있는 응답 형식입니다.
지금은 `frontend/src/mock/mockResponse.js`로 이 형식을 흉내 내고 있고, 백엔드가 준비되면
이 문서의 JSON 그대로 내려주면 프론트 코드 수정 없이 연결됩니다.

## 1. 요청 (Request)

`CourseBuilder`에서 "분석하기"를 누르면 아래 형식으로 요청합니다. (이미 구현되어 있음)

```json
{
  "courses": [
    { "course_code": "COSE362", "interest_score": 4, "grade": "A+" },
    { "course_code": "COSE474", "interest_score": 5, "grade": "A" }
  ],
  "mbti": null,
  "preferred_field": null
}
```

- `interest_score`: 0~5 (별점)
- `grade`: `A+ A B+ B C+ C D F` 중 하나
- `mbti`, `preferred_field`: 현재 화면에는 입력 UI가 없어 항상 `null`로 보냄. 나중에 입력 UI가 생기면 값이 채워질 자리.

## 2. 응답 (Response)

최상위는 `top_fields` 배열 하나이고, **점수 내림차순으로 정렬된 상위 3개**를 내려줍니다.

```json
{
  "top_fields": [
    {
      "field_id": "ML",
      "field_name": "Machine Learning",
      "field_name_kr": "머신러닝",
      "score": 92,

      "ai_reason": "기계학습과 최적화 과목에서 모두 A+ 학점과 최고 흥미도를 보였고, ...",

      "career_roadmap": {
        "roles": ["ML Engineer", "AI Researcher", "Data Scientist"],
        "stages": [
          { "stage": "지금", "milestone": "기계학습·최적화 수강 완료" },
          { "stage": "다음 학기", "milestone": "딥러닝, 데이터과학 수강 추천" },
          { "stage": "졸업 후", "milestone": "ML Engineer 취업 또는 대학원 진학" }
        ]
      },

      "evidence_courses": [
        {
          "course_code": "COSE362",
          "course_name": "기계학습",
          "grade": "A+",
          "interest_score": 5,
          "contribution": "학점·흥미도 모두 최고 수준으로 가장 크게 기여"
        }
      ],

      "explore_courses": [
        {
          "course_code": "COSE474",
          "course_name": "딥러닝",
          "department": "COSE",
          "why": "기계학습 이후 자연스럽게 이어지는 심화 과목이지만 아직 수강하지 않았어요"
        }
      ],

      "labs": [
        { "professor": "홍길동", "lab_name": "AI Lab", "lab_url": "https://example.com" }
      ]
    }
    // ... score 상위 2, 3위 필드도 동일한 구조로 2개 더
  ]
}
```

## 3. 필드별 설명 및 계산 방법 제안

| 필드 | 타입 | 설명 | 계산/생성 방법 제안 |
|---|---|---|---|
| `field_id` | string | 분야 코드. `data/course_field_matrix.csv`의 컬럼명 그대로 사용 (`ML`, `DS`, `Statistics`, `Computer_Vision`, `NLP`, ...) | 고정 매핑 |
| `field_name` | string | 분야 영문명 (표시용) | `field_id` → 영문명 매핑 테이블 |
| `field_name_kr` | string | 분야 한글명 (표시용) | `field_id` → 한글명 매핑 테이블 |
| `score` | number (0~100) | 이 분야에 대한 적합도 점수 | `backend/scoring.py`의 `calculate_student_profile()` 결과 `percentage` 그대로 사용 |
| `ai_reason` | string | 왜 이 분야가 추천됐는지 자연어 설명 (2~4문장) | **LLM API 호출로 생성.** 아래 "4. ai_reason 생성 가이드" 참고 |
| `career_roadmap.roles` | string[] | 관련 직종/직업 목록 (3~4개) | `field_id` → 직업 목록 매핑 테이블 (고정값으로 시작해도 무방) |
| `career_roadmap.stages` | {stage, milestone}[] | 단계별 진로 계획 (보통 3단계: 지금/다음 학기/졸업 후) | 규칙 기반: "지금"은 학생이 실제 들은 과목 중 이 분야 관련도 높은 과목, "다음 학기"는 `explore_courses`에서 relevance 상위 1~2개, "졸업 후"는 `roles`의 대표 직업 1개로 문장 생성. 필요하면 LLM으로 자연스럽게 다듬기 |
| `evidence_courses` | Course[] | 이 분야 점수에 크게 기여한, **학생이 실제로 들은** 과목 (2~3개) | `course_field_matrix.csv`의 relevance × 개별 과목 점수(`calculate_course_score`)가 높은 순으로 정렬 후 상위 N개 |
| `evidence_courses[].contribution` | string | 왜 이 과목이 근거가 되는지 한 줄 요약 | 규칙 기반 템플릿("학점 {grade}, 흥미도 {interest_score}점으로 ...") 또는 LLM 한 줄 생성 |
| `explore_courses` | Course[] | 이 분야와 관련도가 높지만 **학생이 아직 듣지 않은** 과목 (2개) | `course_field_matrix.csv`에서 relevance 높은 과목 중 `student_courses`에 없는 것 상위 N개 |
| `explore_courses[].why` | string | 왜 탐색해볼 만한지 한 줄 설명 | 규칙 기반 템플릿 또는 LLM 한 줄 생성 |
| `labs` | Lab[] | 관련 연구실 정보 (선택) | ⚠️ **현재 데이터 없음.** 교수/연구실/분야 매핑 데이터를 별도로 수집해야 함. 없으면 빈 배열 `[]`로 내려줘도 프론트에서 처리 가능 (섹션 숨김 처리 필요 시 알려주세요) |

`Course` 타입 공통 필드: `course_code`, `course_name` (+ 위 표의 필드별 추가 필드)

## 4. `ai_reason` 생성 가이드 (LLM API 연동)

1. 아래 정보를 프롬프트 컨텍스트로 구성합니다.
   - 학생이 입력한 과목 목록 (`course_name`, `grade`, `interest_score`)
   - `calculate_student_profile()`로 계산한 이 분야의 `score`
   - 이 분야에서 relevance가 높았던 상위 과목 (`evidence_courses`)
2. 프롬프트 예시:
   > 다음은 한 학생이 수강한 과목과 학점, 흥미도입니다: {과목 목록}.
   > 이 학생의 "{field_name_kr}" 분야 적합도 점수는 {score}점으로 계산되었습니다.
   > 이 중 특히 {evidence_courses 과목명들}에서 높은 성취를 보였습니다.
   > 왜 이 학생에게 "{field_name_kr}" 분야가 추천되는지, 학생 본인이 읽는다고 가정하고
   > 친근하고 구체적인 한국어 2~4문장으로 설명해주세요. 과목명을 근거로 들어 설명하세요.
3. 응답 텍스트를 그대로 `ai_reason`에 담아 반환합니다.
4. 3개 분야 모두 같은 방식으로 개별 호출(또는 한 번에 3개 생성하도록 배치 프롬프트) 하면 됩니다.

## 5. 참고

- 프론트 mock 예시 전체: [`frontend/src/mock/mockResponse.js`](../frontend/src/mock/mockResponse.js)
- 결과 화면 구현: [`frontend/src/components/ResultPage.jsx`](../frontend/src/components/ResultPage.jsx)
- 점수 계산 로직: [`backend/scoring.py`](../backend/scoring.py)
- 이 문서의 응답 형식과 다르게 내려줘야 하는 사정이 생기면, 먼저 프론트 담당자와 상의해주세요 (필드명이 하나만 달라도 화면이 깨집니다).
