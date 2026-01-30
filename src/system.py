"""
The system is the place to define system logic, automation, services, etc. as a whole.  It should
provide an *Initialize* method that will be called in main to start the start the system after
variables, devices, and UIs have been defined.

Examples of items in the system file:
* Clocks and scheduled things
* Connection of devices that need connecting
* Set up of services (e.g. ethernet servers, CLIs, etc.)
"""

# Python imports

# Extron Library imports
from extronlib.system import ProgramLog, Wait
from modules.helper.ModuleSupport import eventEx, GenericEvent

# Project imports
from devices import (
    devIPCP,
    devTLP,
    devBarcoProjector,
    devYamahaDSP,
    devQuickQ,
    devCamera1,
    devCamera2,
    devDTP,
    devDMP64,
)

from variables import (
    IP_BARCO_PROJECTOR, IP_YAMAHA_DSP, IP_QUICKQ,
    IP_CAMERA1, IP_CAMERA2, IP_DTP_MATRIX, IP_DMP64,
)

class MyDevice:
    def __init__(self, name, ip, state=0):
        self.name = name
        self.ip = ip
        self.state = state
        self.StateChanged = GenericEvent('Device {} State Changed'.format(name))

     # ----- Getters -----
    def get_name(self):
        return self.name

    def get_ip(self):
        return self.ip

    def get_state(self):
        return self.state
    
    # ----- Updaters -----
    def update(self, name=None, ip=None, state=None):
        if name is not None:
            self.name = name
        if ip is not None:
            self.ip = ip
        if state is not None:
            self.state = state
            self.StateChanged.Trigger(state)  # Trigger event when state changes

    def __repr__(self):
        return 'Device(name={}, ip={}, state={})'.format(self.name, self.ip, self.state)
    
DEVICE_CONFIG = [
    ('DMP64', devDMP64, IP_DMP64),
    ('YamahaQL5', devYamahaDSP, IP_YAMAHA_DSP),
    ('BarcoProjector', devBarcoProjector, IP_BARCO_PROJECTOR),
    ('QuickQ30', devQuickQ, IP_QUICKQ),
    ('Camera1', devCamera1, IP_CAMERA1),
    ('Camera2', devCamera2, IP_CAMERA2),
    ('DTP Crosspoint 82', devDTP, IP_DTP_MATRIX),
]

myDevices = [MyDevice(name, ip, 0) for name, _, ip in DEVICE_CONFIG]
_ui_unlocked = False

def _register_device_events(dev, device_obj):
    def _unlock_ui_once():
        global _ui_unlocked
        if _ui_unlocked:
            return
        _ui_unlocked = True
        Wait(2, lambda: devTLP.HidePopup('PopupConnections'))
        Wait(2, lambda: devTLP.ShowPage('StartPage'))

    def _connected(interface, state, _device=device_obj):
        _device.update(state=1)
        _unlock_ui_once()

    def _disconnected(interface, state, _device=device_obj):
        ProgramLog('{} disconnected'.format(_device.get_name()), 'info')
        _device.update(state=0)

    def _connect_failed(interface, reason, _device=device_obj):
        ProgramLog('{} connect failed: {}'.format(_device.get_name(), reason), 'error')
        _device.update(state=0)

    eventEx(dev, 'Connected')(_connected)
    eventEx(dev, 'Disconnected')(_disconnected)
    try:
        eventEx(dev, 'ConnectFailed')(_connect_failed)
    except Exception:
        pass


def Initialize():
    print('****Initialize() called')
    
    # Register event handlers BEFORE connecting devices
    for idx, (_, dev, _) in enumerate(DEVICE_CONFIG):
        _register_device_events(dev, myDevices[idx])

    # Connect all devices
    devices_to_connect = [dev for _, dev, _ in DEVICE_CONFIG]

    def _connect_next(index=0):
        if index >= len(devices_to_connect):
            if not _ui_unlocked:                                
                Wait(2, lambda: devTLP.HidePopup('PopupConnections'))
                Wait(2, lambda: devTLP.ShowPage('StartPage'))

            print('System Initialized - All connections attempted')
            return
        
        dev = devices_to_connect[index]
        if hasattr(dev, "Connect"):
            try:
                dev.Connect()
            except Exception as exc:
                ProgramLog("Connect error index {}: {}".format(index, exc), "error")
        Wait(0.5, lambda: _connect_next(index + 1))

    _connect_next(0)
