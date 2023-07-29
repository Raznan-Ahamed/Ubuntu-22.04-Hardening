import subprocess, shlex, os

def set_bootloader_password(password, re_password, username):
	# Generate Password Hash
	input_data = f"{password}\n{re_password}"
	process = subprocess.run(['grub-mkpasswd-pbkdf2'], capture_output=True, text=True, input=input_data)
	password_hash = process.stdout.split()

	# Set Bootloader Username and Password
	command_echo = f'sudo echo "set superusers={username}"  | tee -a /etc/grub.d/40_custom && echo "password_pbkdf2 {username} {password_hash[10]}"  | tee -a /etc/grub.d/40_custom'
	process_echo = subprocess.run(command_echo, capture_output=True, text=True)
	print(process_echo.stdout)
    # Update GRUB
	process_update = subprocess.run(['update-grub'], capture_output=True, text=True)




uid = os.getuid()

if uid == 0:
	username = input("Enter Username: ")
	password = input("Enter Password: ")
	re_password = input("Re-Enter Password: ")
	set_bootloader_password(password, re_password, username)	
else:
	print("Please run the script as root")