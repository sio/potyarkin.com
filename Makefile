PELICAN?=$(VENV)/pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/html
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py
PROFILER=$(BASEDIR)/profiler.py

PORT=8000

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make clean                          remove the generated files         '
	@echo '   make regenerate                     regenerate files upon modification '
	@echo '   make publish                        generate using production settings '
	@echo '   make serve [PORT=8000]              serve site at http://localhost:8000'
	@echo '   make profile                        run cProfile to analyze performance'
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '

html: venv
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

publish: venv
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)

profile: venv
	$(VENV)/python $(PROFILER) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

serve: venv
	$(VENV)/pelican --listen --autoreload --port $(PORT) --bind 127.0.0.1 --output $(OUTPUTDIR)

.PHONY: html help clean regenerate serve devserver publish


include Makefile.venv
Makefile.venv:
	curl \
		-o Makefile.fetched \
		-L "https://github.com/sio/Makefile.venv/raw/v2020.02.26/Makefile.venv"
	echo "e0aeebe87c811fd9dfd892d4debb813262646e3e82691e8c4c214197c4ab6fac *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv


.PHONY: links
links: $(VENV)/linkchecker
	$(VENV)/linkchecker https://potyarkin.ml --no-robots --check-extern --no-status

.PHONY: test
test: $(VENV)/pytest
	$(VENV)/pytest

.PHONY: microblog
publish html serve: | microblog
microblog:
	git submodule init
	git submodule update
	cd micro && git pull $$(git remote|head -n1) microblog

.PHONY: webring
webring: content/webring.json
publish html serve: | webring

.PHONY: content/webring.json
content/webring.json: content/blogroll.yml helpers/webring.py | venv
	$(VENV)/python -m helpers.webring $< $@ --cache-mkdir

.PHONY: newspaper
newspaper: content/newspaper.json
publish html serve: | newspaper

.PHONY: content/newspaper.json
content/newspaper.json: content/webring.json
content/newspaper.json: content/blogroll.yml helpers/newspaper.py | venv
	$(VENV)/python -m helpers.newspaper $< $@

.PHONY: whatsnew
whatsnew: | venv
	mkdir -p cache/whatsnew
	$(VENV)/python -m helpers.whatsnew
