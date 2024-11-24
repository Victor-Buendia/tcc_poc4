all:
	$(MAKE) build
	$(MAKE) run

	
build:
	cartesi build
run:
	cartesi run
