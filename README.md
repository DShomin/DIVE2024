
# directory structure

`langgraph_back` is for backend code that for running langgraph server
`langgraph_front` is for frontend code that is as a streamlit app
`postgres_server` is for postgres db that is used for storing data
`notebook` is for jupyter notebook code it is just for test and debug 

# Run server

1. `source postgres_server/build_docker.sh` 명령어를 실행하여 도커 컨테이너를 실행한다.
2. data를 root 디렉토리에 이동시킨다.(DB로 업로드 시킬 csv 파일은 해당 디렉토리로 이동시킨다.)
```
data
├── DB
│   ├── lotte
│   │   ├── 002_ltmb_k7_data.csv
│   │   └── 003_ltmb_mart_data.csv
│   └── samsung
│       └── DIVE_FINAL_F.csv
```
3. `postgres_server/upload_csv.py`를 실행하여 csv 파일을 업로드 시킨다.
    만약 추가로 업로드할 csv가 있다면 해당 파일을 참고하여 파일을 추가로 업로드 시킨다.
4. `postgres_server/upload_test.py`를 실행하여 업로드된 데이터가 잘 업로드 되었는지 확인한다.
5. `source langgraph_back/run_server.sh` 명령어를 실행하여 streamlit 서버를 실행한다.

# requirments
`langgraph_back`경로에 `.env` 파일이 있어야하며 해당 파일에는 `OPENAI_API_KEY`가 있어야한다.