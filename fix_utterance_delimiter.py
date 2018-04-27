import os
import re

INPUT_FOLDER = './discrepancy'
OUTPUT_FOLDER = './fixed_utterance'
files = [x for x in os.listdir(INPUT_FOLDER) if x.endswith('.cha')]

def insert_period(line):
	return line.replace('\x15', '. \x15', 1)

def has_timestamp(line):
	return True if re.search(r'\x15[0-9]+_[0-9]+\x15', line) else False

for file in files:
	print(file)
	with open(os.path.join(INPUT_FOLDER, file)) as f:
		data = f.readlines()

	for i in range(1, len(data)):
		if data[i].startswith('\t') and has_timestamp(data[i]):
			if data[i-1].find('.')>=0 and has_timestamp(data[i-1]):
				data[i-1] = data[i-1].replace('.', '')
			if data[i].find('.') < 0:
				data[i] = insert_period(data[i])

	with open(os.path.join(OUTPUT_FOLDER, file), 'w') as f:
		f.write(''.join(data))
