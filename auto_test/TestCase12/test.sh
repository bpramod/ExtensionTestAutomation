#!/bin/sh
echo "Test$1: Taking sequential snapshots"

#pre backup steps
cp /etc/azure/vmbackup.conf /tmp/
cp ./vmbackup.conf /etc/azure/

cd ../../
iteration_number="$(python auto_test/generate_config_settings.py)"
echo "Iteration Number : "$iteration_number
snapshot_output="$(python main/handle.py -enable)"
sleep 40
status_file=$iteration_number
extension_folder_name="$(pwd)"
extension_error_code="$(python auto_test/validate_status_file.py $extension_folder_name/status/$status_file.status)"
echo "Status File Error Code : "$extension_error_code
if [ "$extension_error_code" -eq 0 ]
then
    echo "Test Case $1 Passed"
else
    echo "Test Case $1 Failed"
fi

#post backup steps
cp /tmp/vmbackup.conf /etc/azure/
rm "config/$iteration_number.settings"
rm "status/$iteration_number.status"
