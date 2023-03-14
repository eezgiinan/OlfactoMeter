from simple_device import SimpleDevice
device = SimpleDevice()
device.on_event('device_locked')
device.on_event('pin_entered')
device.on_event('device_locked')
