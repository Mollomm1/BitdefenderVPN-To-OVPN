no gramarly for u

check [login.py](login.py) for a working example.

# token collecting related stuff

https://login.bitdefender.com/?redirect_url=native://com.bitdefender.vpn&lang=fr_FR 

use a android webview user agent like, i recommand using firefox devtools for this. : `Mozilla/5.0 (Linux; Android 14; SM-A137F Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.86 Mobile Safari/537.36`

after logging (even if you are stuck in password input) in your request tab you should see the /v1/user/signin endpoint the request body should look something like this.
```json
{
    "pass":"YOURPASSWORDINBLANK",
    "fingerprint":"aaaaaaaaaaaaaaaa",
    "redirect_url":"native://com.bitdefender.vpn",
    "partner_id":"com.bitdefender",
    "token":"aaaaaaaaaaaaaaaaaaa",
    "lang":"fr_FR",
    "refresh_code_challenge":"aaaaaaaaaaaaaaaaa",
    "timestamp":10000000,
    "trust_token":"aaaaaaaaaaaaaaaa"}
```

and the response one
```json
{
    "user_token":"partner_user_token",
    "status":"ok",
    "account":"active",
    "remember":false,
    "usage":"login",
    "fullname":"Username",
    "redirect_url":"native://com.bitdefender.vpn?user_token=partner_user_token&status=ok&account=active&remember=false&usage=login&lang=fr_FR"
}
```

the most important part is the partner_user_token from the response, next we need to get a user id and device id (it will add your device as a new one, it will count in the devices limit).

make post request to **https://nimbus.bitdefender.net/connect/login**

with this as body
```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "connect",
  "params": {
    "partner_user_token": "the partner_user_token you got before",
    "partner_id": "com.bitdefender",
    "app_id": "com.bitdefender.vpn"
  }
}
```

and you should recive your user-token like this in the response

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": {
    "user_token": "aaaaaa-aaaa-aaaa-aaa-aaaaaa"
  }
}
```

now do a post req to https://nimbus.bitdefender.net/connect/connect with the following as body:

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "connect_app",
  "params": {
    "device": {
      "device_name": "SM-A137F", // your android phone model name
      "androidid": "z2jd32kr45", // get your id from a real device https://stackoverflow.com/questions/5486694/getting-android-device-identifier-from-adb-and-android-sdk
      "device_type": "phone",
      "device_os": "android"
    },
    "app_id": "com.bitdefender.vpn",
    "user_token": "the user token you got from the connect request"
  }
}
```

and as response you should get:
```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": {
    "device_id": "aaaaaa-aaaa-aaaa-aaa-aaaaaa"
  }
}
```

now you should have:
* your (final) user token.
* your device id

next register your device by doing a post request to https://nimbus.bitdefender.net/connect/app_mgmt

request body:
```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "report_app_state",
  "params": {
    "app_id": "com.bitdefender.vpn",
    "installed_version": "2.2.1.146", // android app ver
    "result": "OK",
    "state": 1,
    "connect_source": {
      "user_token": "your user token",
      "device_id": "your device id",
      "app_id": "com.bitdefender.vpn"
    }
  }
}
```

response body:
```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": {
    "status": "ok"
  }
}
```

if everything right it should return with status OK

from there you can get few other detaills like Username and email with the (POST) https://nimbus.bitdefender.net/connect/user_info endpoint.

req body:
```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "getInfo",
  "params": {
    "connect_source": {
      "user_token": "your user token",
      "device_id": "your device id",
      "app_id": "com.bitdefender.vpn"
    }
  }
}
```

resp body:
```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": {
    "beta_enabled": 0,
    "beta_available": 0,
    "lastname": "",
    "firstname": "Name",
    "email": "abc@gmail.com",
    "country": "FR",
    "lang": "en_US",
    "subs_version": 4,
    "newsletter": {
      "viaProduct": {
        "receiveThreatsInsights": true,
        "receiveNews": true,
        "receiveOffers": true
      },
      "viaEmail": {
        "receiveThreatsInsights": true,
        "receiveNews": true,
        "receiveOffers": true
      }
    },
    "two_fa_enabled": false,
    "user_status": "active",
    "created_ts": 10000000,
    "ext_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "ext_id2": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "fingerprint": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "current_context_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "primary_context_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "groups": [],
    "status": 0
  }
}
```

there is also (POST) https://nimbus.bitdefender.net/connect/subscription to get sub info

req body:
```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "check",
  "params": {
    "format": "v4",
    "connect_source": {
      "user_token": "your user token",
      "device_id": "your device id",
      "app_id": "com.bitdefender.vpn"
    }
  }
}
```

resp body:
```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": {
    "app_id": "com.bitdefender.vpn",
    "countable": 1,
    "last_update": 1000000,
    "service_id": "aaaaaaaaaaaaaaaa",
    "bundle_id": "com.bitdefender.vpn",
    "metadata": {},
    "type": "free",
    "commercial_id": "aaaaaaaaaaaaaaaa",
    "app_params": {
      "level": "basic",
      "connections": 10
    },
    "end_date": 1000000,
    "bundle_friendly_name": "Bitdefender VPN",
    "life_cycle": "recurrent",
    "status": 0,
    "slots": 10,
    "server_time": 1000000,
    "active_slots": 2,
    "subs_version": 4
  }
}
```

i will continue this doc later.

![hi](https://media1.tenor.com/m/UasR8ee7MDsAAAAC/youtube-phone.gif "")