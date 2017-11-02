# ExtensionTestAutomation

List of TestCases:
Test1: Backup Success Scenario
Test2: Plugin Host Config File Missing
Test3: Plugin Host Config File doesn't have desired permissions
Test4: pre script File doesn't have desired permissions COF:true
Test5: post script File Execution Failed COF:true
Test6: post script not found COF:true
Test7: pre script File TimeOut COF:true
Test8: pre script File doesn't have desired permissions COF:false
Test9: post script File Execution Failed COF:false
Test10: post script not found COF:false
Test11: pre script File TimeOut COF:false
Test12: Taking sequential snapshots

Pre-requisites to run test cases:
One need to have a storage account with 4 blobs
-	2 for generating snapshot URIs
-	1 for status blob
-	1 for Log blob

Steps to execute the Tests:
1)Copy the zip file(attached) inside the VM in “/tmp” directory
3) go to “/tmp” directory inside the VM. (cd /tmp)
2) unzip the package (unzip auto_test.zip) 
3) copy the “auto_test” directory to “/var/lib/waagent/Microsoft.Azure.RecoveryServices.VMSnapshotLinux-1.0.*” directory (cp -r auto_test /var/lib/waagent/Microsoft.Azure.RecoveryServices.VMSnapshotLinux-1.0.*)
4) mv to auto_test directory (cd /var/lib/waagent/Microsoft.Azure.RecoveryServices.VMSnapshotLinux-1.0.*/auto_test) 
5) update “testconfig.json”
5) execute the TestRunner script. (python TestRunner.py)

Details of parameters in “testconfig.json” file :
"StorageAccountName", "StorageAccountKey" are the access details for storage accounts containing the test blobs
"BlobContainerName", "BlobNames"  are to generate VHD snaspshot URIs
"LogContainerName","LogBlobName" are to generate log blob URI
"StatusContainerName" , "StatusBlobName" are to generate status blob URI

Sample testconfig.json:
{
       "StorageAccountName" : "pramb6024",
       "StorageAccountKey" : ""
       "BlobContainerName" : "test",
       "BlobNames" : ["disk1","disk2"],
       "LogContainerName" : "test",
       "LogBlobName" : "logs.txt",
       "StatusContainerName" : "test",
       "StatusBlobName" : "status.txt",
     "CertThumbprint" : "13CC23F9AFBF4CBA045573DC22B9A3BE884D9B14"
}
