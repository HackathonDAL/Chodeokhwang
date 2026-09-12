import { useEffect, useState } from 'react'
import CompassPinLogo from './CompassPinLogo'

// 서비스 이름 "어디고?" - 통통한 3D 풍선 느낌 글자가 하나씩 팝업되며
// 나타난 뒤 둥실둥실 떠다니는 모션으로 계속 움직인다.
// 색상은 프로젝트 파스텔 팔레트 그대로 사용한다.
const WORD = [
  { ch: '어', from: '#d9fbf1', base: '#7dd8c0', to: '#4fae95' }, // mint
  { ch: '디', from: '#ede9fe', base: '#c4b5fd', to: '#a78bfa' }, // purple
  { ch: '고', from: '#fdf2f8', base: '#f9a8d4', to: '#f472b6' }, // pink
  { ch: '?', from: '#eff6ff', base: '#93c5fd', to: '#60a5fa' }, // sky
]

const POP_STAGGER = 130 // ms, 글자마다 팝업 시작 시점 차이
const POP_DURATION = 550 // ms, 글자 하나가 팝업되는 데 걸리는 시간
// 로고(핀 낙하 + 나침반 정렬)가 먼저 재생된 뒤에 글자가 나타나도록
// 모든 글자 애니메이션에 공통으로 더하는 시작 지연.
const WORD_BASE_DELAY = 750 // ms

function SplashIntro({ onStart }) {
  const [showCta, setShowCta] = useState(false)

  useEffect(() => {
    const totalMs =
      WORD_BASE_DELAY + (WORD.length - 1) * POP_STAGGER + POP_DURATION
    const timer = setTimeout(() => setShowCta(true), totalMs + 250)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="splash-intro">
      <div className="splash-blobs" aria-hidden="true">
        <span className="splash-blob blob-mint" />
        <span className="splash-blob blob-purple" />
        <span className="splash-blob blob-pink" />
        <span className="splash-blob blob-pink2" />
      </div>

      <div className="splash-logo-wrap">
        <CompassPinLogo size={88} className="splash-logo" />
        <span className="splash-logo-shadow" />
      </div>

      <div className="splash-word">
        {WORD.map((item, charIndex) => (
          <span
            className="bubble-float"
            key={charIndex}
            style={{
              '--float-duration': `${3 + (charIndex % 3) * 0.4}s`,
              '--float-delay': `${charIndex * 0.3}s`,
              '--float-rot': `${charIndex % 2 === 0 ? 3 : -3}deg`,
            }}
          >
            <span
              className="bubble-pop"
              style={{
                '--pop-delay': `${WORD_BASE_DELAY + charIndex * POP_STAGGER}ms`,
                // background(shorthand)을 쓰면 background-clip이 border-box로
                // 초기화돼 글자 모양대로 안 잘린다. backgroundImage(longhand)로 설정.
                backgroundImage: `linear-gradient(180deg, ${item.from} 0%, ${item.base} 55%, ${item.to} 100%)`,
                // 글자를 더 통통해 보이게 테두리를 살짝 두껍게(같은 계열 진한 색)
                WebkitTextStroke: `3px ${item.to}`,
              }}
            >
              {item.ch}
            </span>
          </span>
        ))}
      </div>

      <p className={`splash-subtitle${showCta ? ' visible' : ''}`}>
        당신의 진로를 찾아드립니다
      </p>

      <button
        type="button"
        className={`splash-cta${showCta ? ' visible' : ''}`}
        onClick={onStart}
      >
        시작하기
      </button>
    </div>
  )
}

export default SplashIntro
