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

btnProjectorStatus = Button(devTLP, 40)
labProjectorHours = Label(devTLP, 14)
btnProjectorON = Button(devTLP, 8000)
btnProjectorOFF = Button(devTLP, 13)
btnProjectorInputHdmi1 = Button(devTLP, 15)
btnProjectorInputHdmi2 = Button(devTLP, 18)
btnProjectorInputDisplayPort = Button(devTLP, 19)

projectorInputGroup = MESet([btnProjectorInputHdmi1, btnProjectorInputHdmi2, btnProjectorInputDisplayPort])
projectorInputGroup.SetCurrent(btnProjectorInputHdmi1)
@eventEx(projectorInputGroup.Objects,'Pressed')
def projectorInputGroup_Pressed(button:Button, state:str):
    projectorInputGroup.SetCurrent(button)
    if button == btnProjectorInputHdmi1:
        controlProjector.projector_inputHDMI()
    elif button == btnProjectorInputHdmi2:
        controlProjector.projector_inputDP()
    elif button == btnProjectorInputDisplayPort:
        controlProjector.projector_inputDP()

projectorONoffGroup = MESet([btnProjectorON, btnProjectorOFF])
@eventEx(projectorONoffGroup.Objects,'Pressed')
def projectorONoffGroup_Pressed(button:Button, state:str):
    projectorONoffGroup.SetCurrent(button)
    if button == btnProjectorON:
        controlProjector.projector_on()
        btnProjectorON.SetState(1)
        btnProjectorOFF.SetState(0)
        btnProjectorStatus.SetState(1)
    elif button == btnProjectorOFF:
        controlProjector.projector_off()
        btnProjectorOFF.SetState(1)
        btnProjectorON.SetState(0)
        btnProjectorStatus.SetState(0)


@eventEx(projectorInputGroup.Objects,'Pressed')
def projectorInputGroup_Pressed(button:Button, state:str):
    projectorInputGroup.SetCurrent(button)

btnLifUp = Button(devTLP, 10)
btnLiftDown = Button(devTLP, 9)

@eventEx([btnLifUp, btnLiftDown],['Pressed','Released'])
def lift_buttons_Event(button:Button, state:str):
    if button == btnLifUp:
        if state == 'Pressed':
            controlProjector.LiftUp()
            print("Lift Up Pressed",button.Name,state)
            button.SetState(1)
        elif state == 'Released':
            print("Lift Up Released",button.Name,state)
            button.SetState(0)
    elif button == btnLiftDown:
        if state == 'Pressed':
            controlProjector.LiftDown()
            print("Lift Down Pressed",button.Name,state)
            button.SetState(1)  
        elif state == 'Released':
            print("Lift Down Released",button.Name,state)
            button.SetState(0)

btnScreenDown = Button(devTLP, 23)
btnScreenUp = Button(devTLP, 24)

@eventEx([btnScreenDown, btnScreenUp],['Pressed','Released'])
def screen_buttons_Event(button:Button, state:str):
    if button == btnScreenUp:
        if state == 'Pressed':
            controlProjector.ScreenUp()
            print("Screen Up Pressed",button.Name,state)
            button.SetState(1)
        elif state == 'Released':
            print("Screen Up Released",button.Name,state)
            button.SetState(0)
    elif button == btnScreenDown:
        if state == 'Pressed':
            controlProjector.ScreenDown()
            print("Screen Down Pressed",button.Name,state)
            button.SetState(1)  
        elif state == 'Released':
            print("Screen Down Released",button.Name,state)
            button.SetState(0)



@eventEx(btnCinema, 'Pressed')
@eventEx(btnDiscusion, 'Pressed')
@eventEx(btnTheatre, 'Pressed')
def show_main_page(button: Button, state: str):
    if button == btnCinema:
        projectorInputGroup.SetCurrent(btnProjectorInputHdmi1)
        yamahaPresetGroup.SetCurrent(btnYamahaPreset1)
        quickQ30PresetGroup.SetCurrent(btnQuickQ30Preset1)
        projectorONoffGroup.SetCurrent(btnProjectorON)
        controlProjector.projector_on()
        btnProjectorStatus.SetState(1)
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
        controlYamaha.call_yamaha_preset('1')
    elif button == btnYamahaPreset2:
        controlYamaha.call_yamaha_preset('2')
    elif button == btnYamahaPreset3:
        controlYamaha.call_yamaha_preset('3')



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

