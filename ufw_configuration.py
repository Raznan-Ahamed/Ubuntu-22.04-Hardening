import subprocess, os

def check_ufw_installed():
    try:
        command_check = f"dpkg -l | grep ufw"
        ufw_check = subprocess.run(command_check, capture_output=True, text=True, shell=True)
        if not ufw_check:
            print("ufw not installed")
            command_update = f"apt-get update"
            command_install = f"apt-get install -y ufw"
            ufw_update = subprocess.run(command_update, capture_output=True, text=True, shell=True)
            ufw_install = subprocess.run(command_install, capture_output=True, text=True, shell=True)
        else:
            print("ufw is already installed")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    return True


def enable_ufw():
    try:
        command_check = f"systemctl is-enabled ufw"
        ufw_check = subprocess.run(command_check, text=True, capture_output=True, shell=True)
        if ufw_check:
            print("ufw service is already enabled")
        else:
            print("Enabling ufw service...")
            command_enable = f"systemctl enable ufw"
            ufw_enable = subprocess.run(command_enable, text=True, capture_output=True, shell=True)
            print("ufw enabled")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    return True


def configure_loopback():
    try:
        command_check = f"ufw status | grep 'Anywhere on lo'"
        lo_check = subprocess.run(command_check, text=True, capture_output=True, shell=True)
        if not lo_check:
            print("Configuring ufw loopback traffic...")
            command_lo_in = f"ufw allow in on lo"
            command_lo_out = f"ufw allow out on lo"
            lo_in = subprocess.run(command_lo_in, text=True, capture_output=True, shell=True)
            lo_out = subprocess.run(command_lo_out, text=True, capture_output=True, shell=True)
        else:
            print("ufw loopback traffic is already configured")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    return True

uid = os.getuid()

if uid == 0:
    check_ufw_installed()
    enable_ufw()
    configure_loopback()
else:
    print("Run the script as root")