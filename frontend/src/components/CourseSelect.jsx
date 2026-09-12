import { useState } from 'react'
import { courses } from '../mock/courses'

function CourseSelect({ onNext }) {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCourses, setSelectedCourses] = useState([])

  const filteredCourses = courses.filter((course) =>
    course.course_name.includes(searchTerm)
  )

  const isSelected = (course) =>
    selectedCourses.some((c) => c.course_code === course.course_code)

  const toggleCourse = (course) => {
    setSelectedCourses((prev) =>
      isSelected(course)
        ? prev.filter((c) => c.course_code !== course.course_code)
        : [...prev, course]
    )
  }

  const handleNext = () => {
    console.log('선택한 과목 목록:', selectedCourses)
    onNext?.(selectedCourses)
  }

  return (
    <div className="course-select">
      <h1>수강한 과목을 선택해주세요</h1>

      <input
        type="text"
        placeholder="과목 이름으로 검색"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="course-search"
      />

      <ul className="course-list">
        {filteredCourses.map((course) => (
          <li key={course.course_code}>
            <label>
              <input
                type="checkbox"
                checked={isSelected(course)}
                onChange={() => toggleCourse(course)}
              />
              {course.course_name} ({course.department}) · {course.course_code}
            </label>
          </li>
        ))}
        {filteredCourses.length === 0 && <li>검색 결과가 없습니다.</li>}
      </ul>

      <p>선택한 과목 수: {selectedCourses.length}개</p>

      <button type="button" onClick={handleNext}>
        다음
      </button>
    </div>
  )
}

export default CourseSelect
