#!/bin/sh
echo "Test$1: pre script File doesn't have desired permissions COF:false"

#pre backup steps
cp /etc/azure/VMSnapshotScriptPluginConfig.json /tmp/
cp ./VMSnapshotScriptPluginConfig.json /etc/azure/
chmod 777 /etc/azure/preScript.sh

cd ../../Microsoft.Azure.RecoveryServices.VMSnapshotLinux-*
iteration_number="$(python auto_test/generate_config_settings.py)"
echo "Iteration Number : "$iteration_number
snapshot_output="$(python main/handle.py -enable)"
sleep 40
status_file=$iteration_number
operation="getErrorCode"
extension_folder_name="$(pwd)"
extension_error_code="$(python auto_test/validate_status_file.py $extension_folder_name/status/$status_file.status $operation)"
echo "Status File Error Code : "$extension_error_code
if [ "$extension_error_code" -eq 306 ]
then
    echo "Test Case $1 Passed"
else
    echo "Test Case $1 Failed"
fi


#post backup steps
cp /tmp/VMSnapshotScriptPluginConfig.json /etc/azure/
chmod 700 /etc/azure/preScript.sh
rm "config/$iteration_number.settings"
rm "status/$iteration_number.status"
