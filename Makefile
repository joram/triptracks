PYTHONPATH=.

setup:
	pyenv install 3.10
	pyenv virtualenv 3.10 tt
	pyenv activate tt
	pip install -r requirements.txt

mec:
	./scrapers/products/mec.py

steepandcheap:
	./scrapers/products/steep_and_cheap.py

rei:
	./scrapers/products/rei.py

vpo:
	./scrapers/products/vpo.py

backpack:
	./backpack/update_products_manifest.py
	./backpack/main.py