import os
import json

src_dir = 'text/'
prompt_dir = 'prompt/'

def open_file(fp):
    with open(fp, 'r', encoding='utf-8') as infile:
        return infile.read()
    
if __name__ == '__main__':
    files1 = os.listdir(src_dir)
    files2 = os.listdir(prompt_dir)
    data = list()
    print(len(files1))
    for i in range(len(files1)):
        completion = open_file(src_dir + files1[i])
        prompt = open_file(prompt_dir + files2[i])
        info = {'prompt': prompt, 'completion': completion}
        data.append(info)
    with open('json_fine_tune.jsonl', 'w') as outfile:
        for i in data:
            json.dump(i, outfile)
            outfile.write('\n')