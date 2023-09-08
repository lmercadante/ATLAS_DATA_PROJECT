import os
import requests
import json
from collections import OrderedDict
import time
import csv

#TNS                 = "www.wis-tns.org"
TNS                 = "sandbox.wis-tns.org"
url_tns_api         = "https://" + TNS + "/api/get"

TNS_BOT_ID          = "156355"
TNS_BOT_NAME        = "LSM_bot"
TNS_API_KEY         = "ba3e1918b85287f65877d241b36520a603630242"

def set_bot_tns_marker():
    tns_marker = 'tns_marker{"tns_id": "' + str(TNS_BOT_ID) + '", "type": "bot", "name": "' + TNS_BOT_NAME + '"}'
    return tns_marker

def search():
    search_url = url_tns_api + "/search"
    tns_marker = set_bot_tns_marker()
    headers = {'User-Agent': tns_marker}
    json_file = OrderedDict(search_obj)
    search_data = {'api_key': TNS_API_KEY, 'data': json.dumps(json_file)}
    response = requests.post(search_url, headers = headers, data = search_data)
    return response

def format_to_json(source):
    parsed = json.loads(source, object_pairs_hook = OrderedDict)
    result = json.dumps(parsed, indent = 4)
    return result, parsed

search_obj          = [("ra", ""), ("dec", ""), ("radius", "5"), ("units", "arcsec"), 
                       ("objname", ""), ("objname_exact_match", 0), ("internal_name", ""), 
                       ("internal_name_exact_match", 0), ("objid", ""), ("public_timestamp", "")]
response = search()

json_text,json_data = format_to_json(response.text)
print(json_data)

json_data_dict = json.loads(json.dumps(json_data))
json_data_dict_lvl2 = json_data_dict['data']
json_data_dict_lvl3 = json_data_dict_lvl2['reply']
json_data_dict_lvl4 = json_data_dict_lvl3[0]
object_name = json_data_dict_lvl4['objname']
prefix = json_data_dict_lvl4['prefix']
object_id = json_data_dict_lvl4['objid']

print (json_data_dict_lvl4)
print(type(json_data_dict_lvl4))
print(len(json_data_dict_lvl4))
print(object_name)
print(prefix)
print(object_id)

header = ['Object Name', 'Prefix', 'Object ID']

row = [object_name, prefix, object_id]

with open("object_search_out.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerow(row)
