import requests, uuid, json
from time import sleep
from seleniumwire2 import webdriver
from selenium.webdriver.firefox.options import Options

android_id = "aaaaaaaaaaa" # get your id from a real device https://stackoverflow.com/questions/5486694/getting-android-device-identifier-from-adb-and-android-sdk
device_name = "SM-A137F" # change this to your phone model

def get_user(partner_user_token, device_name, android_id):
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
        return({"user_token": user_token, "device_id": device_id})
    else:
        print("[ERROR] login verification failed.")
        exit()

options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)
partner_user_token = ""

def interceptor(request):
    global partner_user_token
    request.headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 14; SM-A137F Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.86 Mobile Safari/537.36"
    if request.method == "POST" and request.url == "https://api.login.bitdefender.com/v1/user/signin":
        data = json.loads(request.body.decode("utf-8"))
        reciv = requests.post("https://api.login.bitdefender.com/v1/user/signin", json=data, headers=request.headers)
        customdata = reciv.json()
        partner_user_token = customdata["user_token"]
        request.create_response(
            status_code=reciv.status_code,
            headers=reciv.headers,
            json=customdata
        )

driver.request_interceptor = interceptor
driver.get('https://login.bitdefender.com/central/login.html?lang=fr_FR&redirect_url=native:%2F%2Fcom.bitdefender.vpn')
request = driver.wait_for_request("https://api.login.bitdefender.com/v2/user/refresh", timeout=9999999)
driver.close()
user = get_user(partner_user_token, device_name, android_id)

with open('user.json', 'w') as f:
    json.dump(user, f)

print("goodbye!")