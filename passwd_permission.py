import os

def configure_passwd_file_permissions():
    passwd_file = "/etc/passwd-"
    
    if not os.path.exists(passwd_file):
        print(f"File '{passwd_file}' does not exist.")
        return
    
    try:
        # Set permissions to read and write only for root
        os.chmod(passwd_file, 0o600)
        
        # Set ownership to root:root
        os.chown(passwd_file, 0, 0)
        
        print("Permissions and ownership of /etc/passwd- have been configured.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
if __name__ == "__main__":
    configure_passwd_file_permissions()
