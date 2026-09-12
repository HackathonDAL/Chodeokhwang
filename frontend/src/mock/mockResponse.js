// 백엔드가 아직 없을 때 결과 화면을 그리기 위한 목(mock) 응답 데이터
// 실제 API 연동 시 이 구조 그대로 응답이 온다고 가정하고 화면을 개발한다
export const mockResponse = {
  top_fields: [
    {
      field_id: "ML",
      field_name: "Machine Learning",
      score: 92,
      reason:
        "확률론, 머신러닝, 선형대수 등에서 높은 흥미도와 성취도를 보였습니다.",
      recommended_courses: [
        { course_code: "COSE471", course_name: "딥러닝" },
        { course_code: "COSE461", course_name: "최적화" },
      ],
      careers: ["ML Engineer", "AI Researcher", "Data Scientist"],
      labs: [
        { professor: "홍길동", lab_name: "AI Lab", lab_url: "https://example.com" },
      ],
      roadmap: {
        taken: ["확률론", "선형대수"],
        next: ["머신러닝", "최적화"],
        goal: "ML 프로젝트",
      },
    },
    {
      field_id: "STAT",
      field_name: "Statistics",
      score: 85,
      reason:
        "확률론, 통계학, 데이터분석 관련 과목에서 꾸준히 높은 성취도를 보였습니다.",
      recommended_courses: [
        { course_code: "STAT231", course_name: "통계학개론" },
        { course_code: "STAT332", course_name: "회귀분석" },
      ],
      careers: ["Data Analyst", "Statistician", "Quant Researcher"],
      labs: [
        { professor: "김철수", lab_name: "Data Science Lab", lab_url: "https://example.com" },
      ],
      roadmap: {
        taken: ["확률론", "통계학개론"],
        next: ["회귀분석", "베이지안통계"],
        goal: "데이터 분석 프로젝트",
      },
    },
    {
      field_id: "OPT",
      field_name: "Optimization",
      score: 80,
      reason:
        "선형대수, 최적화 이론 등 수리적 사고가 필요한 과목에서 높은 흥미도를 보였습니다.",
      recommended_courses: [
        { course_code: "COSE461", course_name: "최적화" },
        { course_code: "COSE362", course_name: "머신러닝" },
      ],
      careers: ["Operations Research Analyst", "Algorithm Engineer", "Research Scientist"],
      labs: [
        { professor: "이영희", lab_name: "Optimization Lab", lab_url: "https://example.com" },
      ],
      roadmap: {
        taken: ["선형대수", "최적화"],
        next: ["convex optimization", "알고리즘"],
        goal: "최적화 알고리즘 연구",
      },
    },
  ],
}

export default mockResponse
