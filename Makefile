.PHONY: docker-*
docker-login:
	@echo
	docker login -u="${QUAY_USERNAME}" -p="${QUAY_PASSWORD}" quay.io

.PHONY: build build-*

.PHONY: build build-*
build: build-muse build-muse-merge build-multi-muse

build-%:
	@echo
	@echo -- Building docker --
	@make -C $* build-docker NAME=$*

.PHONY: publish publish-% publish-release publish-release-%

publish: publish-muse publish-muse-merge publish-muilt-muse

publish-%:
	@echo
	@make -C $* publish

publish-release: publish-release-muse publish-release-muse-merge publish-release-muilt-muse

publish-release-%:
	@echo
	@make -C $* publish-release

