# Bootloader Script

import subprocess, os

def set_bootloader_password(password, re_password, username):
	# Generate Password Hash
	input_data = f"{password}\n{re_password}"
	process = subprocess.run(['grub-mkpasswd-pbkdf2'], capture_output=True, text=True, input=input_data, shell=True)
	password_hash = process.stdout.split()

	# Set Bootloader Username and Password
	command_echo = f'sudo echo "set superusers={username}" | tee -a /etc/grub.d/40_custom && echo "password_pbkdf2 {username} {password_hash[10]}" | tee -a /etc/grub.d/40_custom'
	process_echo = subprocess.run(command_echo, capture_output=True, text=True, shell=True)
	print(process_echo.stdout)
    # Update GRUB
	process_update = subprocess.run(['update-grub'], capture_output=True, text=True, shell=True)
	print(process_update.stderr)
	print(process_update.stdout)




uid = os.getuid()

def run_bootloader_script():
	if uid == 0:
		username = input("Enter Username: ")
		password = input("Enter Password: ")
		re_password = input("Re-Enter Password: ")
		set_bootloader_password(password, re_password, username)
	else:
		print("Please run the script as root")
		

# Deny IP Forwarding Script

def check_ip_forwarding_status():
    try:
        ipv4_forwarding = subprocess.run(['sysctl', '-n', 'net.ipv4.ip_forwarding'], text=True, capture_output=True)
        ipv6_forwarding = subprocess.run(['sysctl', '-n', 'net.ipv6.conf.all.forwarding'], text=True, capture_output=True)
        if ipv4_forwarding.stdout.strip() == "0" and ipv6_forwarding.stdout.strip() == "0":
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False
    
def disable_ip_forwarding():
    try:
        set_ipv4_forwarding = subprocess.run(['sudo', 'sysctl', '-w', 'net.ipv4.ip_forward=0'], text=True, capture_output=True)
        set_ipv6_forwarding = subprocess.run(['sudo', 'sysctl', '-w', 'net.ipv6.conf.all.forwarding=0'], text=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False
def run_ip_forwarding_script():
    if uid == 0:
        print("Verifying IP Forwarding Status")
        if check_ip_forwarding_status():
            print("IP Forwarding Is Already Disabled")
        else:
            print("IP Forwarding Is Not Disabled")
            if disable_ip_forwarding():
                print("IP Forwarding Has Been Successfully Disabled")
            else:
                print("Failed To Disable IP Forwarding")
    else:
        print("Run The Script As Root")

# Configure ufw Script

def check_ufw_installed():
    try:
        command_check = f"dpkg -l | grep ufw"
        ufw_check = subprocess.run(command_check, capture_output=True, text=True, shell=True)
        if not ufw_check:
            print("ufw not installed")
            print("ufw installing...")
            command_update = f"apt-get update"
            command_install = f"apt-get install -y ufw"
            ufw_update = subprocess.run(command_update, capture_output=True, text=True, shell=True)
            ufw_install = subprocess.run(command_install, capture_output=True, text=True, shell=True)
            print("ufw successfully installed")
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
            print("ufw loopback successfully configured")
        else:
            print("ufw loopback traffic is already configured")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    return True

def run_install_ufw_script():
    if uid == 0:
        check_ufw_installed()
    else:
        print("Run the script as root")

def run_enable_ufw_script():
    if uid == 0:
        enable_ufw()
    else:
        print("Run the script as root")

def run_configure_loopback_script():
    if uid == 0:
        configure_loopback()
    else:
        print("Run the script as root")

if __name__ == "__main__":
    print("Please choose an option to run the benchmark")
    print("1. Set Bootloader Password")
    print("2. Disable IP Forwarding")
    print("3. Install ufw")
    print("4. Enable ufw")
    print("5. Configure loopback IP")
    option = int(input("Choose option: "))
    option_functions = {
    1: run_bootloader_script,
    2: run_ip_forwarding_script,
    3: run_install_ufw_script,
    4: run_enable_ufw_script,
    5: run_configure_loopback_script,
}

if option in option_functions:
    option_functions[option]()
else:
    print("Please choose a valid option!")

    
