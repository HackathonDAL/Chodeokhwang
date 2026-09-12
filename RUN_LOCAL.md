# Soadal 로컬 통합 테스트

저장소 루트(backend, frontend, data가 보이는 폴더)에서 PowerShell을 여세요.
이미 실행 중인 이전 데모 서버는 각각 Ctrl+C로 종료하세요.

## 최초 설치
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd frontend
npm.cmd ci
cd ..
```

## 백엔드 (첫 번째 터미널)
```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
http://127.0.0.1:8000/health 에서 응답을 확인하세요.

## 프론트 (루트에서 새 터미널)
```powershell
cd frontend
npm.cmd run dev -- --port 5173 --strictPort
```
http://localhost:5173 에 접속하세요. 두 서버를 모두 켜두어야 합니다.
포트가 사용 중이면 이전 프론트 서버를 종료하세요. 다른 포트를 쓰려면 백엔드의 CORS_ORIGINS에도 해당 출처를 추가해야 합니다.

## 검증
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
cd frontend
npm.cmd run build
```

## API 변경
- POST /api/analyze: top_fields 및 unexplored_fields를 함께 반환합니다.
- unexplored_fields 항목: field_id, field_name, field_name_kr, reason, representative_course.
- representative_course 항목: course_code, course_name, department, why.
- 추천 분야가 없어도 미탐색 분야를 표시합니다. 빈 미탐색 목록에는 안내를 표시합니다.
- POST /api/unexplored는 기존 독립 조회용 응답 형식을 유지합니다.
- 대표 과목은 data/RepresentSubject.csv를 사용합니다.
- explore_courses는 추천 분야 내 미수강 과목으로, 전체 미탐색 분야와 구분합니다.
- 자연어 설명은 기본적으로 규칙 기반입니다. 직업/로드맵은 검토가 필요한 초안이며 연구실 목록은 빈 배열입니다.
- 분야 점수는 적성 확률이 아닙니다. 미탐색 판정은 입력 과목과 CSV 연관도(0.3 기준)에 의존하며 실제 강의 내용을 확인한 결과가 아닙니다.

샘플: STAT221 B+ 흥미도 3, STAT342 A+ 흥미도 4, COSE213 A+ 흥미도 3, COSE361 A+ 흥미도 5.
추천: ML 86.14, Algorithms 83.93, DS 82.69.
미탐색: Computer_Architecture, Embedded_Systems, HCI (각 대표 과목 1개).

이 문서의 API 확장 사항은 기존 docs/RESULT_API_SPEC.md에 추가되는 내용입니다.
