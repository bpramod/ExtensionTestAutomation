#!/bin/sh
echo "Test$1: Validating extension reported size"
cd ../../Microsoft.Azure.RecoveryServices.VMSnapshotLinux-*
iteration_number="$(python auto_test/generate_config_settings.py)"
echo "Iteration Number : "$iteration_number
snapshot_output="$(python main/handle.py -enable)"
sleep 40
status_file=$iteration_number
operation="getUsedSize"
extension_folder_name="$(pwd)"
used_size="$(python auto_test/validate_status_file.py $extension_folder_name/status/$status_file.status $operation)"
echo "Status File  reported size: "$used_size
if [ "$used_size" -eq 0 ]
then
    echo "Test Case $1 Failed"
else
    echo "Test Case $1 Passed"
fi
rm "config/$iteration_number.settings"
rm "status/$iteration_number.status"
