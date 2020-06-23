import subprocess
import time
import os
import remove_blob_snapshots

def run_testcase(testcase_no):
    cwd = os.getcwd()
    os.chdir(cwd+"/TestCase"+str(testcase_no))
    test_case = subprocess.Popen(["./test.sh",str(testcase_no)],stdout=subprocess.PIPE)
    while(test_case.poll() is None):
        time.sleep(1)
    output = test_case.stdout.read()
    print(output)
    os.chdir(cwd)
    if "Passed" in output:
        return True
    else:
        return False

print ("Running Test Cases")
testcases_passed = 0
testcases_failed = 0
for i in range(1,2):
    if(run_testcase(i)):
        testcases_passed = testcases_passed + 1
    else:
        testcases_failed = testcases_failed + 1


#print ("All Snapshots Deleted : ", str(remove_blob_snapshots.main()))
print ("Number of TestCases Passed : ", str(testcases_passed))
print ("Number of TestCases Failed : ", str(testcases_failed))
print ("TestCase pass percentage : ", str(((testcases_passed*(1.0))/(testcases_passed+testcases_failed))*100))
print ("Test Cases Execution successfully completed")
