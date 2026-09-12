import { useState } from 'react'

// 점수(0~100)를 가로 막대바로 시각화하는 표시용 컴포넌트
function ScoreBar({ score }) {
  return (
    <div className="score-bar-track">
      <div className="score-bar-fill" style={{ width: `${score}%` }} />
    </div>
  )
}

// 화면 3의 카드 한 장 (순위 / 분야명 / 점수 막대바)
function FieldRankingCard({ rank, field, onClick }) {
  return (
    <div className="field-card" onClick={onClick}>
      <div className="field-rank">#{rank}</div>
      <h2>{field.field_name}</h2>
      <ScoreBar score={field.score} />
      <p className="field-score">{field.score}점</p>
    </div>
  )
}

// 화면 4: 선택한 Field 상세
function FieldDetail({ field, onBack }) {
  return (
    <div className="field-detail">
      <button type="button" onClick={onBack}>
        ← 목록으로
      </button>

      <h1>{field.field_name}</h1>

      <section>
        <h2>왜 추천되었나요?</h2>
        <p>{field.reason}</p>
      </section>

      <section>
        <h2>추천 과목</h2>
        <ul>
          {field.recommended_courses.map((course) => (
            <li key={course.course_code}>
              {course.course_name} ({course.course_code})
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>관련 직무</h2>
        <div className="career-tags">
          {field.careers.map((career) => (
            <span className="tag" key={career}>
              {career}
            </span>
          ))}
        </div>
      </section>

      <section>
        <h2>관련 연구실</h2>
        <div className="lab-list">
          {field.labs.map((lab) => (
            <div className="lab-card" key={lab.lab_name}>
              <p className="lab-name">{lab.lab_name}</p>
              <p className="lab-professor">지도교수: {lab.professor}</p>
              <a href={lab.lab_url} target="_blank" rel="noreferrer">
                연구실 바로가기
              </a>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2>Career Roadmap</h2>
        <ul className="roadmap-list">
          {field.roadmap.taken.map((item) => (
            <li key={`taken-${item}`}>✅ {item}</li>
          ))}
          {field.roadmap.next.map((item) => (
            <li key={`next-${item}`}>🔜 {item}</li>
          ))}
          <li>🎯 {field.roadmap.goal}</li>
        </ul>
      </section>
    </div>
  )
}

// 화면 3(분석 결과 TOP 3) + 화면 4(선택한 Field 상세)를 함께 다루는 결과 페이지
// topFields 데이터는 전부 props로만 받는다 -> 나중에 mockResponse 대신 실제
// API 응답을 넘겨도 이 컴포넌트는 수정할 필요가 없다.
function ResultPage({ topFields }) {
  const [selectedField, setSelectedField] = useState(null)

  if (selectedField) {
    return (
      <FieldDetail
        field={selectedField}
        onBack={() => setSelectedField(null)}
      />
    )
  }

  return (
    <div className="result-page">
      <h1>분석 결과 - 추천 진로 TOP 3</h1>

      <div className="field-card-list">
        {topFields.map((field, index) => (
          <FieldRankingCard
            key={field.field_id}
            rank={index + 1}
            field={field}
            onClick={() => setSelectedField(field)}
          />
        ))}
      </div>
    </div>
  )
}

export default ResultPage
