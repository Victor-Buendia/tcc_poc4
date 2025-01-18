PROJECT=hospital
GRAPHQL_SERVER_URL="http://localhost:8080/graphql"
ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:8080/host-runner"

all:
	$(MAKE) build
	$(MAKE) run

	
build:
	(cd ${PROJECT} && cartesi build)
	python3 -m venv venv && source ./venv/bin/activate
	pip install -r hospital/dev-requirements.txt
run:
	(cd ${PROJECT} && cartesi run)

run-node:
	(cd ${PROJECT} && cartesi run --no-backend)
run-backend:
	ls hospital/**/*.py | PYTHONPATH=$$(pwd):${PYTHONPATH} GRAPHQL_SERVER_URL=${GRAPHQL_SERVER_URL} ROLLUP_HTTP_SERVER_URL=${ROLLUP_HTTP_SERVER_URL} entr -r python3 hospital/main.py
run-server:
	ls hospital/**/*.py | PYTHONPATH=$$(pwd):${PYTHONPATH} GRAPHQL_SERVER_URL=${GRAPHQL_SERVER_URL} ROLLUP_HTTP_SERVER_URL=${ROLLUP_HTTP_SERVER_URL} entr -r python3 hospital/api/server.py