import time
import uuid
import hmac
import base64
import hashlib
import urllib
import datetime
import traceback
import urllib.parse
import http.client
import json
import string
import random
import subprocess
import tempfile
import test_utils
import os

waagent_path = '/var/lib/waagent/'
extension_path = os.getcwd() + '/'
config_path = 'config/'
auto_test = 'auto_test/'
test_config_file = extension_path + auto_test + 'testconfig.json'

def main():
    config = open(test_config_file, 'r')
    configData = json.load(config)
    StorageAccountName = configData["StorageAccountName"]
    StorageAccountKey = configData["StorageAccountKey"]
    certThumbprint = configData["CertThumbprint"]
    StorageAccountKey = StorageAccountKey.encode('utf-8')
    diskBlobSasUriList = []
    for diskBlob in configData["BlobNames"]:
        diskBlobSasUriList.append(test_utils.get_blob_sas_uri(StorageAccountName,StorageAccountKey,configData["BlobContainerName"],diskBlob))
    logBlobSasUri = test_utils.get_blob_sas_uri(StorageAccountName,StorageAccountKey,configData["LogContainerName"],configData["LogBlobName"])
    StatusBlobSasUri = test_utils.get_blob_sas_uri(StorageAccountName,StorageAccountKey,configData["StatusContainerName"],configData["StatusBlobName"])
    settingsFileName = str(int(time.time()))
    InitBackupHandlerConfiguration(settingsFileName,certThumbprint,diskBlobSasUriList,logBlobSasUri,StatusBlobSasUri)
    print(settingsFileName)

def InitBackupHandlerConfiguration(settingsFileName,certThumbprint,diskBlobSasUriList,logBlobSasUri,StatusBlobSasUri):
    sampleMetadata = [{'Key':'key1','Value':'value1'},{'Key':'key2','Value':'value2'}]
    publicStr = "{ \"backupMetadata\" : " + json.dumps(sampleMetadata) + "}"
    privateStr = "{\"blobSASUri\":" + json.dumps(diskBlobSasUriList) + "}"
    publicStr = base64.encodestring(publicStr.encode('utf-8'))
    privateStr =  base64.encodestring(privateStr.encode('utf-8'))
    publicStr = publicStr.replace("\n","")
    privateStr = privateStr.replace("\n","")
    '''print base64.decodestring(privateStr)
    print
    print
    print base64.decodestring(publicStr)'''
    taskId = ''.join(random.choice(string.ascii_lowercase) for i in range(15))
    publicConfig = "{" + "\"locale\":\"en-us\"," + "\"logsBlobUri\":\"" + logBlobSasUri + "\"," + "\"taskId\":\"" + taskId + "\"," + "\"statusBlobUri\":\"" + StatusBlobSasUri + "\"," + "\"commandStartTimeUTCTicks\":\""+ str(int(test_utils.ticks())) + "\"," +"\"vmType\": \"microsoft.compute/virtualmachines\","+ "\"objectStr\":\"" +  publicStr +  "\"," + "\"commandToExecute\":\"" + "Snapshot\"" + "}"
    privateConfig = "{\"logsBlobUri\":\"" + logBlobSasUri +  "\"," + "\"objectStr\":\"" + privateStr + "\"" + "}"
    '''print
    print
    print publicConfig
    print
    print
    print privateConfig
    test_pu = json.loads(privateConfig)'''
    InitHandlerConfiguration(settingsFileName, certThumbprint, publicConfig, privateConfig)


def InitHandlerConfiguration(settingsFileName, certThumbprint, publicConfig, privateConfig):
    cert_file = waagent_path + certThumbprint + '.crt'
    temp_f = tempfile.NamedTemporaryFile(delete=False)
    temp_f.write(privateConfig)
    temp_f.close()
    encrypt = subprocess.Popen(["openssl","smime","-encrypt","-outform","DER","-in",temp_f.name,cert_file],stdout=subprocess.PIPE)
    while(encrypt.poll() is None):
        time.sleep(1)
    output = encrypt.stdout.read()
    encryptedPrivateConfig = base64.encodestring(output)
    encryptedPrivateConfig = encryptedPrivateConfig.replace("\n","")
    file_content = "{" + "\"runtimeSettings\": [" + "{" + "\"handlerSettings\": {" + "\"protectedSettings\": \""+ encryptedPrivateConfig +"\"," + "\"protectedSettingsCertThumbprint\": \""+ certThumbprint +"\"," + "\"publicSettings\": "+ publicConfig + "}" + "}" + "]" + "}"
    settings_file = open(extension_path + config_path + settingsFileName+".settings","w+")
    settings_file.write(file_content)

if __name__ == "__main__":
    main()
