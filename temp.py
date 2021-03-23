import os, json

json_path = os.path.join(os.path.split(__file__)[0], 'json.txt')
with open(json_path, 'r', encoding='UTF-8') as f:
    flexmessagestring = f.read()

dict1 = json.loads(flexmessagestring)

dict1['header']['contents'][0]['contents'][1]['text']='南港'
# print(dict1['header']['contents'][0]['contents'][1]['text'])

print(dict1)
