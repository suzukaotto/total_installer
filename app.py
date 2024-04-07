import os
import sys
import time
import requests

from func import *

def wg_install() -> int:
    if platform_name == "Windows":
        url = "https://download.wireguard.com/windows-client/wireguard-installer.exe"
        save_path = "./wg-installer.exe"

        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            downloaded = 0

            file = open(save_path, 'wb')
            for data in response.iter_content(block_size):
                downloaded += len(data)
                file.write(data)
                progress = downloaded / total_size * 100
                print(f"Downloading . . . ({progress:.2f}%)", end='\r')

            # line break
            print("")

            print("Installing . . . ")
            file.close()
            os.system("wg-installer.exe")
            os.remove(save_path)
            os.environ['PATH'] += os.pathsep + r"C:\Program Files\WireGuard"
            print("Wireguard Install Successfully")
            return 0
        except KeyboardInterrupt:
            return 5
        except Exception as e:
            print(e)
            return 1
    else:
        print("Other than Windows operating systems are not yet supported.")
        return 1
        # ~~
        

alert_msg = None
def main():
    global alert_msg
    
    clear()
    print(f"[{program_title}]")
    print(f"{platform_name} {platform_ver}")
    
    # message print
    ## wireguard installed check
    if get_wg_installed() == True:
        os.system("wg --version")
    else:
        print("WireGuard is not installed")
    
    ## admin check
    if is_admin() == False:
        print("Do not administrator privileges.")

    print(f"========================================")
    
    # Restart with administrator privileges
    ## Windows platform
    if is_admin() == False:
        if platform_name == "Windows":
            print("Running again with administrator privileges(Windows) . . . ")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()

    print("1. WireGuard Install")
    print("3. Program Exit")
    
    
    # menu select
    try:
        sel_menu = input("> ")
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        print()
        program_exit()
        return 1
    print("") # line brake

    # menu 0
    if sel_menu == '1':
        clear()
        print("[ WireGuard install page ]")

        # wireguard install check
        if get_wg_installed() == True:
            print("WireGuard is already installed.")
            print("")
            pause()
            return 1

        if ques_tf("Do you want to install WireGuard? [Y/N]: ") == False:
            alert_msg = "Canceled the WireGuard installation."
            return 1
        
        print()
        wg_install_rst = wg_install()
        print()

        if wg_install_rst == 0:
            print("Successfully installed WireGuard.")
        elif wg_install_rst == 1:
            print("! Installation failed.")
        elif wg_install_rst == 4:
            print("! Check your internet connection.")
        elif wg_install_rst == 5:
            print("! Installation has been cancelled.")

        print()
        pause()

        return 0
    
    # menu 5
    elif sel_menu == '3':
        program_exit()
    
    return 1

if __name__ == '__main__':
    while True:
        main()