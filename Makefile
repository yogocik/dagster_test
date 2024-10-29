run-dagster-webserver:
	DAGSTER_HOME=$(shell pwd) dagster-webserver --dagster-log-level error --code-server-log-level critical

run-dagster-daemon:
	DAGSTER_HOME=$(shell pwd) dagster-daemon run --log-level critical --code-server-log-level error

export-dagster-home:
	export DAGSTER_HOME=$(shell pwd)