import requests
import subprocess
import re
import time
import sys

# Function to fetch the recommended servers
def get_recommended_servers():
    url = 'https://nordvpn.com/wp-admin/admin-ajax.php?action=servers_recommendations'
    print("Fetching recommended servers from NordVPN")
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print("Fetched recommended servers successfully")
    return [server['hostname'].replace('.', '_') for server in data]

# Function to execute a shell command and return its output
def execute_command(command):
    print(f"Executing command: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    if result.stderr:
        print(f"Error executing command: {result.stderr.strip()}")
        sys.exit(1)
    
    print(f"Command executed successfully: {command}")
    return result.stdout.strip()

# Function to get the list of configured VPNs on the server
def get_configured_vpns():
    command = "grep -E '^conf_name=' /usr/syno/etc/synovpnclient/{l2tp,openvpn,pptp}/*client.conf 2>/dev/null"
    print("Fetching configured VPNs from NAS")
    config = execute_command(command)
    
    config_split = config.split('\n')

    vpns = []
    for line in config_split:
        match_name = re.match(r"^.*conf_name=(.*)$", line)
        if match_name:
            vpn_name = match_name.group(1)
            vpns.append(vpn_name)

    print(f"Configured VPNs: {vpns}")
    return vpns

# Function to connect to a VPN
def connect_to_vpn(vpn_name):
    print(f"Connecting to VPN: {vpn_name}")
    # Create reconnect command file
    execute_command(f"(echo conf_name={vpn_name} && echo proto=openvpn) > /usr/syno/etc/synovpnclient/vpnc_connecting")

    # Give root file permissions
    execute_command("chown devonuto:root /usr/syno/etc/synovpnclient/vpnc_connecting")

    # Call reconnection
    execute_command(f"/usr/syno/bin/synovpnc reconnect --protocol=openvpn --name={vpn_name} --keepfile")

    time.sleep(10)

    # Verify connection
    connection_status = execute_command("/usr/syno/bin/synovpnc get_conn").split('\n')

    if not any("Uptime" in status for status in connection_status):
        print(f"Failed to establish VPN connection: {connection_status}")
        sys.exit(1)

    print(f"Connected to VPN: {vpn_name}")

def main():
    try:
        recommended_servers = get_recommended_servers()
        configured_vpns = get_configured_vpns()

        if not configured_vpns:
            print("No VPNs configured on NAS.")
            return

        # Normalize server names to match the format of configured VPNs
        normalized_recommended_servers = [server.replace('.', '_') for server in recommended_servers]

        # Find the highest recommended server that is configured
        for server in normalized_recommended_servers:
            print(f"Checking if {server} is configured on the NAS")
            for vpn_name in configured_vpns:
                # Check if the server is configured
                if re.search(server, vpn_name, re.IGNORECASE):
                    print(f"Connecting to recommended server: {server}")
                    connect_to_vpn(vpn_name)
                    print(f"Successfully connected to {server}")
                    return

        print("No recommended servers are configured on the NAS: {normalized_recommended_servers}")
    except Exception as e:
        print(f"An uncaught error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
