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
kbd = Keyboard(devices)
layout = KeyboardLayoutUS(kbd)
keycodes={"cmd":227, "ctrl":224, "shift":225, "alt":226, "altgr":230,"enter":40, "del":42, "supr":76, "tab":43, "larrow":80, "rarrow":79, "uarrow":82, "darrow":81}

def run_client(data, pool):
    data=b'\x0f\x00\x00\x00'.decode('utf-8')+data
    client = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    client.settimeout(300)
    try:
        client.connect((HOST,PORT))
        print("Client connected to server")
        client.send(data)
        response=bytearray(256)
        while True:
            client.recv_into(response)
            signature=response[:4]
            if signature == b'\x0f\x00\x00\x00':
                client.close()
                break
            elif signature == b'\x02\x00\x00\x00':
                message = response[4:].strip(b'\x00').split(b'\xff\xff')[0]
                message = message.decode('utf-8')
                print("Writing " + message + " to host.")
                parseKeys(message)
            elif signature == b'\x03\x00\x01\x07':
                client.close()
                print("Connection to server closed by remote host")
            print(f"Received: {response}")
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
while True:
    while not wifi.radio.connected:
        print("Connecting to wifi")
        try:
            wifi.radio.connect(AP_NAME,AP_PASSWORD)
            if wifi.radio.connected:
                print("Connected")
                break
        except:
            pass
        sleep(15)
    pool=SocketPool(wifi.radio)
    ap=wifi.radio.ap_info
    stime=run_client(f'{getenv("id")};{wifi.radio.ipv4_address};{ap.ssid};{ap.bssid.hex()}', pool)
    sleep(stime)
