from extronlib.ui import Button, Label
from extronlib.system import MESet, ProgramLog
from modules.helper.ModuleSupport import eventEx
from devices import devTLP

import control.projectorControl as controlProjector



btnProjectorStatus = Button(devTLP, 40)
labProjectorHours = Label(devTLP, 14)
btnProjectorON = Button(devTLP, 8000)
btnProjectorOFF = Button(devTLP, 13, holdTime=2)
btnProjectorInputHdmi1 = Button(devTLP, 15)
btnProjectorInputHdmi2 = Button(devTLP, 18)
btnProjectorInputDisplayPort = Button(devTLP, 19)

projectorInputGroup = MESet([btnProjectorInputHdmi1, btnProjectorInputHdmi2, btnProjectorInputDisplayPort])
projectorInputGroup.SetCurrent(btnProjectorInputHdmi1)
@eventEx(projectorInputGroup.Objects,'Pressed')
def projectorInputGroup_Pressed(button:Button, state:str):
    projectorInputGroup.SetCurrent(button)
    if button == btnProjectorInputHdmi1:
        controlProjector.projectorInputHdmi1()
    elif button == btnProjectorInputHdmi2:
        controlProjector.projectorInputHdmi2()
    elif button == btnProjectorInputDisplayPort:
        controlProjector.projectorInputDisplayPort()

projectorONoffGroup = MESet([btnProjectorON, btnProjectorOFF])
@eventEx(projectorONoffGroup.Objects,['Pressed','Held'])
def projectorONoffGroup_Pressed(button:Button, state:str):
    if button == btnProjectorON and state == 'Pressed':
        projectorONoffGroup.SetCurrent(button)
        controlProjector.projectorOn()
    elif button == btnProjectorOFF and state == 'Held':
        projectorONoffGroup.SetCurrent(button)
        controlProjector.projectorOff()


@eventEx(projectorInputGroup.Objects,'Pressed')
def projectorInputGroup_Pressed(button:Button, state:str):
    projectorInputGroup.SetCurrent(button)

btnLifUp = Button(devTLP, 10)
btnLiftDown = Button(devTLP, 9)

@eventEx([btnLifUp, btnLiftDown],['Pressed','Released'])
def lift_buttons_Event(button:Button, state:str):
    if button == btnLifUp:
        if state == 'Pressed':
            controlProjector.liftUp()
            print("Lift Up Pressed",button.Name,state)
            button.SetState(1)
        elif state == 'Released':
            print("Lift Up Released",button.Name,state)
            button.SetState(0)
    elif button == btnLiftDown:
        if state == 'Pressed':
            controlProjector.liftDown()
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
            controlProjector.screenUp()
            print("Screen Up Pressed",button.Name,state)
            button.SetState(1)
        elif state == 'Released':
            print("Screen Up Released",button.Name,state)
            button.SetState(0)
    elif button == btnScreenDown:
        if state == 'Pressed':
            controlProjector.screenDown()
            print("Screen Down Pressed",button.Name,state)
            button.SetState(1)  
        elif state == 'Released':
            print("Screen Down Released",button.Name,state)
            button.SetState(0)

# Subscribe to projector status events
@eventEx(controlProjector.projectorPower, 'Triggered')
def handleProjectorPowerChange(source, command, value, qualifier):
    """Update UI when projector power status changes"""
    ProgramLog('Projector Power Status Changed: {}'.format(value), 'info')
    if value == 'On':
        btnProjectorON.SetState(1)
        btnProjectorOFF.SetState(0)
        btnProjectorStatus.SetState(1)
    elif value == 'Off':
        btnProjectorON.SetState(0)
        btnProjectorOFF.SetState(1)
        btnProjectorStatus.SetState(0)
    elif value in ['Warming', 'Cooling']:
        btnProjectorStatus.SetState(2)


@eventEx(controlProjector.projectorInput, 'Triggered')
def handleProjectorInputChange(source, command, value, qualifier):
    """Update UI when projector input changes"""
    ProgramLog('Projector Input Status Changed: {}'.format(value), 'info')
    if value == 'L1 HDMI':
        projectorInputGroup.SetCurrent(btnProjectorInputHdmi1)
    elif value == 'L2 HDMI':
        projectorInputGroup.SetCurrent(btnProjectorInputHdmi2)
    elif value == 'L1 DisplayPort':
        projectorInputGroup.SetCurrent(btnProjectorInputDisplayPort)


@eventEx(controlProjector.projectorHours, 'Triggered')
def handleProjectorHoursChange(source, command, value, qualifier):
    """Update UI when projector hours change"""
    ProgramLog('Projector Hours: {}'.format(value), 'info')
    labProjectorHours.SetText(str(value))
