import test_utils
import json
import urllib.parse
import os

def main():
    test_config_file = os.getcwd() + '/testconfig.json'
    config = open(test_config_file, 'r')
    configData = json.load(config)
    StorageAccountName = configData["StorageAccountName"]
    StorageAccountKey = configData["StorageAccountKey"]
    diskBlobSasUriList = []
    for diskBlob in configData["BlobNames"]:
        diskBlobSasUriList.append(test_utils.get_blob_sas_uri(StorageAccountName,StorageAccountKey,configData["BlobContainerName"],diskBlob))

    headers = {}
    all_snapshots_deleted = True
    headers["x-ms-version"] =  "2015-02-21"
    headers["x-ms-blob-type"] = "BlockBlob"
    headers["x-ms-delete-snapshots"] = "only"
    headers["Content-Length"] = '0'
    body_content = ''
    for sasuri in diskBlobSasUriList:
        sasuri_obj = urllib.parse.urlparse(sasuri)
        result, httpResp, errMsg = test_utils.HttpCallGetResponse('DELETE', sasuri_obj, body_content, headers = headers)
        if httpResp.status != 202:
            all_snapshots_deleted = False
    return all_snapshots_deleted

if __name__ == "__main__":
    main()
