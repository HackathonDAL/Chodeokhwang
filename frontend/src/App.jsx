import { useState } from 'react'
import './App.css'
import IntroScreen from './components/IntroScreen'
import CourseBuilder from './components/CourseBuilder'
import ResultPage from './components/ResultPage'
import { mockResponse } from './mock/mockResponse'

function App() {
  // 생성형 AI 캐릭터를 쓴 인트로 화면은 보류 상태라 기본값에서는 건너뛴다.
  // 다시 쓰게 되면 초기값을 'intro'로만 되돌리면 된다.
  const [step, setStep] = useState('build') // 'intro' | 'build' | 'result'

  const handleAnalyze = (requestBody) => {
    // TODO: 백엔드 연동 시 requestBody로 API를 호출하고,
    // 그 응답의 top_fields를 ResultPage에 props로 넘기면 된다.
    // 지금은 백엔드가 없으므로 mockResponse를 결과로 사용한다.
    console.log('분석 요청 데이터:', requestBody)
    setStep('result')
  }

  return (
    <>
      {step === 'intro' && <IntroScreen onStart={() => setStep('build')} />}
      {step === 'build' && <CourseBuilder onAnalyze={handleAnalyze} />}
      {step === 'result' && <ResultPage topFields={mockResponse.top_fields} />}
    </>
  )
}

export default App
