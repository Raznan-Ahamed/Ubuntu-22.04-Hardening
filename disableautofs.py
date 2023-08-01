import subprocess
def disable_automount():
    try:
        # Disable the automount service
        subprocess.check_call(['systemctl', 'disable', 'autofs'])

        # Stop the automount service if it is currently running
        subprocess.check_call(['systemctl', 'stop', 'autofs'])

        print("Automounting has been disabled.")

    except subprocess.CalledProcessError as e:
        print(f"Failed to disable automounting: {e}")
        return False
    return True
if __name__ == "__main__":
    disable_automount()    exit(f"Failed to remove autofs package. {str(e)}")

print("Autofs has been disabled and removed.")
