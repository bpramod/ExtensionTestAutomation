import os
for i in range(2,14):
    cwd = os.getcwd()
    os.chdir(cwd+"/TestCase"+str(i))
    filename = 'test.sh'
# Read in the file
    with open(filename, 'r') as file :
          filedata = file.read()

# Replace the target string
    filedata = filedata.replace('cd ../../Microsoft.Azure.RecoveryServices.VMSnapshotLinux-*', 'cd ../../Microsoft.Azure.Backup.Test.MyBackupTestLinuxInt-*')
    #filedata = filedata.replace('cd ../../Microsoft.Azure.Backup.Test.MyBackupTestLinuxInt-*', 'cd ../../Microsoft.Azure.RecoveryServices.VMSnapshotLinux-*')

# Write the file out again
    with open(filename, 'w') as file:
          file.write(filedata)
    os.chdir(cwd)
