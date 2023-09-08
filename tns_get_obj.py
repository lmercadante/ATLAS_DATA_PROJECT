import os
import requests
import json
from collections import OrderedDict
import time
import csv
import pandas as pd


TNS                 = "sandbox.wis-tns.org"
url_tns_api         = "https://" + TNS + "/api/get"

TNS_BOT_ID          = "156355"
TNS_BOT_NAME        = "LSM_bot"
TNS_API_KEY         = "ba3e1918b85287f65877d241b36520a603630242"

input_file = pd.read_csv('object_search_out.csv')
object_name_list = input_file['Object Name']
#object_id_list = input_file['Object ID']
object_name = object_name_list[0]
#object_id = object_id_list[0]
print(object_name)

get_obj             = [("objname", object_name), ("objid", ""), ("photometry", "1"), ("spectra", "0")]

def set_bot_tns_marker():
    tns_marker = 'tns_marker{"tns_id": "' + str(TNS_BOT_ID) + '", "type": "bot", "name": "' + TNS_BOT_NAME + '"}'
    return tns_marker

def format_to_json(source):
    parsed = json.loads(source, object_pairs_hook = OrderedDict)
    result = json.dumps(parsed, indent = 4)
    return result

def get():
    get_url = url_tns_api + "/object"
    tns_marker = set_bot_tns_marker()
    headers = {'User-Agent': tns_marker}
    json_file = OrderedDict(get_obj)
    get_data = {'api_key': TNS_API_KEY, 'data': json.dumps(json_file)}
    response = requests.post(get_url, headers = headers, data = get_data)
    return response

response = get()
json_data = format_to_json(response.text)
print (json_data)
#print(json_data.index('jd'))

ra_srt, ra_end = json_data.index('radeg') + 8,json_data.index('radeg')+20
dec_srt, dec_end = json_data.index('decdeg') + 9,json_data.index('decdeg')+18
jd_srt, jd_end = json_data.index('jd')+5,json_data.index('jd') + 17
z_srt, z_end = json_data.index('redshift')+11,json_data.index('redshift') + 16
ra =float( ''.join([sub for sub in json_data])[ra_srt : ra_end])
dec =float(''.join([sub for sub in json_data])[dec_srt : dec_end])
jd = float(''.join([sub for sub in json_data])[jd_srt : jd_end])
z = float(''.join([sub for sub in json_data])[z_srt : z_end])
#print(json_data[545])
#print(ra)
#print(dec)
#print(jd)
print(z)

def jd_to_mjd(julian_date):
    return julian_date - 2400000.5

mjd = jd_to_mjd(jd)

header = ['Name','RA(deg)','DEC(deg)','MJD', 'SN_Redshift']
row = [str(object_name),str(ra),str(dec),str(mjd), str(z)]
with open("object_get_out.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerow(row)
