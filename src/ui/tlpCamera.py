from extronlib.ui import Button, Label
from extronlib.system import MESet, ProgramLog
from modules.helper.ModuleSupport import eventEx
from devices import devTLP

import control.cameraControl as controlCamera

btnCamera1Preset1 = Button(devTLP, 27)
btnCamera1Preset2 = Button(devTLP, 25)
btnCamera1Preset3 = Button(devTLP, 26)

camera1Group = MESet([btnCamera1Preset1, btnCamera1Preset2, btnCamera1Preset3])
@eventEx(camera1Group.Objects,'Pressed')
def camera1Group_Pressed(button:Button, state:str):
    camera1Group.SetCurrent(button)
    if button == btnCamera1Preset1:
        controlCamera.callCamera1Preset('1')
    elif button == btnCamera1Preset2:
        controlCamera.callCamera1Preset('2')
    elif button == btnCamera1Preset3:
        controlCamera.callCamera1Preset('3')

        
btnCamera2Preset1 = Button(devTLP, 44)
btnCamera2Preset2 = Button(devTLP, 42)  
btnCamera2Preset3 = Button(devTLP, 43)

camera2Group = MESet([btnCamera2Preset1, btnCamera2Preset2, btnCamera2Preset3])
@eventEx(camera2Group.Objects,'Pressed')    
def camera2Group_Pressed(button:Button, state:str):
    camera2Group.SetCurrent(button)
    if button == btnCamera2Preset1:
        controlCamera.callCamera2Preset('1')
    elif button == btnCamera2Preset2:
        controlCamera.callCamera2Preset('2')
    elif button == btnCamera2Preset3:
        controlCamera.callCamera2Preset('3')

# Subscribe to Camera1 preset status events
@eventEx(controlCamera.callCamera1Preset, 'Triggered')
def handleCamera1RecallPresetChange(source, command, value, qualifier):
    """Update UI when Camera1 recall preset status changes"""
    ProgramLog('Camera1 Recall Preset Status Changed: {}'.format(value), 'info')
    if value == '1':
       camera1Group.SetCurrent(btnCamera1Preset1)
    elif value == '2':
        camera1Group.SetCurrent(btnCamera1Preset2)
    elif value == '3':
        camera1Group.SetCurrent(btnCamera1Preset3)

@eventEx(controlCamera.callCamera2Preset, 'Triggered')
def handleCamera2RecallPresetChange(source, command, value, qualifier):
    """Update UI when Camera2 recall preset status changes"""
    ProgramLog('Camera2 Recall Preset Status Changed: {}'.format(value), 'info')
    if value == '1':
       camera2Group.SetCurrent(btnCamera2Preset1)
    elif value == '2':
        camera2Group.SetCurrent(btnCamera2Preset2)
    elif value == '3':
        camera2Group.SetCurrent(btnCamera2Preset3)