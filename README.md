# Set Recommended VPN Server on Synology NAS

## Description

This script automates the process of connecting your Synology NAS to the most recommended VPN server provided by NordVPN. It fetches the current top-recommended servers, checks against configured VPNs on your NAS, and connects to the best available option.

### How it Works

1. **Fetch Recommendations:** The script starts by fetching the latest recommended servers from NordVPN's API.
2. **Check Configured VPNs:** It then checks which of these recommended servers are already configured on your NAS.
3. **Connect:** If a match is found, it connects your NAS to the highest recommended server.

### Customization

Users can modify the script to change the number of recommended servers it considers by adjusting the list slicing in the `get_recommended_servers` function. For example, to consider more servers, increase the range of the list returned.

## Prerequisites

To run this script, ensure that your Synology NAS is running at least DSM 7.2 and has Python and Requests installed.

### Installing Python on DSM 7.2

To ensure the script runs smoothly on your Synology NAS, Python must be installed. Here’s how to install Python using the DSM Package Center:

1. **Access your Synology NAS via a web browser.**
2. **Open Package Center:**
   - Navigate to the main menu and click on **Package Center**.
3. **Search for Python:**
   - In the Package Center, use the search bar to search for "Python".
4. **Install Python 3:**
   - Find the Python 3 package and click **Install**. This will install Python along with its script environment.

### Installing `requests` on DSM 7.2
1. **SSH into your NAS.**
2. **Install `requests`:**
   Assuming Python is installed, you can install the `requests` library using pip. If pip is not installed, first install it:
   ```bash
   wget https://bootstrap.pypa.io/get-pip.py
   python3 get-pip.py
   ```
   Then install `requests`:
   ```bash
   pip3 install requests
   ```

### Verifying Installations

After installations, verify that `requests` can be imported successfully in your Python environment:
```bash
python3 -c "import requests; print(requests.__version__)"
```

This command should print the version of `requests` without errors, confirming it's correctly installed.

## Instructions For Use

**NB:** Modify this script to replace <USERNAME> with the user on your DSM before execution.

### Setting Up VPNs on DSM

Before using the script, you need to set up VPN profiles on your NAS. 
The VPN profiles must be named according to the servers recommended by NordVPN, e.g., `au701_nordvpn_com_upd`.

#### Steps to Configure VPNs

1. **Download Configuration Files:**
   Go to [NordVPN OVPN Configurations](https://nordvpn.com/ovpn/) and download the OpenVPN configuration files for the servers you want to use.
   
3. **Set Up VPN Profiles:**
   Follow the detailed guide provided by WunderTech on setting up NordVPN on a Synology NAS at [this link](https://www.wundertech.net/how-to-connect-to-nordvpn-on-a-synology/).

### Test Run the Script

1. **Upload the script to your NAS:** You can use any SCP client to transfer the script file to your NAS.
2. **Run the script:**
    ```bash
    python3 autoswitch-vpn.py
    ```

### Creating a Scheduled Task on Synology NAS DSM 7.2

To make the script run every 3 hours on a Synology NAS running DSM 7.2, you can follow these steps to set up a scheduled task using the Task Scheduler in the DSM Control Panel.

1. **Access DSM Control Panel**   
- **Login** to your Synology NAS via a web browser.
- Open the **Control Panel** by clicking on the menu icon in the top left corner.

2. **Open Task Scheduler**   
- In the Control Panel, locate and click on **Task Scheduler** under the **System** section.

3. **Create a New Scheduled Task**   
- Click on the **Create** button and select **Scheduled Task** followed by **User-defined script**.

4. **Configure the Task**

#### General Settings
- **Task**: Give your task a name, e.g., "Connect to Recommended VPN".
- **User**: Select **root** from the drop-down menu for sufficient permissions.

#### Task Settings
- **Run command**: Input the command to run your script, e.g.,
  ```bash
  /usr/bin/python3 /path/to/your/script/autoswitch-vpn.py
  ```

## Troubleshooting
If you encounter issues, verify that:
- VPN profiles are correctly named and configured.
- The script has the necessary permissions to execute and modify VPN configurations.
- All Python dependencies are properly installed.
- Ensure executable permissions are granted to the script: `chmod +x /path/to/your/script/autoswitch-vpn.py`
  
This setup ensures that your NAS always connects to the optimal server based on the current load, enhancing both the performance and security of your network connections.
