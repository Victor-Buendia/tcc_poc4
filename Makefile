PROJECT=hospital
GRAPHQL_SERVER_URL="http://localhost:8080/graphql"
ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:8080/host-runner"

build:
	(cd ${PROJECT} && cartesi build)

run-node:
	(cd ${PROJECT} && cartesi run --no-backend)
run-backend:
	ls ${PROJECT}/**/*.py | GRAPHQL_SERVER_URL=${GRAPHQL_SERVER_URL} ROLLUP_HTTP_SERVER_URL=${ROLLUP_HTTP_SERVER_URL} entr -r python3 ${PROJECT}/main.py
run-server:
	ls ${PROJECT}/**/*.py | GRAPHQL_SERVER_URL=${GRAPHQL_SERVER_URL} ROLLUP_HTTP_SERVER_URL=${ROLLUP_HTTP_SERVER_URL} entr -r python3 ${PROJECT}/api/server.py