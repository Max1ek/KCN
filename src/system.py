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

def _wire_device_logging(dev, name):
    if hasattr(dev, "Connected"):
        prev_connected = dev.Connected
        def _connected(interface, state):
            try:
                if callable(prev_connected):
                    prev_connected(interface, state)
            except Exception as exc:
                ProgramLog("{} connected handler error: {}".format(name, exc), "error")
        dev.Connected = _connected

    if hasattr(dev, "Disconnected"):
        prev_disconnected = dev.Disconnected
        def _disconnected(interface, state):
            try:
                if callable(prev_disconnected):
                    prev_disconnected(interface, state)
            except Exception as exc:
                ProgramLog("{} disconnected handler error: {}".format(name, exc), "error")
            ProgramLog("{} disconnected: {}".format(name, state), "info")
        dev.Disconnected = _disconnected

    if hasattr(dev, "Send"):
        send_func = dev.Send
        def _send(data, _send=send_func):
            return _send(data)
        dev.Send = _send

    if hasattr(dev, "SendAndWait"):
        send_wait_func = dev.SendAndWait
        def _send_and_wait(data, timeout, **delimiter):
            return send_wait_func(data, timeout, **delimiter)
        dev.SendAndWait = _send_and_wait

    def _wrap_receive(target, target_name):
        if hasattr(target, "ReceiveData"):
            prev = target.ReceiveData
            if callable(prev):
                def _receive_data(interface, data, _prev=prev):
                    try:
                        _prev(interface, data)
                    except Exception as exc:
                        ProgramLog("{} receive handler error: {}".format(target_name, exc), "error")
                target.ReceiveData = _receive_data

    if hasattr(dev, "Interface"):
        _wrap_receive(dev.Interface, name)
    else:
        _wrap_receive(dev, name)

    if hasattr(dev, "ConnectFailed"):
        def _connect_failed(interface, reason):
            ProgramLog("{} connect failed: {}".format(name, reason), "error")
        dev.ConnectFailed = _connect_failed

    if hasattr(dev, "SubscribeStatus"):
        def _status_cb(command, value, qualifier):
            if command == "ConnectionStatus" and value == "Disconnected":
                ProgramLog("{} disconnected".format(name), "info")
        try:
            dev.SubscribeStatus("ConnectionStatus", None, _status_cb)
        except Exception as exc:
            ProgramLog("{} subscribe status failed: {}".format(name, exc), "error")

def Initialize():
    print('****Initialize() called')
    devTLP.ShowPage('Intro')
    devTLP.ShowPopup('PopupConnections')
    # Connect all devices    
    _wire_device_logging(devBarcoProjector, "BarcoProjector")
    _wire_device_logging(devYamahaDSP, "YamahaDSP")
    _wire_device_logging(devQuickQ, "QuickQ")
    _wire_device_logging(devCamera1, "Camera1")
    _wire_device_logging(devCamera2, "Camera2")
    _wire_device_logging(devDTP, "DTPMatrix")
    _wire_device_logging(devDMP64, "DMP64")

    devices_to_connect = [
        devDMP64,
        devBarcoProjector,
        devYamahaDSP,
        devQuickQ,
        devCamera1,
        devCamera2,
        devDTP,
    ]

    def _connect_next(index=0):
        if index >= len(devices_to_connect):
            return
        dev = devices_to_connect[index]
        if hasattr(dev, "Connect"):
            try:
                dev.Connect()
            except Exception as exc:
                ProgramLog("Connect error index {}: {}".format(index, exc), "error")
        Wait(0.5, lambda: _connect_next(index + 1))

    _connect_next(0)
    devTLP.HidePopup('PopupConnections')    
    devTLP.ShowPage('StartPage')
    # Finish Initialize() with a print()
    print('System Initialized')
