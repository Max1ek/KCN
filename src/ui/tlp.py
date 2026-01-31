"""
This is the place to put the modules for each UI in the system.  One module for each unique ui --
mirrored panels should be in the same file.
* UI object definition
* UI navigation
"""

# Python imports

# Extron Library imports
from extronlib.system import MESet, ProgramLog, Wait, RFile, Timer
from extronlib.ui import Button, Label, Level
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

import control.projectorControl as controlProjector
import control.yamahaControl as controlYamaha
import ui.tlpProjector as tlpProjector
import ui.tlpCamera as tlpCamera
import ui.tlpYamaha as tlpYamaha
import ui.tlpQuickQ as tlpQuickQ


# Define UI Objects

# Define UI Object Events

waitbar = Level(devTLP, 53)
def handle_waitbar(timer,count):
    if count == 100:
        timer.Stop()

    waitbar.SetLevel(count)

StartAnimationTimer = Timer(0.5, handle_waitbar)

labDMP64 = Label(devTLP, 37).SetText('{}'.format(myDevices[0].name))
labDMP64Ip = Label(devTLP, 45).SetText('{}'.format(myDevices[0].ip))
labDMP64State = Button(devTLP, 50)
labDMP64State.SetState(myDevices[0].state)

@eventEx(myDevices[0].StateChanged, 'Triggered')
def handle_dmp64_state_changed(src, state):
    labDMP64State.SetState(state)
    ProgramLog('DMP64 state updated to: {}'.format(state), 'info')


labYamahaQL5 = Label(devTLP, 36).SetText('{}'.format(myDevices[1].name))
labYamahaQL5Ip = Label(devTLP, 39).SetText('{}'.format(myDevices[1].ip))
labYamahaQL5State = Button(devTLP, 49)
labYamahaQL5State.SetState(myDevices[1].state)

@eventEx(myDevices[1].StateChanged, 'Triggered')
def handle_yamahaql5_state_changed(src, state):
    labYamahaQL5State.SetState(state)
    ProgramLog('YamahaQL5 state updated to: {}'.format(state), 'info')

labProjector = Label(devTLP, 21).SetText('{}'.format(myDevices[2].name))
labProjectorIp = Label(devTLP, 38).SetText('{}'.format(myDevices[2].ip))
labProjectorState = Button(devTLP, 48)
labProjectorState.SetState(myDevices[2].state)

@eventEx(myDevices[2].StateChanged, 'Triggered')
def handle_projector_state_changed(src, state):
    labProjectorState.SetState(state)
    ProgramLog('Projector state updated to: {}'.format(state), 'info')

labQuickQ = Label(devTLP, 46).SetText('{}'.format(myDevices[3].name))
labQuickQIp = Label(devTLP, 47).SetText('{}'.format(myDevices[3].ip))
labQuickQState = Button(devTLP, 51)
labQuickQState.SetState(myDevices[3].state)

@eventEx(myDevices[3].StateChanged, 'Triggered')
def handle_quickq_state_changed(src, state):
    labQuickQState.SetState(state)
    ProgramLog('QuickQ state updated to: {}'.format(state), 'info')

labCamera1 = Label(devTLP, 55).SetText('{}'.format(myDevices[4].name))
labCamera1Ip = Label(devTLP, 56).SetText('{}'.format(myDevices[4].ip))
labCamera1State = Button(devTLP, 57)
labCamera1State.SetState(myDevices[4].state)

@eventEx(myDevices[4].StateChanged, 'Triggered')
def handle_camera1_state_changed(src, state):
    labCamera1State.SetState(state)
    ProgramLog('Camera1 state updated to: {}'.format(state), 'info')

labCamera2 = Label(devTLP, 58).SetText('{}'.format(myDevices[5].name))
labCamera2Ip = Label(devTLP, 59).SetText('{}'.format(myDevices[5].ip))
labCamera2State = Button(devTLP, 60)
labCamera2State.SetState(myDevices[5].state)

@eventEx(myDevices[5].StateChanged, 'Triggered')
def handle_camera2_state_changed(src, state):
    labCamera2State.SetState(state)
    ProgramLog('Camera2 state updated to: {}'.format(state), 'info')


btnCinema = Button(devTLP, 2)
btnDiscusion = Button(devTLP, 3)
btnTheatre = Button(devTLP, 4)


@eventEx(btnCinema, 'Pressed')
@eventEx(btnDiscusion, 'Pressed')
@eventEx(btnTheatre, 'Pressed')
def show_main_page(button: Button, state: str):
    if button == btnCinema:
        tlpProjector.projectorInputGroup.SetCurrent(tlpProjector.btnProjectorInputHdmi1)
        tlpYamaha.yamahaPresetGroup.SetCurrent(tlpYamaha.btnYamahaPreset1)
        tlpQuickQ.quickQ30PresetGroup.SetCurrent(tlpQuickQ.btnQuickQ30Preset1)
        tlpProjector.projectorONoffGroup.SetCurrent(tlpProjector.btnProjectorON)
        tlpProjector.btnProjectorOFF.SetState(1)
        controlProjector.projectorOn()
        tlpProjector.btnProjectorStatus.SetState(1)
    elif button == btnDiscusion:
        tlpProjector.projectorInputGroup.SetCurrent(tlpProjector.btnProjectorInputHdmi2)
        tlpYamaha.yamahaPresetGroup.SetCurrent(tlpYamaha.btnYamahaPreset2)
        tlpQuickQ.quickQ30PresetGroup.SetCurrent(tlpQuickQ.btnQuickQ30Preset2)
        tlpProjector.projectorONoffGroup.SetCurrent(None)
    elif button == btnTheatre:
        tlpProjector.projectorInputGroup.SetCurrent(tlpProjector.btnProjectorInputDisplayPort)
        tlpProjector.projectorONoffGroup.SetCurrent(None)
    devTLP.ShowPage('MainPage')



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


homeBtn = Button(devTLP, 8022,holdTime=2)
@eventEx(homeBtn, 'Held')
def homeBtn_Pressed(homeBtn:Button, state:str):
    tlpCamera.camera2Group.SetCurrent(None)
    tlpCamera.camera1Group.SetCurrent(None)
    tlpYamaha.yamahaPresetGroup.SetCurrent(None)
    tlpQuickQ.quickQ30PresetGroup.SetCurrent(None)
    #doplnit vypnutie projektora a lift 
    controlProjector.projectorOff()
    tlpProjector.btnProjectorStatus.SetState(0)
    devTLP.ShowPage('StartPage')   

btnHelp = Button(devTLP, 62)
@eventEx(btnHelp, 'Pressed')
def btnHelp_Pressed(btnHelp:Button, state:str):
    devTLP.ShowPage('HelpPage')



