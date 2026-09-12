import { useState } from 'react'
import './App.css'
import CourseSelect from './components/CourseSelect'
import CourseEvaluate from './components/CourseEvaluate'
import ResultPage from './components/ResultPage'
import { mockResponse } from './mock/mockResponse'

function App() {
  const [step, setStep] = useState('select') // 'select' | 'evaluate' | 'result'
  const [selectedCourses, setSelectedCourses] = useState([])

  const handleSelectNext = (courses) => {
    setSelectedCourses(courses)
    setStep('evaluate')
  }

  const handleAnalyze = (requestBody) => {
    // TODO: 백엔드 연동 시 requestBody로 API를 호출하고,
    // 그 응답의 top_fields를 ResultPage에 props로 넘기면 된다.
    // 지금은 백엔드가 없으므로 mockResponse를 결과로 사용한다.
    console.log('분석 요청 데이터:', requestBody)
    setStep('result')
  }

  return (
    <>
      {step === 'select' && <CourseSelect onNext={handleSelectNext} />}
      {step === 'evaluate' && (
        <CourseEvaluate
          selectedCourses={selectedCourses}
          onAnalyze={handleAnalyze}
        />
      )}
      {step === 'result' && <ResultPage topFields={mockResponse.top_fields} />}
    </>
  )
}

export default App
