#!/bin/sh
echo "Test$1: Plugin Host Config File doesn't have desired permissions"
cd ../../

#pre backup steps
chmod 777 /etc/azure/VMSnapshotScriptPluginConfig.json

iteration_number="$(python auto_test/generate_config_settings.py)"
echo "Iteration Number : "$iteration_number
snapshot_output="$(python main/handle.py -enable)"
sleep 40
status_file=$iteration_number
operation="getErrorCode"
extension_folder_name="$(pwd)"
extension_error_code="$(python auto_test/validate_status_file.py $extension_folder_name/status/$status_file.status $operation)"
echo "Status File Error Code : "$extension_error_code
if [ "$extension_error_code" -eq 1 ]
then
    echo "Test Case $1 Passed"
else
    echo "Test Case $1 Failed"
fi


#post backup steps
chmod 600 /etc/azure/VMSnapshotScriptPluginConfig.json
rm "config/$iteration_number.settings"
rm "status/$iteration_number.status"
