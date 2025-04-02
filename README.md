# DIVE2024 프로젝트

본 프로젝트는 LangGraph와 PostgreSQL을 활용한 데이터 분석 및 시각화 애플리케이션입니다. LangGraph 기반의 백엔드와 Streamlit 기반의 프론트엔드로 구성되어 있습니다.

## 프로젝트 구조

- `langgraph_back`: LangGraph 서버를 실행하기 위한 백엔드 코드
- `langgraph_front`: Streamlit 앱으로 구현된 프론트엔드 코드
- `postgres_server`: 데이터 저장을 위한 PostgreSQL 데이터베이스 관련 코드
- `public`: 정적 파일들을 위한 디렉토리

## 환경 설정

1. 가상 환경 설정 (선택사항)
```bash
python -m venv .myenv
source .myenv/bin/activate  # Linux/Mac
# 또는
.myenv\Scripts\activate     # Windows
```

2. 필요 패키지 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
   - `langgraph_back` 디렉토리에 `.env` 파일을 생성하고 다음 내용을 추가:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 데이터베이스 설정

1. PostgreSQL 도커 컨테이너 실행
```bash
source postgres_server/build_docker.sh
```

2. 필요한 데이터 파일 준비
   - 데이터 파일(CSV)을 준비하여 `data/DB/` 디렉토리에 배치합니다
   - 디렉토리 구조는 다음과 같아야 합니다:
   ```
   data/
   └── DB/
       ├── lotte/
       │   ├── 002_ltmb_k7_data.csv
       │   └── 003_ltmb_mart_data.csv
       └── samsung/
           └── DIVE_FINAL_F.csv
   ```

3. 데이터베이스에 CSV 파일 업로드
```bash
python postgres_server/upload_csv.py
```

4. 데이터 업로드 확인
```bash
python postgres_server/upload_test.py
```

## 서버 실행

```bash
source langgraph_back/run_server.sh
```

## 개발 환경

- Python 3.10+
- PostgreSQL
- Docker

## 참고사항

- 민감한 정보(.env 파일, API 키 등)는 절대 Git에 커밋하지 마세요.
- 대용량 데이터 파일은 `.gitignore`에 의해 Git에서 제외됩니다.
- 노트북 파일(.ipynb)은 주로 테스트 및 디버깅용으로만 사용됩니다.