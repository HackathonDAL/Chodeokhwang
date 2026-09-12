// 사용자가 입력을 마치면 백엔드로 보낼 요청 형식 예시
// courses: 사용자가 수강한 과목 목록 (과목 코드 / 흥미도 / 성적)
// mbti, preferred_field: 선택 입력 항목 (입력하지 않으면 null)
export const requestExample = {
  courses: [
    { course_code: "COSE362", interest_score: 5, grade: "A+" },
  ],
  mbti: null,
  preferred_field: null,
}

export default requestExample
