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

# Project imports
from extronlib.system import Wait, ProgramLog
from modules.helper.ModuleSupport import eventEx, GenericEvent
from devices import devBarcoProjector
from devices import devLiftRelay 
from devices import devScreenRelay


# GenericEvents for projector status changes
projectorInput = GenericEvent('Projector Input Changed')
projectorPower = GenericEvent('Projector Power Changed')
projectorHours = GenericEvent('Projector Hours Changed')


def _projectorPowerCallback(command, value, qualifier):
    """Internal callback that triggers the GenericEvent"""
    ProgramLog('Projector Power status: {}'.format(value), 'info')
    projectorPower.Trigger(command, value, qualifier)


def _projectorInputCallback(command, value, qualifier):
    """Internal callback that triggers the GenericEvent"""
    ProgramLog('Projector Input status: {}'.format(value), 'info')
    projectorInput.Trigger(command, value, qualifier)


def _projectorHoursCallback(command, value, qualifier):
    """Internal callback that triggers the GenericEvent"""
    ProgramLog('Projector Laser Hours: {}'.format(value), 'info')
    projectorHours.Trigger(command, value, qualifier)


@eventEx(devBarcoProjector, ['Connected', 'Disconnected'])
def handleProjectorConnection(interface, state):
    """Subscribe to projector status on connection"""
    if state == 'Connected':
        ProgramLog('Projector connected - subscribing to status', 'info')
        devBarcoProjector.SubscribeStatus('Power', None, _projectorPowerCallback)
        devBarcoProjector.SubscribeStatus('Input', None, _projectorInputCallback)
        devBarcoProjector.SubscribeStatus('LaserHours', None, _projectorHoursCallback)

        try:
            devBarcoProjector.Update('Power')
            devBarcoProjector.Update('Input')
            devBarcoProjector.Update('LaserHours')
        except Exception as exc:
            ProgramLog('Projector status update failed: {}'.format(exc), 'error')
    else:
        ProgramLog('Projector disconnected', 'warning')


def screenUp():
    """Start moving screen up - Open relay"""
    ProgramLog('Screen moving UP - Relay OPEN', 'info')
    devScreenRelay.SetState('Open')
    devScreenRelay.Pulse(2)


def screenDown():
    """Start moving screen down - Close relay"""
    ProgramLog('Screen moving DOWN - Relay CLOSED', 'info')
    devScreenRelay.SetState('Close')
    devScreenRelay.Pulse(2)


def liftUp():
    """Start moving lift up - Open relay"""
    ProgramLog('Lift moving UP - Relay OPEN', 'info')
    devLiftRelay.SetState('Open')
    devLiftRelay.Pulse(2)


def liftDown():
    """Start moving lift down - Close relay"""
    ProgramLog('Lift moving DOWN - Relay CLOSED', 'info')
    devLiftRelay.SetState('Close')
    devLiftRelay.Pulse(2)


def projectorOn():
    """Turn on the projector"""
    ProgramLog('Turning ON the Projector', 'info')
    devBarcoProjector.Set('Power', 'On')


def projectorOff():
    """Turn off the projector"""
    ProgramLog('Turning OFF the Projector', 'info')
    devBarcoProjector.Set('Power', 'Off')


def projectorInputHdmi1():
    """Set projector input to HDMI 1"""
    ProgramLog('Setting Projector Input to HDMI 1', 'info')
    devBarcoProjector.Set('Input', 'L1 HDMI')


def projectorInputHdmi2():
    """Set projector input to HDMI 2"""
    ProgramLog('Setting Projector Input to HDMI 2', 'info')
    devBarcoProjector.Set('Input', 'L2 HDMI')


def projectorInputDisplayPort():
    """Set projector input to DisplayPort"""
    ProgramLog('Setting Projector Input to DisplayPort', 'info')
    devBarcoProjector.Set('Input', 'L1 DisplayPort')
