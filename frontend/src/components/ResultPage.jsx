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
    <button type="button" className="field-card" onClick={onClick}>
      <div className="field-rank">#{rank}</div>
      <h2>{field.field_name}</h2>
      <p className="field-name-kr">{field.field_name_kr}</p>
      <ScoreBar score={field.score} />
      <p className="field-score">적합도 {field.score}점</p>
    </button>
  )
}

// 화면 4: 선택한 Field 상세
// - 왜 추천되었는지(AI 자연어 설명)
// - 커리어 로드맵(직종 + 단계별 계획)
// - 추천 근거가 충분한 과목
// - 아직 탐색해보지 않은 분야의 과목
// - 관련 연구실
function FieldDetail({ field, onBack }) {
  return (
    <div className="field-detail">
      <button type="button" className="back-btn" onClick={onBack}>
        ← 목록으로
      </button>

      <div className="field-detail-header">
        <span className="field-detail-score">적합도 {field.score}점</span>
        <h1>{field.field_name}</h1>
        <p className="field-name-kr">{field.field_name_kr}</p>
      </div>

      <section className="detail-section">
        <h2 className="section-title">왜 이 분야가 추천되었을까요?</h2>
        <div className="ai-reason-card">
          <span className="ai-badge">AI 분석</span>
          <p>{field.ai_reason}</p>
        </div>
      </section>

      <section className="detail-section">
        <h2 className="section-title">커리어 로드맵</h2>
        <div className="career-tags">
          {field.career_roadmap.roles.map((role) => (
            <span className="tag" key={role}>
              {role}
            </span>
          ))}
        </div>
        <ol className="roadmap-timeline">
          {field.career_roadmap.stages.map((step, index) => (
            <li key={step.stage}>
              <span className="roadmap-dot">{index + 1}</span>
              <div>
                <p className="roadmap-stage">{step.stage}</p>
                <p className="roadmap-milestone">{step.milestone}</p>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <section className="detail-section">
        <h2 className="section-title">추천 근거가 충분한 과목</h2>
        <div className="evidence-course-list">
          {field.evidence_courses.map((course) => (
            <div className="evidence-course-card" key={course.course_code}>
              <div className="evidence-course-head">
                <h3>{course.course_name}</h3>
                <span className="evidence-grade">{course.grade}</span>
              </div>
              <p className="evidence-code">{course.course_code}</p>
              <div className="evidence-interest">
                {[1, 2, 3, 4, 5].map((star) => (
                  <span
                    key={star}
                    className={
                      star <= course.interest_score ? 'mini-star filled' : 'mini-star'
                    }
                  >
                    ★
                  </span>
                ))}
              </div>
              <p className="evidence-contribution">{course.contribution}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="detail-section">
        <h2 className="section-title">이 추천 분야에서 더 배워볼 미수강 과목</h2>
        <div className="explore-course-list">
          {field.explore_courses.map((course) => (
            <div className="explore-course-card" key={course.course_code}>
              <div className="card-badges">
                <span className="badge badge-dept">{course.department}</span>
                <span className="badge badge-code">{course.course_code}</span>
              </div>
              <h3>{course.course_name}</h3>
              <p className="explore-why">{course.why}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="detail-section">
        <h2 className="section-title">관련 연구실</h2>
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
    </div>
  )
}

// 화면 3(분석 결과 TOP 3) + 화면 4(선택한 Field 상세)를 함께 다루는 결과 페이지
// topFields 데이터는 전부 props로만 받는다 -> 나중에 mockResponse 대신 실제
// API 응답을 넘겨도 이 컴포넌트는 수정할 필요가 없다.
// 응답 형식은 docs/RESULT_API_SPEC.md 참고.
function ResultPage({ topFields, unexploredFields = [], onRestart }) {
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
      <button type="button" className="back-btn" onClick={onRestart}>
        ← 과목 다시 입력하기
      </button>
      <h1>분석 결과 - 추천 진로 TOP 3</h1>
      <p className="builder-subtitle">
        가장 적성에 맞는 분야를 확인하고, 자세한 커리어 로드맵을 살펴보세요
      </p>

      <div className="field-card-list">
        {topFields.length === 0 && <p>현재는 추천 근거가 충분한 분야가 없어요. 아래 분야부터 탐색해보세요.</p>}
        {topFields.map((field, index) => (
          <FieldRankingCard
            key={field.field_id}
            rank={index + 1}
            field={field}
            onClick={() => setSelectedField(field)}
          />
        ))}
      </div>
      <section className="detail-section unexplored-section" aria-labelledby="unexplored-heading">
        <h2 id="unexplored-heading" className="section-title">아직 탐색하지 않은 분야 ({unexploredFields.length})</h2>
        <p>적성이 낮다는 뜻이 아니라, 입력한 수강 경험만으로는 아직 판단하기 어려운 분야예요. 분야별 대표 과목을 하나씩 소개합니다.</p>
        {unexploredFields.length === 0 ? (
          <p role="status">현재 기준에서 미탐색으로 분류된 분야가 없어요. 모든 분야를 충분히 경험했다는 뜻은 아닙니다.</p>
        ) : (
          <div className="unexplored-grid">
            {unexploredFields.map((field) => (
              <article className="explore-course-card" key={field.field_id}>
                <h3>{field.field_name_kr}</h3>
                <p>{field.field_name}</p>
                <p className="explore-why">{field.reason}</p>
                <h4>대표 과목 · {field.representative_course.course_name}</h4>
                <div className="card-badges">
                  <span className="badge badge-code">{field.representative_course.course_code}</span>
                  <span className="badge badge-dept">{field.representative_course.department}</span>
                </div>
                <p className="explore-why">{field.representative_course.why}</p>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}

export default ResultPage
