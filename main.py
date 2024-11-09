import requests, argparse

# you can change those to anything, the endpoint don't seems to care.
app_version = "6.9"
sdk_version = "4.2.0"

parser = argparse.ArgumentParser(
    prog='BitdefenderVPN To OVPN',
    description='Generate ovpn configs from Bitdefender VPN, don\'t need the vpn client installed and works anywhere including linux.',
    epilog='')

parser.add_argument('-t', '--token', required=True, help='Access token for Bitdefender VPN')
parser.add_argument('-l', '--location', required=False, default="france-paris", help='Location for the VPN connection (default is france-paris)')
parser.add_argument('-p', '--protocol', required=False, default="tcp", choices=['tcp', 'udp'], help='Protocol for the VPN connection (tcp or udp, default is tcp)')

args = parser.parse_args()

access_token = args.token
location = args.location
openvpn_protocol = args.protocol

# idk why the domain is that sus, and it is an official thing https://community.bitdefender.com/en/discussion/98276/bitdefender-vpn-and-host-file.
req = requests.get(f'https://1uzxr3b3jraw5nlmnvbsikiioud2vilw5.web-networking.com/user/provide?access_token={access_token}&app_version={app_version}&sdk_version={sdk_version}&location={location}&ipaddr=false&type=openvpn-{openvpn_protocol}&config_version=')
jsondata = req.json()

if jsondata["result"] == "OK":
    print("[INFO] Got configuration infos")
    template = open("ovpn.template", "r")
    filedata = template.read().replace("replace_protocol", openvpn_protocol)
    filedata = filedata.replace("replace_ip", str(jsondata["servers"][0]["address"]))
    filedata = filedata.replace("replace_port", str(jsondata["servers"][0]["port"]))
    filedata = filedata.replace("replace_cert", str(jsondata["openvpn_cert"]))
    template.close()
    output = open("Bitdefender.ovpn", "w")
    output.write(filedata)
    output.close()
    print("[SUCCESS] Generating the openvpn/auth configuration done.")
    print(f'\nUsername : {jsondata["username"]}\nPassword : {jsondata["password"]}\nSaved as Bitdefender.ovpn\n> Friendly reminder: those are only valid for 24 hours.\n')
elif jsondata["result"] == "SERVER_UNAVAILABLE":
    print("[INFO] Invalid location or protocol")
elif jsondata["result"] == "NOT_AUTHORIZED":
    print("[ERROR] INVALID TOKEN Provided")
else:
    print("[ERROR] "+jsondata["result"])