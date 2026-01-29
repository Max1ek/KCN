"""
This is the place to put the modules for each UI in the system.  One module for each unique ui --
mirrored panels should be in the same file.
* UI object definition
* UI navigation
"""

# Python imports

# Extron Library imports
from extronlib.system import MESet, ProgramLog, Wait, RFile, Timer
from extronlib.ui import Button, Label, Slider,Level
# Project imports
from modules.helper.ModuleSupport import eventEx
from devices import devTLP as devTLP
from devices import devYamahaDSP as devYamahaDSP
from devices import devBarcoProjector as devBarcoProjector
from devices import devQuickQ as devQuickQ
from devices import devCamera1 as devCamera1
from devices import devCamera2 as devCamera2
from devices import devLiftRelay as devLiftRelay
from devices import devScreenRelay as devScreenRelay
from devices import devDMP64 as devDMP64

# Define UI Objects

# Define UI Object Events

waitbar = Level(devTLP, 53)
def handle_waitbar(timer,count):
    if count == 100:
        timer.Stop()

    waitbar.SetLevel(count)

StartAnimationTimer = Timer(0.5, handle_waitbar)





btnCinema = Button(devTLP, 2)
btnDiscusion = Button(devTLP, 3)
btnTheatre = Button(devTLP, 4)

btnProjectorStatus = Button(devTLP, 40)
labProjectorHours = Label(devTLP, 14)
btnProjectorON = Button(devTLP, 8000)
btnProjectorOFF = Button(devTLP, 13)
btnProjectorInputHdmi1 = Button(devTLP, 15)
btnProjectorInputHdmi2 = Button(devTLP, 18)
btnProjectorInputDisplayPort = Button(devTLP, 19)

projectorInputGroup = MESet([btnProjectorInputHdmi1, btnProjectorInputHdmi2, btnProjectorInputDisplayPort])
projectorInputGroup.SetCurrent(btnProjectorInputHdmi1)

projectorONoffGroup = MESet([btnProjectorON, btnProjectorOFF])


_dmp64_status = "Unknown"
_dmp64_flash_state = 0

def _dmp64_flash_timer_tick(timer, count):
    _toggle_dmp64_status_flash()

_dmp64_flash_timer = Timer(0.5, _dmp64_flash_timer_tick)
_dmp64_flash_timer.Pause()

def _set_projector_status_state(state):
    btnProjectorStatus.SetState(state)

def _start_dmp64_flash():
    if _dmp64_flash_timer.State != "Running":
        _dmp64_flash_timer.Restart()

def _stop_dmp64_flash():
    if _dmp64_flash_timer.State == "Running":
        _dmp64_flash_timer.Pause()

def _toggle_dmp64_status_flash():
    global _dmp64_flash_state
    _dmp64_flash_state = 0 if _dmp64_flash_state == 1 else 1
    _set_projector_status_state(_dmp64_flash_state)

def _update_dmp64_status(command, value, qualifier):
    global _dmp64_status
    _dmp64_status = value

    if value == "Connected":
        _stop_dmp64_flash()
        _set_projector_status_state(1)
    elif value == "Disconnected":
        _stop_dmp64_flash()
        _set_projector_status_state(0)
    else:
        _start_dmp64_flash()

try:
    devDMP64.SubscribeStatus("ConnectionStatus", None, _update_dmp64_status)
    _start_dmp64_flash()
except Exception as exc:
    ProgramLog("DMP64 SubscribeStatus failed: {}".format(exc), "error")

def _attach_dmp64_event_handlers():
    if hasattr(devDMP64, "Connected"):
        prev_connected = devDMP64.Connected
        def _connected(interface, state):
            try:
                if callable(prev_connected):
                    prev_connected(interface, state)
            except Exception as exc:
                ProgramLog("DMP64 connected handler error: {}".format(exc), "error")
            _stop_dmp64_flash()
            _set_projector_status_state(1)
        devDMP64.Connected = _connected

    if hasattr(devDMP64, "Disconnected"):
        prev_disconnected = devDMP64.Disconnected
        def _disconnected(interface, state):
            try:
                if callable(prev_disconnected):
                    prev_disconnected(interface, state)
            except Exception as exc:
                ProgramLog("DMP64 disconnected handler error: {}".format(exc), "error")
            _stop_dmp64_flash()
            _set_projector_status_state(0)
        devDMP64.Disconnected = _disconnected

_attach_dmp64_event_handlers()

def _attach_dmp64_rx_handler():
    if hasattr(devDMP64, "Interface"):
        iface = devDMP64.Interface
    else:
        iface = devDMP64

    if hasattr(iface, "ReceiveData"):
        prev_rx = iface.ReceiveData
        if callable(prev_rx):
            def _rx(interface, data):
                try:
                    prev_rx(interface, data)
                except Exception as exc:
                    ProgramLog("DMP64 rx handler error: {}".format(exc), "error")
                if _dmp64_status != "Connected":
                    _stop_dmp64_flash()
                    _set_projector_status_state(1)
            iface.ReceiveData = _rx

_attach_dmp64_rx_handler()

@eventEx(projectorInputGroup.Objects,'Pressed')
def projectorInputGroup_Pressed(button:Button, state:str):
    projectorInputGroup.SetCurrent(button)

btnLifUp = Button(devTLP, 10)
btnLiftDown = Button(devTLP, 9)
btnScreenDown = Button(devTLP, 23)
btnScreenUp = Button(devTLP, 24)

_startup_lock = True

def _startup_timer_tick(timer, count):
    if _startup_lock:
        devTLP.ShowPage('StartPage')

_startup_timer = Timer(1, _startup_timer_tick)
_startup_timer.Restart()

_all_buttons = [
    btnCinema,
    btnDiscusion,
    btnTheatre,
    btnProjectorStatus,
    btnProjectorON,
    btnProjectorOFF,
    btnProjectorInputHdmi1,
    btnProjectorInputHdmi2,
    btnProjectorInputDisplayPort,
    btnLifUp,
    btnLiftDown,
    btnScreenDown,
    btnScreenUp,
]

@eventEx(btnCinema, 'Pressed')
@eventEx(btnDiscusion, 'Pressed')
@eventEx(btnTheatre, 'Pressed')
def show_main_page(button: Button, state: str):
    global _startup_lock
    if state != "Pressed":
        return
    _startup_lock = False
    if _startup_timer.State == "Running":
        _startup_timer.Pause()
    if button == btnCinema:
        projectorInputGroup.SetCurrent(btnProjectorInputHdmi1)
        yamahaPresetGroup.SetCurrent(btnYamahaPreset1)
        quickQ30PresetGroup.SetCurrent(btnQuickQ30Preset1)
        projectorONoffGroup.SetCurrent(btnProjectorON)
       # btnProjectorON.SetState(1)
    elif button == btnDiscusion:
        projectorInputGroup.SetCurrent(btnProjectorInputHdmi2)
        yamahaPresetGroup.SetCurrent(btnYamahaPreset2)
        quickQ30PresetGroup.SetCurrent(btnQuickQ30Preset2)
        projectorONoffGroup.SetCurrent(None)
    elif button == btnTheatre:
        projectorInputGroup.SetCurrent(btnProjectorInputDisplayPort)
        projectorONoffGroup.SetCurrent(None)
    devTLP.ShowPage('MainPage')



btnCamera1Preset1 = Button(devTLP, 27)
btnCamera1Preset2 = Button(devTLP, 25)
btnCamera1Preset3 = Button(devTLP, 26)

camera1Group = MESet([btnCamera1Preset1, btnCamera1Preset2, btnCamera1Preset3])
@eventEx(camera1Group.Objects,'Pressed')
def camera1Group_Pressed(button:Button, state:str):
    camera1Group.SetCurrent(button)

btnCamera2Preset1 = Button(devTLP, 44)
btnCamera2Preset2 = Button(devTLP, 42)  
btnCamera2Preset3 = Button(devTLP, 43)

camera2Group = MESet([btnCamera2Preset1, btnCamera2Preset2, btnCamera2Preset3])
@eventEx(camera2Group.Objects,'Pressed')    
def camera2Group_Pressed(button:Button, state:str):
    camera2Group.SetCurrent(button)

btnYamahaPreset1 = Button(devTLP, 31)
btnYamahaPreset2 = Button(devTLP, 29)
btnYamahaPreset3 = Button(devTLP, 30)
yamahaPresetGroup = MESet([btnYamahaPreset1, btnYamahaPreset2, btnYamahaPreset3])
@eventEx(yamahaPresetGroup.Objects,'Pressed')
def yamahaPresetGroup_Pressed(button:Button, state:str):
    yamahaPresetGroup.SetCurrent(button)
    if button == btnYamahaPreset1:
        devYamahaDSP.RecallPreset(1)
    elif button == btnYamahaPreset2:
        devYamahaDSP.RecallPreset(2)
    elif button == btnYamahaPreset3:
        devYamahaDSP.RecallPreset(3)

btnQuickQ30Preset1 = Button(devTLP, 35)
btnQuickQ30Preset2 = Button(devTLP, 33)
btnQuickQ30Preset3 = Button(devTLP, 34)
quickQ30PresetGroup = MESet([btnQuickQ30Preset1, btnQuickQ30Preset2, btnQuickQ30Preset3])
@eventEx(quickQ30PresetGroup.Objects,'Pressed')
def quickQ30PresetGroup_Pressed(button:Button, state:str):
        quickQ30PresetGroup.SetCurrent(button)
        if button == btnQuickQ30Preset1:
            devQuickQ.RecallPreset(1)
        elif button == btnQuickQ30Preset2:
            devQuickQ.RecallPreset(2)
        elif button == btnQuickQ30Preset3:
            devQuickQ.RecallPreset(3)


btnStatus = Button(devTLP, 20)
@eventEx(btnStatus, 'Pressed')
def btnStatus_Pressed(btnStatus:Button, state:str):
    devTLP.ShowPopup('ModalPopup')
    

btnClosePopup = Button(devTLP, 80)
@eventEx(btnClosePopup, 'Pressed')
def btnClosePopup_Pressed(btnClosePopup:Button, state:str):
    if state != "Pressed":
        return
    devTLP.HidePopup('ModalPopup')


homeBtn = Button(devTLP, 8022)
@eventEx(homeBtn, 'Pressed')
def homeBtn_Pressed(homeBtn:Button, state:str):
    camera2Group.SetCurrent(None)
    camera1Group.SetCurrent(None)
    yamahaPresetGroup.SetCurrent(None)
    quickQ30PresetGroup.SetCurrent(None)
    devTLP.ShowPage('StartPage')   

_all_buttons.extend([
    btnCamera1Preset1,
    btnCamera1Preset2,
    btnCamera1Preset3,
    btnCamera2Preset1,
    btnCamera2Preset2,
    btnCamera2Preset3,
    btnYamahaPreset1,
    btnYamahaPreset2,
    btnYamahaPreset3,
    btnQuickQ30Preset1,
    btnQuickQ30Preset2,
    btnQuickQ30Preset3,
    btnStatus,
    btnClosePopup,
    homeBtn,
])

@eventEx(_all_buttons, 'Pressed')
def log_button_pressed(button: Button, state: str):
    return
