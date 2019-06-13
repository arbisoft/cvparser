.PHONY: requirements, install_pocketsphinx, clean

DIFF_COVER_BASE_BRANCH=master

help:
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  deployment                  install dependencies for deployment"
	@echo "  install_pocketsphinx          clones pocketsphinx repo"
	@echo "  clean         				 removes pocketsphinx repo"

requirements:
	pip install -r requirements.txt

install_pocketsphinx:
	git clone --recursive https://github.com/bambocher/pocketsphinx-python
	sudo apt-get install swig -y
	sudo apt-get install libpulse-dev -y
	sudo apt-get install libasound2-dev -y
	cd pocketsphinx-python; pwd; sed -i 's/al.h/OpenAL\/al.h/' deps/sphinxbase/src/libsphinxad/ad_openal.c; sed -i 's/alc.h/OpenAL\/alc.h/' deps/sphinxbase/src/libsphinxad/ad_openal.c; python setup.py install

clean:
	sudo rm -r pocketsphinx-python
