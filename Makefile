run:
	python src/main.py

convert:
	python scripts/convert.py

clean:
	rm -rf src/generated_files/*.py
	touch src/generated_files/__init__.py
