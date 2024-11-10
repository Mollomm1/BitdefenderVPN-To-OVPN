#todo
import requests

# values test, get the partner_user_token from : https://login.bitdefender.com/?redirect_url=native://com.bitdefender.vpn&lang=fr_FR 
partner_user_token = "averylongstring"
device_name = "SM-A137F"
android_id = "aaaaaaaaaa" # get your id from a real device https://stackoverflow.com/questions/5486694/getting-android-device-identifier-from-adb-and-android-sdk
app_ver = "2.2.1.146"

a = requests.post("https://nimbus.bitdefender.net/connect/login", json={
    "id": 1,
    "jsonrpc": "2.0",
    "method": "connect",
    "params": {
        "partner_user_token": partner_user_token,
        "partner_id": "com.bitdefender",
        "app_id": "com.bitdefender.vpn"
    }
}).json()

if "error" in a:
    print("[ERROR] 1 - login_connect "+str(a["error"]["message"]))
    print("Thats probably because your partner_user_token is invalid")
    exit()

user_token = a["result"]["user_token"]

b = requests.post("https://nimbus.bitdefender.net/connect/connect", json={
    "id": 1,
    "jsonrpc": "2.0",
    "method": "connect_app",
    "params": {
        "device": {
            "device_name": device_name,
            "androidid": android_id,
            "device_type": "phone",
            "device_os": "android"
        },
        "app_id": "com.bitdefender.vpn",
        "user_token": user_token
    }
}).json()

if "error" in b:
    print("[ERROR] 2 - connect_app "+str(b["error"]["message"]))
    print("Thats probably because your android_id is invalid")
    exit()

device_id = b["result"]["device_id"]

print(f'Got user and device ids!!\nuser : {user_token}\ndevice : {device_id}')

c = requests.post("https://nimbus.bitdefender.net/connect/app_mgmt", json={
    "id": 1,
    "jsonrpc": "2.0",
    "method": "report_app_state",
    "params": {
        "app_id": "com.bitdefender.vpn",
        "installed_version": app_ver,
        "result": "OK",
        "state": 1,
        "connect_source": {
            "user_token": user_token,
            "device_id": device_id,
            "app_id": "com.bitdefender.vpn"
        }
    }
}).json()

if "error" in c:
    print("[ERROR] 3 - connect_app "+str(c["error"]["message"]))
    exit()

if c["result"]["status"] == "ok":
    print("[SUCESS] login test success!")
else:
    print("[ERROR] login verification failed.")