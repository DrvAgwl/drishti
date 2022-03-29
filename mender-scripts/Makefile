
COMMIT =$(shell git rev-parse --short HEAD)

build:
	docker build -t "make-drishti-artifacts" .
run:
	COMMIT=`git rev-parse --short HEAD`
	mv ../.git /tmp/.git
	docker run --rm -v `pwd`/../:/udaan-drishti -v /tmp/:/artifacts --env COMMIT=$(COMMIT) make-drishti-artifacts
	mv /tmp/.git ../

