// 백엔드가 아직 없을 때 결과 화면을 그리기 위한 목(mock) 응답 데이터.
// 실제 API 연동 시 이 구조 그대로 응답이 온다고 가정하고 화면을 개발한다.
// 정확한 필드 설명은 docs/RESULT_API_SPEC.md 참고.
export const mockResponse = {
  top_fields: [
    {
      field_id: "ML",
      field_name: "Machine Learning",
      field_name_kr: "머신러닝",
      score: 92,
      ai_reason:
        "기계학습과 최적화 과목에서 모두 A+ 학점과 최고 흥미도를 보였고, 자료구조·알고리즘 성취도도 높아 이론과 구현을 함께 다루는 역량이 뚜렷합니다. 특히 최적화 이론에 대한 흥미가 다른 지원자 대비 두드러져, 모델 학습 원리를 깊이 파고드는 연구/엔지니어링 방향에 잘 맞는 프로필로 판단했습니다.",
      career_roadmap: {
        roles: ["ML Engineer", "AI Researcher", "Data Scientist"],
        stages: [
          { stage: "지금", milestone: "기계학습·최적화 수강 완료" },
          { stage: "다음 학기", milestone: "딥러닝, 데이터과학 수강 추천" },
          { stage: "졸업 후", milestone: "ML Engineer 취업 또는 대학원 진학" },
        ],
      },
      evidence_courses: [
        {
          course_code: "COSE362",
          course_name: "기계학습",
          grade: "A+",
          interest_score: 5,
          contribution: "학점·흥미도 모두 최고 수준으로 가장 크게 기여",
        },
        {
          course_code: "COSE461",
          course_name: "자연어처리",
          grade: "A+",
          interest_score: 4,
          contribution: "응용 분야 성취도가 높아 실전 역량을 뒷받침",
        },
      ],
      explore_courses: [
        {
          course_code: "COSE474",
          course_name: "딥러닝",
          department: "COSE",
          why: "기계학습 이후 자연스럽게 이어지는 심화 과목이지만 아직 수강하지 않았어요",
        },
        {
          course_code: "CSAI310",
          course_name: "고급강화학습",
          department: "CSAI",
          why: "관심 분야와 연결되는 최신 세부 분야로, 탐색해보면 좋아요",
        },
      ],
      labs: [
        {
          professor: "홍길동",
          lab_name: "AI Lab",
          lab_url: "https://example.com",
        },
      ],
    },
    {
      field_id: "STAT",
      field_name: "Statistics",
      field_name_kr: "통계학",
      score: 85,
      ai_reason:
        "확률및랜덤과정, 데이터과학 과목에서 꾸준히 높은 학점을 유지했고 수리적인 과목에 대한 흥미도도 안정적으로 높았습니다. 데이터를 다루는 기초 체력이 탄탄해, 통계적 방법론을 활용한 분석·의사결정 직무와 궁합이 좋다고 판단했습니다.",
      career_roadmap: {
        roles: ["Data Analyst", "Statistician", "Quant Researcher"],
        stages: [
          { stage: "지금", milestone: "확률및랜덤과정, 데이터과학 수강 완료" },
          { stage: "다음 학기", milestone: "회귀분석, 통계적머신러닝 수강 추천" },
          { stage: "졸업 후", milestone: "데이터 분석가 취업 또는 대학원 진학" },
        ],
      },
      evidence_courses: [
        {
          course_code: "COSE382",
          course_name: "확률및랜덤과정",
          grade: "A+",
          interest_score: 5,
          contribution: "수리 기초 과목에서의 높은 성취가 핵심 근거",
        },
        {
          course_code: "COSE471",
          course_name: "데이터과학",
          grade: "A",
          interest_score: 4,
          contribution: "데이터 분석 실무 감각을 보여주는 과목",
        },
      ],
      explore_courses: [
        {
          course_code: "STAT424",
          course_name: "통계적머신러닝",
          department: "STAT",
          why: "통계와 머신러닝을 잇는 과목으로 다음 단계로 추천해요",
        },
        {
          course_code: "STAT342",
          course_name: "회귀분석",
          department: "STAT",
          why: "통계학 분야의 기본기를 다지기 좋은 과목이에요",
        },
      ],
      labs: [
        {
          professor: "김철수",
          lab_name: "Data Science Lab",
          lab_url: "https://example.com",
        },
      ],
    },
    {
      field_id: "OPT",
      field_name: "Optimization",
      field_name_kr: "최적화",
      score: 80,
      ai_reason:
        "최적화, 자료구조 과목에서 높은 흥미도를 보이며 수리적 사고와 알고리즘적 문제 해결을 동시에 즐기는 성향이 드러났습니다. 정답이 명확한 문제를 효율적으로 푸는 것을 좋아하는 편이라, 알고리즘·운영 최적화 관련 직무에서 강점을 발휘할 것으로 예상됩니다.",
      career_roadmap: {
        roles: [
          "Operations Research Analyst",
          "Algorithm Engineer",
          "Research Scientist",
        ],
        stages: [
          { stage: "지금", milestone: "최적화, 자료구조 수강 완료" },
          { stage: "다음 학기", milestone: "알고리즘, 컴파일러 수강 추천" },
          { stage: "졸업 후", milestone: "알고리즘 엔지니어 취업 또는 대학원 진학" },
        ],
      },
      evidence_courses: [
        {
          course_code: "COSE461",
          course_name: "자연어처리",
          grade: "A+",
          interest_score: 4,
          contribution: "수리 기반 문제 해결 역량을 보여주는 과목",
        },
        {
          course_code: "COSE213",
          course_name: "자료구조",
          grade: "A",
          interest_score: 4,
          contribution: "알고리즘적 사고의 기초가 되는 과목",
        },
      ],
      explore_courses: [
        {
          course_code: "COSE214",
          course_name: "알고리즘",
          department: "COSE",
          why: "최적화 이론을 실제 알고리즘 설계에 적용해볼 수 있어요",
        },
        {
          course_code: "COSE312",
          course_name: "컴파일러",
          department: "COSE",
          why: "최적화 기법이 실제로 쓰이는 대표적인 시스템 과목이에요",
        },
      ],
      labs: [
        {
          professor: "이영희",
          lab_name: "Optimization Lab",
          lab_url: "https://example.com",
        },
      ],
    },
  ],
}

export default mockResponse
