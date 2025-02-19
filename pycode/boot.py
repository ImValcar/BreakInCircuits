import usb_cdc, usb_hid, storage, supervisor
supervisor.runtime.autoreload = False
usb_hid.enable((usb_hid.Device.KEYBOARD))
print("Fully booted")
