import professorImg from '../assets/professor.png'

// 화면 0: 사주풀이 스타일의 인트로 화면
// AI 교수님 캐릭터 + 말풍선(운명 문구 일부 블러 처리)으로 호기심을 유발한 뒤
// 버튼을 누르면 실제 과목 입력 화면(CourseBuilder)으로 넘어간다.
function IntroScreen({ onStart }) {
  return (
    <div className="intro-screen">
      <img
        src={professorImg}
        alt="정보대학 AI 교수 캐릭터"
        className="professor-bg"
      />
      <div className="intro-overlay" aria-hidden="true" />

      <div className="intro-sparkles" aria-hidden="true">
        <span>✦</span>
        <span>✧</span>
        <span>✦</span>
        <span>✧</span>
      </div>

      <div className="intro-content">
        <div className="speech-bubble">
          <p>
            자네는{' '}
            <span className="fate-blur" aria-label="가려진 운명 문구">
              블러 처리된 운명 문구
            </span>
            할 운명이야
          </p>
        </div>

        <button type="button" className="intro-cta" onClick={onStart}>
          나의 진로 알아보기
        </button>
      </div>
    </div>
  )
}

export default IntroScreen
