import sys
import json

status_file = sys.argv[1]

f = open(status_file , 'r')
status = f.readlines()[0]
status_dict = json.loads(status)
print status_dict[0]['status']['code']
f.close()
