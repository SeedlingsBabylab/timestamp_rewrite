import re
import os
from timestamp_revert_brute import restore_timestamps

INPUT_FOLDER = 'debug'
LENA_FOLDER = 'debug'
#INPUT_FOLDER = 'all_cha'
#LENA_FOLDER = 'both_all_ob1fixed'
OUTPUT_FOLDER = 'discrepancy'
#OUTPUT_FOLDER = 'fix_attempt_2'

def load(filename):
    input_folder = LENA_FOLDER if filename.endswith('lena.cha') else INPUT_FOLDER
    with open(os.path.join(input_folder, filename)) as f:
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

def locate_context(file, context):
    try:
        processed_context = context.split('\t')[1]
        timestamp = re.search(r'\x15([0-9]+_[0-9]+)', context)
        if timestamp:
            processed_context = timestamp.group(1)
    except:
        processed_context = context
    for i in range(len(file)):
        if file[i].find(processed_context) >= 0:
            return i

def write_back(filename, file):
    with open(os.path.join(OUTPUT_FOLDER, filename), 'w') as f:
        for line in file:
            if not line.strip():
                continue
            f.write(line)

files = sorted([x for x in os.listdir(INPUT_FOLDER) if x.endswith('.cha') and not x.endswith('lena.cha')])
edits = []
for file in files:
    print(file)
    code = load(file)
    lena = load(file[:5]+'.lena.cha')
    code_timestamps = extract_timestamps(code)
    lena_timestamps = extract_timestamps(lena)
    missing, changes, corrected = restore_timestamps(lena_timestamps, code_timestamps)
    print(changes)
    print(missing)
    edits.append((file, changes))
    with open('lena_timestamps.txt', 'w') as f:
        f.write('\n'.join([x[0] for x in lena_timestamps]))
    with open('code_timestamps.txt', 'w') as f:
        f.write('\n'.join([x[0] for x in code_timestamps]))
    with open('corrected.txt', 'w') as f:
        f.write('\n'.join(corrected))
    for change in changes:
        for i in range(len(code)-1, -1, -1):
            if code[i].find('\x15'+change[1]+'\x15')>=0:
                code[i] = code[i].replace('\x15'+change[1]+'\x15', '\x15'+change[0]+'\x15')
                break

    for timestamp in missing:
        #print(timestamp)
        for i in range(len(lena)):
            if lena[i].find(timestamp) >= 0:
                prev_context = lena[i-1]
                post_context = lena[i+1]
                missing_line = lena[i]
        prev_context_location = locate_context(code, prev_context)
        post_context_location = locate_context(code, post_context)
        if prev_context_location:
            code.insert(prev_context_location+1, missing_line)
        elif post_context_location:
            code.insert(post_context_location-1, missing_line)
        else:
            print('Error: cannot find context' + timestamp)

    write_back(file, code)

with open('edits.txt', 'w') as f:
    for edit in edits:
        f.write(edit[0] + '\n')
        for change in edit[1]:
            f.write('\t' + change[1] + ' -> ' + change[0] + '\n')



# for file in files:
#     print(file)
#     code = load(file)
#     lena = load(file[:5]+'.lena.cha')
#     timestamps = extract_timestamps(code)
#     dis_timestamps = detect_timestamp_discontinuity(timestamps)
#     for timestamp in dis_timestamps:
#         print(timestamp)
#         missing_timestamp = timestamp[0][0].split('_')[1] + '_' + timestamp[1][0].split('_')[0]
#         for i in range(len(lena)):
#             if lena[i].find(missing_timestamp) >= 0:
#                 prev_context = lena[i-1]
#                 post_context = lena[i+1]
#                 missing_line = lena[i]
#         prev_context_location = locate_context(code, prev_context)
#         post_context_location = locate_context(code, post_context)
#         code.insert(prev_context_location+1, missing_line)
#     write_back(file, code)


# files = sorted([x for x in os.listdir(INPUT_FOLDER) if x.endswith('.cha')])
# for i in range(0, len(files), 2):
#     lena_filename = files[i] if files[i].endswith('lena.cha') else files[i+1]
#     code_filename = files[i+1] if files[i].endswith('lena.cha') else files[i]
#     try:
#         lena = load(lena_filename)
#         code = load(code_filename)
#     except:
#         print('Error: ' + lena_filename[:5])
#         pass
#     lena_timestamps = extract_timestamps(lena)
#     code_timestamps = extract_timestamps(code)
#     if(len(lena_timestamps) - len(code_timestamps) != 0):
#         print(lena_filename)

# code = '01_06_sparse_code.cha'
# code = load(code)
# code_timestamps = extract_timestamps(code)
#
# discontinue_timestamps = [x[0][0] for x in detect_timestamp_discontinuity(code_timestamps)]
# print('\n'.join(discontinue_timestamps))

#lena_timestamps = [x[0] for x in lena_timestamps]
#code_timestamps = [x[0] for x in code_timestamps]
#print(len(lena_timestamps))
#print(len(code_timestamps))
#print('\n'.join(code_timestamps))
# for timestamp in lena_timestamps:
#     if timestamp not in code_timestamps:
#         print(timestamp)
