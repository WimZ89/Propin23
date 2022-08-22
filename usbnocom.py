import sys

import usb.core
import usb.util

# find our device
# dev = usb.core.find(idVendor=0x303a, idProduct=0x4001)
dev = usb.core.find(find_all=True)
for d in dev:
    print(f"{d.idVendor:X}")
    if d.idVendor == 0x303A:
        dev = d
        print(dev)
        break
        # print(d.is_kernel_driver_active(0))

# if dev.is_kernel_driver_active(i):
#     try:
#         dev.detach_kernel_driver(i)
#     except usb.core.USBError as e:
#         sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(i, str(e)))
# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
config = dev.configurations()[0]
for i in range(config.bNumInterfaces):
    print("detach",i )
    dev.detach_kernel_driver(i)
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

# write the data
ep.write('test')