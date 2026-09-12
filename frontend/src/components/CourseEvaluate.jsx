import { useState } from 'react'

const GRADES = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F']

function CourseEvaluate({ selectedCourses, onAnalyze }) {
  const [evaluations, setEvaluations] = useState(
    selectedCourses.map((course) => ({
      ...course,
      interest_score: 0,
      grade: 'A+',
    }))
  )

  const updateInterestScore = (course_code, score) => {
    setEvaluations((prev) =>
      prev.map((c) =>
        c.course_code === course_code ? { ...c, interest_score: score } : c
      )
    )
  }

  const updateGrade = (course_code, grade) => {
    setEvaluations((prev) =>
      prev.map((c) => (c.course_code === course_code ? { ...c, grade } : c))
    )
  }

  const handleAnalyze = () => {
    const requestBody = {
      courses: evaluations.map(({ course_code, interest_score, grade }) => ({
        course_code,
        interest_score,
        grade,
      })),
      mbti: null,
      preferred_field: null,
    }
    console.log('분석 요청 JSON:', requestBody)
    onAnalyze?.(requestBody)
  }

  return (
    <div className="course-evaluate">
      <h1>선택한 과목을 평가해주세요</h1>

      <div className="course-card-list">
        {evaluations.map((course) => (
          <div className="course-card" key={course.course_code}>
            <h2>{course.course_name}</h2>
            <p className="course-meta">
              {course.department} · {course.course_code}
            </p>

            <div className="field-row">
              <span className="field-label">흥미도</span>
              <div className="star-rating">
                {[1, 2, 3, 4, 5].map((star) => (
                  <span
                    key={star}
                    className={
                      star <= course.interest_score ? 'star filled' : 'star'
                    }
                    onClick={() => updateInterestScore(course.course_code, star)}
                  >
                    ★
                  </span>
                ))}
              </div>
            </div>

            <div className="field-row">
              <span className="field-label">학점</span>
              <select
                value={course.grade}
                onChange={(e) => updateGrade(course.course_code, e.target.value)}
              >
                {GRADES.map((grade) => (
                  <option key={grade} value={grade}>
                    {grade}
                  </option>
                ))}
              </select>
            </div>
          </div>
        ))}
      </div>

      <button type="button" onClick={handleAnalyze}>
        분석하기
      </button>
    </div>
  )
}

export default CourseEvaluate
