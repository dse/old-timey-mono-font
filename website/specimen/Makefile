SHELL = bash

default: \
	prepare \
	src/fonts/OldTimeyCode.woff2 \
	src/fonts/OldTimeyMono.woff2 \
	fontdata \
	build

prepare: FORCE
	rm -fr src/_data/fontdata.json || true
	rm -fr src/_data/fonts || true
	rm -fr src/fonts/* || true

src/fonts/%.woff2: ../../dist/ttf/%.ttf
	../../support/bin/fontconvert "$<" "$@.tmp.woff2"
	mv "$@.tmp.woff2" "$@"

fontdata: FORCE
	yarn fontdata

build: FORCE
	yarn build

.PHONY: FORCE
