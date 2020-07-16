#!/bin/sh
echo "Test$1: FailedWorkloadInvalidRoleapponly"

cp /etc/azure/workload.conf /tmp/
cp faultyconfig.conf /etc/azure/workload.conf
cp /etc/azure/vmbackup.conf /tmp/
cp vmbackup.conf /etc/azure/vmbackup.conf


cd ../../
iteration_number="$(python3 auto_test/generate_config_settings.py)"
echo "Iteration Number : "$iteration_number
snapshot_output="$(python3 main/handle.py -enable)"
sleep 40
status_file=$iteration_number
operation="getErrorCode"
extension_folder_name="$(pwd)"
extension_error_code="$(python3 auto_test/validate_status_file.py $extension_folder_name/status/$status_file.status $operation)"
echo "Status File Error Code : "$extension_error_code
if [ "$extension_error_code" -eq 1 ]
then
    echo "Test Case $1 Passed"
else
    echo "Test Case $1 Failed"
fi

cp /tmp/workload.conf /etc/azure/
cp /tmp/vmbackup.conf /etc/azure/
rm "config/$iteration_number.settings"
rm "status/$iteration_number.status"
