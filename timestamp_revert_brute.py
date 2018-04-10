import re
import os
import difflib

INPUT_FOLDER = 'both_all_ob1fixed'
INPUT_FOLDER = 'debug'
OUTPUT_FOLDER = 'fix_attempt'

def load(filename):
    with open(os.path.join(INPUT_FOLDER, filename)) as f:
        return f.readlines()

def extract_timestamps(lines):
    timestamps = []
    for i in range(len(lines)):
        timestamps += [(x, i) for x in re.findall(r'\x15([0-9]+_[0-9]+)', lines[i])]
    return timestamps

def detect_timestamp_discontinuity(timestamps):
    res = []
    for i in range(1, len(timestamps)):
        if not timestamps[i][0].split('_')[0]==timestamps[i-1][0].split('_')[1]:
            res.append((timestamps[i-1], timestamps[i]))
    return res

def grab_correct_endtime(lines, index):
    line = lines[index+1] + lines[index+2] + lines[index+3]
    line = re.sub(r'\n+?\t+?', ' ', line)
    match = re.findall(r'was ([0-9]+)', line)
    if match:
        return match[-1]
    else:
        return None

def grab_correct_endtime_from_lena(timestamp):
    return MAPPING[timestamp.split('_')[0]]

def create_mapping(timestamps):
    mapping = {}
    for timestamp in timestamps:
        mapping[timestamp[0].split('_')[0]] = timestamp[0].split('_')[1]
    return mapping

def write_back(filename, file):
    with open(os.path.join(OUTPUT_FOLDER, filename), 'w') as f:
        for line in file:
            f.write(line)

def restore_timestamps(lena_timestamps, code_timestamps):
    diff = list(difflib.ndiff([x[0] for x in lena_timestamps], [x[0] for x in code_timestamps]))
    with open('diff.txt', 'w') as f:
        f.write('\n'.join(diff))
    diff = [x for x in diff if not x.startswith('?') and x]
    i = 0
    changes = []
    while i < len(diff) - 1:
        if diff[i].startswith('-') and diff[i+1].startswith('-') and diff[i+2].startswith('-')  and diff[i+3].startswith('-') and diff[i+4].startswith('-')\
        and diff[i+5].startswith('+') and diff[i+6].startswith('+') and diff[i+7].startswith('+') and diff[i+8].startswith('+') and diff[i+9].startswith('+'):
            changes.append((diff[i].lstrip('- '), diff[i+5].lstrip('+ ')))
            changes.append((diff[i+1].lstrip('- '), diff[i+6].lstrip('+ ')))
            changes.append((diff[i+2].lstrip('- '), diff[i+7].lstrip('+ ')))
            changes.append((diff[i+3].lstrip('- '), diff[i+8].lstrip('+ ')))
            changes.append((diff[i+4].lstrip('- '), diff[i+9].lstrip('+ ')))
            diff[i] = diff[i].replace('-', ' ')
            diff[i+1] = diff[i+1].replace('-', ' ')
            diff[i+2] = diff[i].replace('-', ' ')
            diff[i+3] = diff[i].replace('-', ' ')
            diff[i+4] = diff[i].replace('-', ' ')
            del diff[i+9]
            del diff[i+8]
            del diff[i+7]
            del diff[i+6]
            del diff[i+5]
            i += 5
            continue
        if diff[i].startswith('-') and diff[i+1].startswith('-') and diff[i+2].startswith('-')  and diff[i+3].startswith('-')\
        and diff[i+4].startswith('+') and diff[i+5].startswith('+') and diff[i+6].startswith('+') and diff[i+7].startswith('+'):
            changes.append((diff[i].lstrip('- '), diff[i+4].lstrip('+ ')))
            changes.append((diff[i+1].lstrip('- '), diff[i+5].lstrip('+ ')))
            changes.append((diff[i+2].lstrip('- '), diff[i+6].lstrip('+ ')))
            changes.append((diff[i+3].lstrip('- '), diff[i+7].lstrip('+ ')))
            diff[i] = diff[i].replace('-', ' ')
            diff[i+1] = diff[i+1].replace('-', ' ')
            diff[i+2] = diff[i].replace('-', ' ')
            diff[i+3] = diff[i].replace('-', ' ')
            del diff[i+7]
            del diff[i+6]
            del diff[i+5]
            del diff[i+4]
            i += 4
            continue
        if diff[i].startswith('-') and diff[i+1].startswith('-') and diff[i+2].startswith('-')\
        and diff[i+3].startswith('+') and diff[i+4].startswith('+') and diff[i+5].startswith('+'):
            changes.append((diff[i].lstrip('- '), diff[i+3].lstrip('+ ')))
            changes.append((diff[i+1].lstrip('- '), diff[i+4].lstrip('+ ')))
            changes.append((diff[i+2].lstrip('- '), diff[i+5].lstrip('+ ')))
            diff[i] = diff[i].replace('-', ' ')
            diff[i+1] = diff[i+1].replace('-', ' ')
            diff[i+2] = diff[i].replace('-', ' ')
            del diff[i+5]
            del diff[i+4]
            del diff[i+3]
            i += 3
            continue
        if diff[i].startswith('-') and diff[i+1].startswith('-') and diff[i+2].startswith('+') and diff[i+3].startswith('+'):
            changes.append((diff[i].lstrip('- '), diff[i+2].lstrip('+ ')))
            changes.append((diff[i+1].lstrip('- '), diff[i+3].lstrip('+ ')))
            diff[i] = diff[i].replace('-', ' ')
            diff[i+1] = diff[i+1].replace('-', ' ')
            del diff[i+3]
            del diff[i+2]
            i += 2
            continue
        if diff[i].startswith('-') and diff[i+1].startswith('+'):
            changes.append((diff[i].lstrip('- '), diff[i+1].lstrip('+ ')))
            diff[i] = diff[i].replace('-', ' ')
            del diff[i+1]
            i += 1
            continue
        if diff[i+1].startswith('-') and diff[i].startswith('+'):
            changes.append((diff[i+1].lstrip('- '), diff[i].lstrip('+ ')))
            diff[i+1] = diff[i+1].replace('-', ' ')
            del diff[i]
            i += 1
            continue
        i += 1
    missing = [x.lstrip('- ') for x in diff if x.startswith('-')]
    diff = [x.strip() for x in diff]
    # with open('diff.txt', 'w') as f:
    #     f.write('\n'.join(diff))
    return missing, changes, diff

if __name__=='__main__':
    MISSING_LINE = []
    files = sorted([x for x in os.listdir(INPUT_FOLDER) if x.endswith('.cha')])
    for i in range(0, len(files), 2):
        print(files[i])
        lena_filename = files[i] if files[i].endswith('lena.cha') else files[i+1]
        code_filename = files[i+1] if files[i].endswith('lena.cha') else files[i]
        try:
            lena = load(lena_filename)
            code = load(code_filename)
        except:
            print('Error: ' + lena_filename[:5])
            pass
        lena_timestamps = extract_timestamps(lena)
        code_timestamps = extract_timestamps(code)
