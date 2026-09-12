# 정보보안 데모: 초기 관심 추천 보완

기준 파일: Soadal-infosec-demo.zip. 프론트 화면 및 API 응답 형식은 원본을 유지했습니다.

변경 내용
- 직접 관련 과목에서 흥미도 4 이상, 과목 평가 기준을 충족하면 초기 관심 후보로 허용합니다.
- 기존의 충분한 근거 기준과 분야 점수 기준(0.6), 상위 3개 제한은 유지합니다.
- 분야 점수는 기존처럼 전체 관련 과목의 연관도 가중평균, 흥미 80%/학점 20%입니다.
- 한 과목뿐이라는 이유로 추천 자격을 잃지 않습니다. 다른 분야보다 점수가 낮으면 상위 3개에 들지 않을 수 있습니다.
- 초기 후보의 추천 이유에는 경험이 적다는 설명을 붙입니다.
- 선형대수·확률 기초·인공지능 개론 등의 타 분야 연결 28개를 간접 연결로 보수적으로 조정했습니다.
  data/relevance_changes.csv에 이전 값, 변경 값, 이유를 기록했습니다.
- 기초 연결은 0.4 이하로 두어 직접 탐색 근거로 과대 해석되지 않게 했습니다.
- 강의계획서를 전수 검증한 값은 아닙니다. 포괄적인 응용·프로젝트 과목은 강의 내용에 따라 추가 검토가 필요합니다.
- RepresentSubject.csv와 과목 목록의 일관성을 검증했습니다.

실행 방법
기존 서버를 Ctrl+C로 종료하고 새 폴더에서 PowerShell을 엽니다.

최초 설치:
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd frontend
npm.cmd ci
cd ..
```
백엔드:
```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
새 PowerShell 창을 이 폴더에서 열어 프론트 실행:
```powershell
cd frontend
npm.cmd run dev -- --port 5173 --strictPort
```
http://localhost:5173 에 접속합니다.

테스트:
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
