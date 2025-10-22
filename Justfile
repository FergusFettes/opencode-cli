set dotenv-load

install:
	uv sync

build:
	uv build

publish: clear build
	uv publish --token $PYPI_TOKEN

test-publish: clear build
	uv publish --token $PYPI_TOKEN --publish-url https://test.pypi.org/legacy/

dev:
	uv sync

clear:
	rm -rf dist
