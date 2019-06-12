.PHONY: requirements

DIFF_COVER_BASE_BRANCH=master

help:
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  deployment                  install dependencies for deployment"

requirements:
	pip install -r requirements.txt
	sudo apt-get install swig
	sudo apt-get install libpulse-dev
	sudo apt-get install libasound2-dev
	git clone --recursive https://github.com/bambocher/pocketsphinx-python
	cd pocketsphinx-python
	gedit deps/sphinxbase/src/libsphinxad/ad_openal.c
	sed -i 's/al.h/OpenAL//al.h/' deps/sphinxbase/src/libsphinxad/ad_openal.c
	sed -i 's/alc.h/OpenAL//alc.h/' deps/sphinxbase/src/libsphinxad/ad_openal.c
	python setup.py install
	cd ..
	rm -r pocketsphinx-python
