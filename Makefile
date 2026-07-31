PYTHON ?= /Users/molfesepj/miniconda3/envs/mne/bin/python
PELICAN ?= /Users/molfesepj/miniconda3/envs/mne/bin/pelican
PELICANOPTS ?=

BASEDIR := $(CURDIR)
INPUTDIR := $(BASEDIR)/content
OUTPUTDIR := $(BASEDIR)/output
CONFFILE := $(BASEDIR)/pelicanconf.py
PUBLISHCONF := $(BASEDIR)/publishconf.py

.PHONY: help build clean rebuild serve image publish

help:
	@echo "make build    Build the development site"
	@echo "make serve    Build, watch, and serve at http://127.0.0.1:8000"
	@echo "make image    Regenerate the front-page collaborator image"
	@echo "make publish  Build with publishconf.py"
	@echo "make clean    Remove generated output"

build:
	"$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

clean:
	rm -rf "$(OUTPUTDIR)"

rebuild: clean build

serve:
	"$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" -r -l $(PELICANOPTS)

image:
	"$(PYTHON)" "$(BASEDIR)/scripts/build_collaborators_image.py"

publish:
	"$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(PUBLISHCONF)" $(PELICANOPTS)
