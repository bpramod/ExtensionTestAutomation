import time
import uuid
import hmac
import base64
import hashlib
import urllib
import datetime
import traceback
import urlparse
import httplib
import json
import string
import random
import subprocess
import tempfile

waagent_path = '/var/lib/waagent/'
extension_path = 'Microsoft.Azure.RecoveryServices.VMSnapshotLinux-1.0.9109.0/'
config_path = 'config/'
auto_test = 'auto_test/'
test_config_file = waagent_path + extension_path + auto_test + 'testconfig.json'

signedpermissions = 'rwd'
signedidentifier = ""
signedIP = ""
signedProtocol = "https"
signedversion = "2015-02-21"
rscc = ""
rscd = ""
rsce = ""
rscl = ""
rsct = ""

def ticks():
    dt = datetime.datetime.utcnow()
    return (dt - datetime.datetime(1, 1, 1)).total_seconds() * 10000000

def get_blob_sas_uri(StorageAccountName,StorageAccountKey,AzureContainer,AzureBlob):
    canonicalizedresource = "/blob/" + StorageAccountName + "/" + AzureContainer + "/" + AzureBlob
    signedstart = datetime.datetime.utcnow()
    signedstart = signedstart - datetime.timedelta(minutes=30)
    signedstartISO = signedstart.replace(microsecond=0).isoformat() + 'Z'
    signedexpiry = signedstart + datetime.timedelta(hours=5)
    signedexpiryISO = signedexpiry.replace(microsecond=0).isoformat() + 'Z'

    StringToSign = signedpermissions + "\n" + str(signedstartISO) + "\n" + str(signedexpiryISO) + "\n" + canonicalizedresource + "\n" + signedidentifier + "\n" + signedversion + "\n" +  rscc + "\n" + rscd + "\n" +  rsce + "\n" +  rscl + "\n" +  rsct

    StringToSign = StringToSign.encode('utf-8')
    hashed = hmac.new(base64.b64decode(StorageAccountKey), digestmod=hashlib.sha256)
    hashed.update(StringToSign)
    signature = base64.encodestring(hashed.digest()).strip()
    blob_sas_uri = signedProtocol + '://'+StorageAccountName+'.blob.core.windows.net/'+AzureContainer+'/'+AzureBlob+'?sv='+signedversion + '&sr=b&sig=' + urllib.quote(signature) + '&st=' + urllib.quote(str(signedstartISO)) + '&se=' + urllib.quote(str(signedexpiryISO)) + '&sp=' + signedpermissions + '&spr=' + signedProtocol
    return blob_sas_uri

def HttpCallGetResponse(method, sasuri_obj, data, headers):
    result = 2
    resp = None
    errorMsg = None
    try:
        resp = None
        connection = httplib.HTTPSConnection(sasuri_obj.hostname, timeout = 10)
        connection.request(method=method, url=(sasuri_obj.path + '?' + sasuri_obj.query), body=data, headers = headers)
        resp = connection.getresponse()
        connection.close()
        result = 0
    except Exception as e:
        errorMsg = str(datetime.datetime.now()) +  " Failed to call http with error: %s, stack trace: %s" % (str(e), traceback.format_exc())
    
    return result, resp, errorMsg

def Call(method, sasuri_obj, data, headers, fallback_to_curl = False):
    try:
        result, resp, errorMsg = HttpCallGetResponse(method, sasuri_obj, data, headers)
        responseBody = resp.read()
        
        if(resp.status == 200 or resp.status == 201):
            return 0
        else:
            return resp.status
    except Exception as e:
        errorMsg = "Failed to call http with error: %s, stack trace: %s" % (str(e), traceback.format_exc())
        return 2


def WriteBlockBlob(msg,blobUri):
    retry_times = 3
    while(retry_times > 0):
        if(blobUri is not None):
            sasuri_obj = urlparse.urlparse(blobUri)
            headers = {}
            headers["x-ms-blob-type"] = 'BlockBlob'
            result = Call(method = 'PUT', sasuri_obj = sasuri_obj, data = msg, headers = headers, fallback_to_curl = True)
            if(result == 0):
                retry_times = 0
            else:
                retry_times = 0
        retry_times = retry_times - 1

if __name__ == "__main__":
    main()
