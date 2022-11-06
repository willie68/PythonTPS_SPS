import usb_cdc
import storage
#enable extra usb serial output
usb_cdc.enable(console=True, data=True)
#internal drive read/write
storage.remount("/", False)