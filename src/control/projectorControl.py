"""
This is the place to put control code for various types of systems (e.g. AV, Building Management).
The core purpose is for separation of concerns. Each concern should be as isolated as possible,
taking advantage of the framework structure and helper modules.

Examples:

* AV devices
* Building management systems
  * Lighting
  * HVAC
* Cloud Services
"""

# Python imports

# Extron Library imports
import ui.tlp as tlp
# Project imports
from extronlib.system import Wait, ProgramLog
from modules.helper.ModuleSupport import eventEx, GenericEvent
from devices import devBarcoProjector
from devices import devLiftRelay 
from devices import devScreenRelay


projectorInput = GenericEvent('Projector Input Changed')
projectorPower = GenericEvent('Projector Power Changed')
projectorHours = GenericEvent('Projector Hours Changed')


@eventEx(devBarcoProjector, ['Connected', 'Disconnected'])
def initProjectorSubscriptions():
    devBarcoProjector.SubscribeStatus('Power', None, projectorPower.Trigger)
    devBarcoProjector.SubscribeStatus('Input', None, projectorInput.Trigger)
    devBarcoProjector.SubscribeStatus('LaserHours', None, projectorHours.Trigger)

    try:
        devBarcoProjector.Update('Power')
        devBarcoProjector.Update('Input')
        devBarcoProjector.Update('LaserHours')
    except Exception as exc:
        ProgramLog('Projector status update failed: {}'.format(exc), 'error')


def ScreenUp():
    """Start moving screen up - Open relay"""
    ProgramLog('Screen moving UP - Relay OPEN', 'info')
    devScreenRelay.SetState('Open')  # Open relay for screen up
    devScreenRelay.Pulse(2)

def ScreenDown():
    """Start moving screen down - Close relay"""
    ProgramLog('Screen moving DOWN - Relay CLOSED', 'info')
    devScreenRelay.SetState('Close')  # Close relay for screen down
    devScreenRelay.Pulse(2)

def LiftUp():
    """Start moving lift up - Open relay"""
    ProgramLog('Lift moving UP - Relay OPEN', 'info')
    devLiftRelay.SetState('Open')  # Open relay for lift up
    devLiftRelay.Pulse(2)

def LiftDown():
    """Start moving lift down - Close relay"""
    ProgramLog('Lift moving DOWN - Relay CLOSED', 'info')
    devLiftRelay.SetState('Close')  # Close relay for lift down
    devLiftRelay.Pulse(2)

def projector_on():
    """Turn on the projector"""
    ProgramLog('Turning ON the Projector', 'info')
    devBarcoProjector.Set('Power', 'On')

def projector_off():
    """Turn off the projector"""
    ProgramLog('Turning OFF the Projector', 'info')
    devBarcoProjector.Set('Power', 'Off')

def projector_inputHDMI():
    """Set projector input to HDMI"""
    ProgramLog('Setting Projector Input to HDMI', 'info')
    devBarcoProjector.Set('Input', 'L1 HDMI') # 

def projector_inputDP():
    """Set projector input to DisplayPort"""
    ProgramLog('Setting Projector Input to DisplayPort', 'info')
    devBarcoProjector.Set('Input', 'L1 DisplayPort')

@eventEx(projectorHours, 'Triggered')
def _projector_hours_status(source:GenericEvent,command:str, value:str,qualifier:str):
    ProgramLog('Projector Hours Status Changed: {}'.format(value), 'info')
    tlp.lblProjectorHours.SetText(value)
    
@eventEx(projectorPower, 'Triggered')
def _projector_power_status(source:GenericEvent,command:str, value:str,qualifier:str):
    ProgramLog('Projector Power Status Changed: {}'.format(value), 'info')
    if value == 'On':
        tlp.btnProjectorON.SetState(1)
        tlp.btnProjectorOFF.SetState(0)
        tlp.btnProjectorStatus.SetState(1)
    elif value == 'Off':
        tlp.btnProjectorON.SetState(0)
        tlp.btnProjectorOFF.SetState(1)
        tlp.btnProjectorStatus.SetState(0)

@eventEx(projectorInput, 'Triggered')
def _projector_input_status(source:GenericEvent,command:str, value:str,qualifier:str):
    ProgramLog('Projector Input Status Changed: {}'.format(value), 'info')
    if value == 'L1 HDMI':
        tlp.projectorInputGroup.SetCurrent(tlp.btnProjectorInputHdmi1)
    elif value == 'L1 DisplayPort':
        tlp.projectorInputGroup.SetCurrent(tlp.btnProjectorInputDisplayPort)
