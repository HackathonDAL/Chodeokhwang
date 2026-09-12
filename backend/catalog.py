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
