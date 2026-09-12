import { useState } from 'react'
import './App.css'
import SplashIntro from './components/SplashIntro'
import CourseBuilder from './components/CourseBuilder'
import ResultPage from './components/ResultPage'
import { withViewTransition } from './utils/viewTransition'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'https://kucompass.onrender.com'

function App() {
  const [step, setStep] = useState('splash') // 'splash' | 'build' | 'result'
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // 화면(step)이 바뀔 때 부드러운 크로스페이드로 전환되도록 감싼 setter.
  const goToStep = (next) => withViewTransition(() => setStep(next))

  const handleAnalyze = async (requestBody) => {
    setLoading(true)
    setError('')
    try {
      const response = await fetch(`${API_BASE_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
      })
      const data = await response.json().catch(() => null)
      if (!response.ok) {
        const detail = data?.detail
        throw new Error(
          typeof detail === 'string'
            ? detail
            : (detail?.message ?? '입력값 또는 백엔드 데이터를 확인해주세요.')
        )
      }
      if (
        !Array.isArray(data?.top_fields) ||
        !Array.isArray(data?.unexplored_fields)
      ) {
        throw new Error(
          '새 데모의 백엔드를 실행해주세요. 응답에 미탐색 분야 정보가 없습니다.'
        )
      }
      setResult(data)
      goToStep('result')
    } catch (requestError) {
      setError(
        requestError instanceof TypeError
          ? '백엔드 서버에 연결할 수 없습니다. 백엔드가 8000번 포트에서 실행 중인지 확인해주세요.'
          : requestError.message
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {step === 'splash' && <SplashIntro onStart={() => goToStep('build')} />}
      {step === 'build' && (
        <CourseBuilder
          onAnalyze={handleAnalyze}
          isAnalyzing={loading}
          analyzeError={error}
        />
      )}
      {step === 'result' && result && (
        <ResultPage
          topFields={result.top_fields}
          unexploredFields={result.unexplored_fields}
          onRestart={() => {
            setResult(null)
            setError('')
            goToStep('build')
          }}
        />
      )}
    </>
  )
}

export default App
