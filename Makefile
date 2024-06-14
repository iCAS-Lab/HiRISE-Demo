run:
	chmod 700 scripts/run.sh
	scripts/run.sh

libedgetpu:
	echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
	curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
	sudo apt-get update
	sudo apt install libedgetpu-dev

install:
	mamba env create -f env.yml
	mamba activate hirise

kill:
	pkill xinit

convert:
	python scripts/convert.py

clean:
	rm -rf src/generated_files/*.py
	touch src/generated_files/__init__.py
