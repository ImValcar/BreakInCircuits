import usb_cdc, usb_hid, storage, supervisor
supervisor.runtime.autoreload = False
usb_hid.enable((usb_hid.Device.KEYBOARD,))
supervisor.set_usb_identification("KU-0316 Keyboard","HP. Inc",0x03F0,0x0036) # Las hardware IDs se pueden obtener de -> http://www.linux-usb.org/usb-ids.html
print("Fully booted")
