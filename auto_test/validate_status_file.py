import sys
import json

status_file = sys.argv[1]
operation = sys.argv[2]

f = open(status_file , 'r')
status = f.readlines()[0]
status_dict = json.loads(status)
if( operation == "getErrorCode" ):
    print (status_dict[0]['status']['code'])
    #message = status_dict[0]['status']['formattedMessage']['message']
    #message_dict = json.loads(message)
    #print(message_dict['snapshotConsistency'])
elif (operation == "getUsedSize"):
    print (status_dict[0]['status']['storageDetails']['totalUsedSizeInBytes'])
else:
    print (status_dict[0]['status']['operation'])
f.close()
