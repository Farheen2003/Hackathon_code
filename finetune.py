import requests
import openai
from pprint import pprint

openai.api_key = ""

def file_upload(f, purpose='fine-tune'):
    resp = openai.File.create(purpose=purpose, file=open(f))
    pprint(resp)
    return resp

def file_list() :
    resp = openai.File.list()
    pprint(resp)

def finetune_model(fileid, suffix, model='davinci'):
    header = {'Content-Type': 'application/json', 'Authorization' : 'Bearer %s' % openai.api_key}
    payload = {'training_file': fileid, 'model': model, 'suffix': suffix}
    resp = requests.request(method='POST', url='https://api.openai.com/v1/fine-tunes', json=payload,
    headers=header, timeout=45)
    pprint(resp.json())

def finetune_list():
    header = {'Content-Type': 'application/json', 'Authorization' : 'Bearer %s' % openai.api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes',
    headers=header, timeout=45)
    pprint(resp.json())

def finetune_events(ftid):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % openai.api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s/events' % openai.api_key,
    headers=header, timeout=45)
    pprint(resp.json)

def finetune_get(ftid):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % openai.api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s' % ftid,
    headers=header, timeout=45)
    pprint(resp.json)

resp = file_upload('json_fine_tune.jsonl')
finetune_model(resp['id'], 'fine_tune_model', 'davinci')
