import { useState } from 'react'
import './App.css'
import SplashIntro from './components/SplashIntro'
import IntroScreen from './components/IntroScreen'
import CourseBuilder from './components/CourseBuilder'
import ResultPage from './components/ResultPage'
import { mockResponse } from './mock/mockResponse'
import { withViewTransition } from './utils/viewTransition'

function App() {
  // 생성형 AI 캐릭터를 쓴 인트로 화면(IntroScreen)은 보류 상태라 기본
  // 흐름에서는 건너뛴다. 다시 쓰게 되면 SplashIntro 다음 단계를 'intro'로
  // 바꾸면 된다.
  const [step, setStep] = useState('splash') // 'splash' | 'intro' | 'build' | 'result'

  // 화면(step)이 바뀔 때 부드러운 크로스페이드로 전환되도록 감싼 setter.
  const goToStep = (next) => withViewTransition(() => setStep(next))

  const handleAnalyze = (requestBody) => {
    // TODO: 백엔드 연동 시 requestBody로 API를 호출하고,
    // 그 응답의 top_fields를 ResultPage에 props로 넘기면 된다.
    // 지금은 백엔드가 없으므로 mockResponse를 결과로 사용한다.
    console.log('분석 요청 데이터:', requestBody)
    goToStep('result')
  }

  return (
    <>
      {step === 'splash' && <SplashIntro onStart={() => goToStep('build')} />}
      {step === 'intro' && <IntroScreen onStart={() => goToStep('build')} />}
      {step === 'build' && <CourseBuilder onAnalyze={handleAnalyze} />}
      {step === 'result' && <ResultPage topFields={mockResponse.top_fields} />}
    </>
  )
}

export default App
