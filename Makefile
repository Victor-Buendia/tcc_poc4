PROJECT=hospital

all:
	$(MAKE) build
	$(MAKE) run

	
build:
	(cd ${PROJECT} && cartesi build)
run:
	(cd ${PROJECT} && cartesi run)
