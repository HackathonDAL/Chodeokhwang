"""표시명과 직종 예시 초안. 채용 전망/자격/취업 보장을 의미하지 않는다."""
CATALOG = {
    "ML": ("Machine Learning", "머신러닝", ["ML Engineer", "AI Researcher", "Data Scientist"]),
    "DS": ("Data Science", "데이터과학", ["Data Scientist", "Data Analyst", "Analytics Engineer"]),
    "Statistics": ("Statistics", "통계학", ["Statistician", "Data Analyst", "Biostatistician"]),
    "Computer_Vision": ("Computer Vision", "컴퓨터 비전", ["Computer Vision Engineer", "Vision Researcher", "Image Processing Engineer"]),
    "NLP": ("Natural Language Processing", "자연어처리", ["NLP Engineer", "NLP Researcher", "Search Engineer"]),
    "Software_Engineering": ("Software Engineering", "소프트웨어공학", ["Software Engineer", "Backend Engineer", "QA Engineer"]),
    "Algorithms": ("Algorithms", "알고리즘", ["Algorithm Engineer", "Software Engineer", "Algorithms Researcher"]),
    "HCI": ("Human-Computer Interaction", "인간컴퓨터상호작용", ["UX Researcher", "Interaction Designer", "HCI Researcher"]),
    "Optimization": ("Optimization", "최적화", ["Optimization Engineer", "Operations Research Analyst", "Optimization Researcher"]),
    "infoSec": ("Information Security", "정보보안", ["보안 엔지니어", "보안 분석가", "보안 연구원"]),
    "Computer_Architecture": ("Computer Architecture", "컴퓨터구조", ["CPU Design Engineer", "Hardware Engineer", "Computer Architecture Researcher"]),
    "Embedded_Systems": ("Embedded Systems", "임베디드시스템", ["Embedded Software Engineer", "Firmware Engineer", "IoT Engineer"]),
    "Robotics": ("Robotics", "로봇공학", ["Robotics Engineer", "Robot Software Engineer", "Robotics Researcher"]),
    "Computer_Systems": ("Computer Systems", "컴퓨터시스템", ["Systems Software Engineer", "Platform Engineer", "Systems Researcher"]),
    "Cognitive_Science": ("Cognitive Science", "인지과학", ["Cognitive Science Researcher", "UX Researcher", "Human Factors Researcher"]),
    "Applied_Mathematics": ("Applied Mathematics", "응용수학", ["Mathematical Modeler", "Simulation Engineer", "Applied Mathematics Researcher"]),
}
CATALOG["Apllied_Mathematics"] = CATALOG["Applied_Mathematics"]

FIELD_DESCRIPTIONS = {
    "ML": "데이터에서 패턴을 학습해 새로운 상황을 예측하거나 판단하는 방법을 연구해요. 추천 서비스와 예측 모델 같은 지능형 시스템을 만들어요.",
    "DS": "데이터를 수집하고 분석해 질문에 답하고 의사결정을 돕는 분야예요. 통계와 프로그래밍을 함께 활용해 현상을 이해해요.",
    "Statistics": "불확실한 현상을 데이터로 이해하고, 표본을 통해 전체의 특성을 추론하는 분야예요. 실험 설계와 분석 결과의 신뢰성을 다뤄요.",
    "Computer_Vision": "컴퓨터가 사진과 영상 속 사물이나 공간을 이해하도록 만드는 분야예요. 이미지 인식과 영상 분석 등을 다뤄요.",
    "NLP": "컴퓨터가 사람의 언어를 이해하고 생성하도록 만드는 분야예요. 번역, 검색, 대화 시스템 같은 기술을 다뤄요.",
    "Software_Engineering": "소프트웨어를 체계적으로 설계하고 개발하며 유지하는 방법을 배우는 분야예요. 협업, 테스트, 서비스 품질을 함께 고민해요.",
    "Algorithms": "문제를 해결하는 절차를 설계하고 얼마나 효율적인지 분석하는 분야예요. 탐색과 정렬 등 다양한 계산 문제를 다뤄요.",
    "HCI": "사람이 컴퓨터와 서비스를 쉽고 편리하게 사용할 수 있도록 연구하는 분야예요. 사용자의 행동과 필요를 이해하고 인터페이스를 설계·평가해요.",
    "Optimization": "주어진 조건에서 가장 적절한 선택을 찾는 방법을 연구해요. 자원 배분, 일정 계획, 모델 학습 등 다양한 문제에 활용돼요.",
    "infoSec": "정보와 시스템을 안전하게 보호하는 방법을 배우는 분야예요. 소프트웨어와 네트워크의 취약점을 이해하고, 공격을 예방하거나 탐지·대응하는 기술을 다뤄요.",
    "Computer_Architecture": "프로세서와 메모리 등 컴퓨터 내부 장치가 어떻게 구성되고 협력하는지 배우는 분야예요. 명령을 실행하는 구조와 성능을 높이는 설계 방법을 다뤄요.",
    "Embedded_Systems": "가전, 자동차, 센서처럼 특정 기능을 수행하는 기기 안의 컴퓨터를 다뤄요. 하드웨어와 소프트웨어를 연결해 기기가 주변 환경에 반응하도록 만들어요.",
    "Robotics": "로봇이 주변을 감지하고 움직임을 계획하며 행동하도록 만드는 분야예요. 센서, 제어, 인공지능을 함께 활용해요.",
    "Computer_Systems": "운영체제와 시스템 소프트웨어가 컴퓨터 자원을 관리하고 프로그램을 실행하는 원리를 배워요. 안정적이고 효율적인 실행 환경을 다뤄요.",
    "Cognitive_Science": "사람이 지각하고 배우며 기억하고 판단하는 과정을 탐구해요. 심리학과 컴퓨터과학 등 여러 관점에서 마음과 지능을 이해해요.",
    "Applied_Mathematics": "현실의 문제를 수학적 모델로 표현하고 해결하는 분야예요. 자연현상과 공학 문제를 분석하거나 시뮬레이션하는 방법을 다뤄요.",
}
FIELD_DESCRIPTIONS["Apllied_Mathematics"] = FIELD_DESCRIPTIONS["Applied_Mathematics"]

# 일반적인 업무 소개. 분야별 편집 문구로 제공한다.
CAREER_DESCRIPTIONS = {'ML': [{'title': '머신러닝 엔지니어', 'description': '데이터로 예측·분류 모델을 학습시키고, 서비스에 적용한 뒤 성능을 개선해요.'}, {'title': 'AI 연구원', 'description': '새로운 학습 방법과 모델을 설계하고 실험으로 효과를 확인해요.'}, {'title': '데이터 사이언티스트', 'description': '데이터 분석과 예측 모델을 활용해 서비스나 사업의 문제 해결을 도와요.'}], 'DS': [{'title': '데이터 사이언티스트', 'description': '데이터에서 패턴을 찾고 통계·머신러닝 모델로 문제를 분석해요.'}, {'title': '데이터 분석가', 'description': '사용자 행동과 서비스 지표를 분석하고 의사결정에 필요한 근거를 전달해요.'}, {'title': '애널리틱스 엔지니어', 'description': '분석에 쓰이는 데이터를 정리하고 일관된 지표와 데이터 모델을 관리해요.'}], 'Statistics': [{'title': '통계 분석가', 'description': '조사와 실험을 설계하고 데이터의 불확실성을 고려해 결과를 해석해요.'}, {'title': '데이터 분석가', 'description': '데이터를 비교하고 가설을 검토해 현상을 설명하는 근거를 찾아요.'}, {'title': '생물통계 연구원', 'description': '생명과학·의료 연구의 데이터를 분석하고 연구 결과의 통계적 타당성을 살펴봐요.'}], 'Computer_Vision': [{'title': '컴퓨터 비전 엔지니어', 'description': '사진과 영상에서 사물이나 움직임을 인식하는 모델을 개발해요.'}, {'title': '비전 연구원', 'description': '영상과 공간을 이해하는 새로운 방법을 연구하고 실험해요.'}, {'title': '영상처리 엔지니어', 'description': '영상의 잡음을 줄이거나 특징을 추출해 영상 품질과 활용성을 높여요.'}], 'NLP': [{'title': '자연어처리 엔지니어', 'description': '문서 분석·번역·대화 기능처럼 사람의 언어를 다루는 모델과 서비스를 개발해요.'}, {'title': '자연어처리 연구원', 'description': '언어를 이해하고 생성하는 모델의 학습 방법과 평가 방법을 연구해요.'}, {'title': '검색 엔지니어', 'description': '사용자의 질문에 맞는 문서를 찾고 검색 결과의 순서와 품질을 개선해요.'}], 'Software_Engineering': [{'title': '소프트웨어 개발자', 'description': '요구사항에 맞춰 프로그램을 설계·구현하고 테스트하며 유지보수해요.'}, {'title': '백엔드 개발자', 'description': '서버의 기능과 데이터 처리 구조를 만들고 서비스가 안정적으로 작동하도록 관리해요.'}, {'title': '소프트웨어 품질 엔지니어', 'description': '테스트를 설계하고 자동화해 오류를 찾고 소프트웨어 품질을 개선해요.'}], 'Algorithms': [{'title': '알고리즘 개발자', 'description': '주어진 문제에 맞는 계산 절차를 설계하고 실행 시간과 메모리 사용을 개선해요.'}, {'title': '소프트웨어 개발자', 'description': '자료구조와 알고리즘을 활용해 서비스의 기능과 처리 성능을 구현해요.'}, {'title': '알고리즘 연구원', 'description': '계산 문제의 난이도를 분석하고 새로운 해결 방법의 성질을 증명해요.'}], 'HCI': [{'title': 'UX 리서처', 'description': '인터뷰와 사용성 평가로 사용자의 행동과 어려움을 파악하고 개선 방향을 제안해요.'}, {'title': '인터랙션 디자이너', 'description': '사용자가 제품과 상호작용하는 흐름을 설계하고 시제품으로 사용 경험을 검토해요.'}, {'title': 'HCI 연구원', 'description': '사람과 기술의 상호작용을 연구하고 새로운 인터페이스를 만들고 평가해요.'}], 'Optimization': [{'title': '최적화 엔지니어', 'description': '자원과 제약을 수학적으로 표현해 비용·시간 등을 개선하는 해법을 구현해요.'}, {'title': '운영과학 분석가', 'description': '배차·재고·일정처럼 운영상의 선택을 모델링하고 의사결정을 도와요.'}, {'title': '최적화 연구원', 'description': '최적해를 찾는 알고리즘의 정확성과 계산 효율을 연구해요.'}], 'infoSec': [{'title': '보안 엔지니어', 'description': '시스템과 서비스의 보호 장치를 설계하고 취약점을 점검·개선해요.'}, {'title': '보안 분석가', 'description': '보안 로그와 이상 징후를 분석하고 침해 사고의 탐지와 대응을 수행해요.'}, {'title': '보안 연구원', 'description': '공격과 취약점의 원리를 분석하고 새로운 방어 방법을 연구해요.'}], 'Computer_Architecture': [{'title': '프로세서 설계 엔지니어', 'description': '명령을 처리하는 프로세서의 구조와 회로 동작을 설계하고 검증해요.'}, {'title': '하드웨어 엔지니어', 'description': '컴퓨터 장치와 디지털 회로를 설계하고 성능과 동작을 시험해요.'}, {'title': '컴퓨터구조 연구원', 'description': '프로세서와 메모리 구조를 연구해 성능과 에너지 효율을 개선해요.'}], 'Embedded_Systems': [{'title': '임베디드 소프트웨어 개발자', 'description': '자동차나 가전 같은 기기 안에서 동작하는 프로그램을 개발해요.'}, {'title': '펌웨어 엔지니어', 'description': '센서와 장치를 직접 제어하는 소프트웨어를 작성하고 하드웨어와의 동작을 검증해요.'}, {'title': 'IoT 엔지니어', 'description': '기기와 네트워크를 연결해 센서 데이터를 주고받고 원격으로 제어하는 기능을 만들어요.'}], 'Robotics': [{'title': '로봇 엔지니어', 'description': '로봇의 센서·구동 장치·제어 기능을 통합하고 실제 동작을 시험해요.'}, {'title': '로봇 소프트웨어 개발자', 'description': '로봇의 위치 추정과 경로 계획, 움직임 제어를 위한 프로그램을 개발해요.'}, {'title': '로봇공학 연구원', 'description': '로봇이 주변을 인식하고 학습하며 행동하는 새로운 방법을 연구해요.'}], 'Computer_Systems': [{'title': '시스템 소프트웨어 개발자', 'description': '운영체제와 실행 환경의 자원 관리와 성능을 개선하는 소프트웨어를 개발해요.'}, {'title': '플랫폼 엔지니어', 'description': '개발과 서비스 운영에 필요한 공통 실행 환경을 만들고 자동화해요.'}, {'title': '컴퓨터시스템 연구원', 'description': '분산 시스템과 운영체제 등의 구조를 연구해 효율성과 안정성을 높여요.'}], 'Cognitive_Science': [{'title': '인지과학 연구원', 'description': '사람의 지각·기억·학습·판단을 실험과 계산 모델로 연구해요.'}, {'title': 'UX 리서처', 'description': '사람이 정보를 이해하고 제품을 사용하는 방식을 조사해 사용자 경험 개선을 도와요.'}, {'title': '인간공학 연구원', 'description': '사람의 인지·신체 특성을 고려해 제품과 작업 환경의 편의성과 안전성을 연구해요.'}], 'Applied_Mathematics': [{'title': '수학 모델링 연구원', 'description': '현실 현상을 수학적 관계로 표현하고 모델의 결과를 해석해요.'}, {'title': '시뮬레이션 엔지니어', 'description': '수치 계산으로 물리·공학 시스템의 동작을 모사하고 설계 대안을 비교해요.'}, {'title': '응용수학 연구원', 'description': '미분방정식과 수치해석 등의 방법으로 과학·공학 문제의 해법을 연구해요.'}]}
CAREER_DESCRIPTIONS["Apllied_Mathematics"] = CAREER_DESCRIPTIONS["Applied_Mathematics"]
