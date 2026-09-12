import { useState, useRef, useEffect } from 'react'
import { courses } from '../mock/courses'

const GRADES = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F']

// "+" 버튼을 눌렀을 때 뜨는 과목 검색 오버레이
function CourseSearchOverlay({ excludeCodes, onAdd, onClose }) {
  const [term, setTerm] = useState('')
  const inputRef = useRef(null)

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  const results = courses.filter((c) => {
    if (excludeCodes.has(c.course_code)) return false
    if (!term.trim()) return true
    const q = term.trim().toLowerCase()
    return (
      c.course_name.includes(term.trim()) ||
      c.course_code.toLowerCase().includes(q)
    )
  })

  return (
    <div className="search-overlay-backdrop" onClick={onClose}>
      <div className="search-overlay" onClick={(e) => e.stopPropagation()}>
        <div className="search-overlay-header">
          <input
            ref={inputRef}
            type="text"
            placeholder="과목명 또는 학수번호로 검색 (예: 딥러닝, COSE471)"
            value={term}
            onChange={(e) => setTerm(e.target.value)}
            className="course-search"
          />
          <button type="button" className="icon-btn" onClick={onClose} aria-label="닫기">
            ✕
          </button>
        </div>

        <ul className="search-result-list">
          {results.map((course) => (
            <li key={course.course_code}>
              <button type="button" onClick={() => onAdd(course)}>
                <span className="course-name">{course.course_name}</span>
                <span className="course-meta">
                  {course.course_code}
                </span>
              </button>
            </li>
          ))}
          {results.length === 0 && (
            <li className="empty-hint">검색 결과가 없습니다.</li>
          )}
        </ul>
      </div>
    </div>
  )
}

// 화면 1: 빈 화면 + "+"로 과목을 추가하고, 추가와 동시에 학점/흥미도까지 입력하는 통합 화면
function CourseBuilder({ onAnalyze, isAnalyzing = false, analyzeError = '' }) {
  const [entries, setEntries] = useState([])
  const [isSearchOpen, setSearchOpen] = useState(false)

  const excludeCodes = new Set(entries.map((e) => e.course_code))

  const addCourse = (course) => {
    setEntries((prev) => [
      ...prev,
      { ...course, interest_score: 0, grade: 'A+' },
    ])
    setSearchOpen(false)
  }

  const removeCourse = (course_code) => {
    setEntries((prev) => prev.filter((e) => e.course_code !== course_code))
  }

  const updateInterestScore = (course_code, score) => {
    setEntries((prev) =>
      prev.map((e) =>
        e.course_code === course_code ? { ...e, interest_score: score } : e
      )
    )
  }

  const updateGrade = (course_code, grade) => {
    setEntries((prev) =>
      prev.map((e) => (e.course_code === course_code ? { ...e, grade } : e))
    )
  }

  const handleAnalyze = () => {
    const requestBody = {
      courses: entries.map(({ course_code, interest_score, grade }) => ({
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
    <div className="course-builder">
      <h1>수강한 과목을 추가해주세요</h1>
      <p className="builder-subtitle">
        과목을 추가하면서 흥미도와 학점을 함께 입력해주세요
      </p>

      {entries.length === 0 && (
        <p className="empty-hint-text">아직 추가한 과목이 없어요</p>
      )}

      <div className="course-card-list">
        {entries.map((course, index) => (
          <div className="course-card" key={course.course_code}>
            <button
              type="button"
              className="card-remove"
              onClick={() => removeCourse(course.course_code)}
              aria-label="삭제"
            >
              ✕
            </button>

            <div className="card-badges">
              <span className="badge badge-code">{course.course_code}</span>
            </div>

            <h2 className="card-title">{course.course_name}</h2>

            <div className="card-stats">
              <div className="stat-cell">
                <div className="stat-value stat-stars">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <span
                      key={star}
                      className={
                        star <= course.interest_score
                          ? 'stat-star filled'
                          : 'stat-star'
                      }
                      onClick={() =>
                        updateInterestScore(course.course_code, star)
                      }
                    >
                      ★
                    </span>
                  ))}
                </div>
                <span className="stat-label">흥미도</span>
              </div>

              <div className="stat-cell">
                <select
                  className="stat-value stat-select"
                  value={course.grade}
                  onChange={(e) =>
                    updateGrade(course.course_code, e.target.value)
                  }
                >
                  {GRADES.map((grade) => (
                    <option key={grade} value={grade}>
                      {grade}
                    </option>
                  ))}
                </select>
                <span className="stat-label">학점</span>
              </div>

              <div className="stat-cell">
                <span className="stat-value">{index + 1}</span>
                <span className="stat-label">순서</span>
              </div>
            </div>

            <div className="card-progress">
              <div
                className="card-progress-fill"
                style={{ width: `${(course.interest_score / 5) * 100}%` }}
              />
            </div>
          </div>
        ))}

        <button
          type="button"
          className="add-tile"
          onClick={() => setSearchOpen(true)}
          aria-label="과목 추가"
        >
          <span className="add-tile-icon">+</span>
          <span className="add-tile-text">과목 추가</span>
        </button>
      </div>

      {entries.length > 0 && (
        <button type="button" className="analyze-btn" onClick={handleAnalyze} disabled={isAnalyzing}>
          {isAnalyzing ? '분석 중...' : '분석하기'}
        </button>
      )}

      {analyzeError && <p className="analyze-error" role="alert">{analyzeError}</p>}

      {isSearchOpen && (
        <CourseSearchOverlay
          excludeCodes={excludeCodes}
          onAdd={addCourse}
          onClose={() => setSearchOpen(false)}
        />
      )}
    </div>
  )
}

export default CourseBuilder
