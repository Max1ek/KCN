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
from system import myDevices

# Define UI Objects

# Define UI Object Events

waitbar = Level(devTLP, 53)
def handle_waitbar(timer,count):
    if count == 100:
        timer.Stop()

    waitbar.SetLevel(count)

StartAnimationTimer = Timer(0.5, handle_waitbar)


labProjector = Label(devTLP, 21).SetText('{}'.format(myDevices[2].name))
labProjectorIp = Label(devTLP, 38).SetText('{}'.format(myDevices[2].ip))
labProjectorState = Button(devTLP, 48).SetState((myDevices[2].state))

labYamahaQL5 = Label(devTLP, 36).SetText('{}'.format(myDevices[1].name))
labYamahaQL5Ip = Label(devTLP, 39).SetText('{}'.format(myDevices[1].ip))
labYamahaQL5State = Button(devTLP, 49).SetState((myDevices[1].state))

labDMP64 = Label(devTLP, 37).SetText('{}'.format(myDevices[0].name))
labDMP64Ip = Label(devTLP, 45).SetText('{}'.format(myDevices[0].ip))
labDMP64State = Button(devTLP, 50)
labDMP64State.SetState(myDevices[0].state)

@eventEx(myDevices[0].StateChanged, 'Triggered')
def handle_dmp64_state_changed(src, state):
    labDMP64State.SetState(state)
    ProgramLog('DMP64 state updated to: {}'.format(state), 'info')



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
