// 어디고 로고: 지도 핀(pin) 실루엣 안에 나침반 바늘(compass needle)을 결합한
// 미니멀 플랫 아이콘. 메인 컬러는 크림슨 레드(#8A1538).
function CompassPinLogo({ size = 96, className = '' }) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 100 120"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label="어디고 로고"
    >
      {/* 지도 핀 실루엣 */}
      <path
        d="M50,10 C72,10 88,28 88,50 C88,78 60,105 50,118 C40,105 12,78 12,50 C12,28 28,10 50,10 Z"
        fill="#8A1538"
      />

      {/* 핀 안쪽 원 (나침반이 들어갈 자리) */}
      <circle cx="50" cy="48" r="24" fill="#ffffff" />

      {/* 나침반 바늘: 위쪽(N)은 진한 크림슨, 아래쪽(S)은 흰 바탕에 크림슨 테두리 */}
      <g className="logo-needle" style={{ transformOrigin: '50px 48px' }}>
        <path d="M50,26 L60,48 L50,48 Z" fill="#8A1538" />
        <path d="M50,26 L40,48 L50,48 Z" fill="#c23859" />
        <path
          d="M50,70 L60,48 L50,48 Z"
          fill="#ffffff"
          stroke="#8A1538"
          strokeWidth="2"
          strokeLinejoin="round"
        />
        <path
          d="M50,70 L40,48 L50,48 Z"
          fill="#ffffff"
          stroke="#8A1538"
          strokeWidth="2"
          strokeLinejoin="round"
        />
        <circle cx="50" cy="48" r="4" fill="#8A1538" />
      </g>
    </svg>
  )
}

export default CompassPinLogo
