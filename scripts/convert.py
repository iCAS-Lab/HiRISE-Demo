import subprocess
import sys
from pathlib import Path

INPUT_DIRECTORY = Path('src/ui')
OUTPUT_DIRECTORY = Path('src/generated_files')

for input_file in INPUT_DIRECTORY.iterdir():
    # Check and process .ui files.
    if input_file.suffix == '.ui':
        output_file = OUTPUT_DIRECTORY / (input_file.stem + '.py')
        command = ['pyside6-uic', str(input_file), '-o', str(output_file),
                   '--from-imports', '.']
    # Check and process .qrc files.
    elif input_file.suffix == '.qrc':
        output_file = OUTPUT_DIRECTORY / (input_file.stem + '_rc.py')
        command = ['pyside6-rcc', str(input_file), '-o', str(output_file)]
    else:
        # Skip non .ui or .qrc file.
        continue

    # Convert file.
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error converting {input_file}: {e}', file=sys.stderr)