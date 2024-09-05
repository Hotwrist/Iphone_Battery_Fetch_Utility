# Description: This Python script fetches the battery
#              health information from an iPhone device.

import subprocess
import re

# This function checks if an iPhone device is connected
def check_device_connection():
    try:
        # We need to execute an external command in this python script
        # and later on capture the result of this command execution.
        # shell=False is necessary to prevent execution of untrusted inputs.
        # This will retrieve the device list
        is_success = subprocess.check_output(['idevice_id', '-l'], text=True, shell=False).strip()
        if not is_success:
            print("Error: No iPhone device was detected. Try connecting your iPhone.")
            return False
        else:
            print(f"Connected Device ID: {is_success}")
        return True
    except subprocess.CalledProcessError as conn_chk_error:
        print("ERROR: Failed to check device connection: ", conn_chk_error)
        return False

def get_raw_battery_info():
    """Fetch raw battery information using ideviceinfo command."""
    try:
        raw_output = subprocess.check_output(['ideviceinfo', '-q', 'com.apple.mobile.battery'], text=True)
        return raw_output
    except subprocess.CalledProcessError as e:
        print("ERROR: Battery health data could not be fetched: ", e)
        return None

def parse_battery_info(raw_data):
    """Parse the raw battery data into a readable format."""
    battery_info = {}
    for line in raw_data.splitlines():
        match = re.match(r'(.+):\s(.+)', line)
        if match:
            key, value = match.groups()
            battery_info[key.strip()] = value.strip()
    return battery_info

def display_battery_info(battery_info):
    """Display the parsed battery health information."""
    if not battery_info:
        print("There was no battery health information found.")
        return

    print("\niPhone Battery Health Information:")
    print("=" * 40)
    print(f"Battery Level: {battery_info.get('BatteryCurrentCapacity', 'Unknown')}%")
    print(f"Cycle Count: {battery_info.get('CycleCount', 'Unknown')}")
    print(f"Maximum Capacity: {battery_info.get('MaximumCapacity', 'Unknown')} mAh")
    print(f"Peak Performance: {battery_info.get('PeakPower', 'Unknown')}")
    print(f"Battery State: {battery_info.get('BatteryCharging', 'Unknown')}")
    print(f"Temperature: {battery_info.get('Temperature', 'Unknown')} K")
    print(f"Voltage: {battery_info.get('Voltage', 'Unknown')} mV")
    print(f"Fully Charged: {battery_info.get('FullyCharged', 'Unknown')}")
    print(f"Charging Status: {battery_info.get('IsCharging', 'Unknown')}")
    print("=" * 40)

def main():
    """Main function to run the battery health fetcher."""
    if not check_device_connection():
        return

    raw_data = get_raw_battery_info()
    if raw_data:
        battery_info = parse_battery_info(raw_data)
        display_battery_info(battery_info)
    else:
        print("Error: Failed to retrieve iPhone\'s battery health data.")

if __name__ == "__main__":
    main()
