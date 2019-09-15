.PHONY: deploy
deploy: build
	twine upload dist/*

.PHONY: test-deploy
test-deploy: build
	twine upload -r pypitest dist/*

.PHONY: build
build:
	rm -rf pyroombaadapter.egg-info dist
	python setup.py sdist bdist_wheel

