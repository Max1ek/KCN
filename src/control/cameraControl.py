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
from control.yamahaControl import _yamahaRecallPresetCallback
from extronlib.system import ProgramLog
from modules.helper.ModuleSupport import GenericEvent, eventEx
from devices import devCamera1, devCamera2

camera1RecallPreset = GenericEvent('Camera1 Recall Preset')
camera2RecallPreset = GenericEvent('Camera2 Recall Preset')

def _camera1RecallPresetCallback(command, value, qualifier):
    """Internal callback that triggers the GenericEvent"""
    ProgramLog('Camera1 Recall Preset status: {}'.format(value), 'info')
    camera1RecallPreset.Trigger(command, value, qualifier)

def _camera2RecallPresetCallback(command, value, qualifier):
    """Internal callback that triggers the GenericEvent"""
    ProgramLog('Camera2 Recall Preset status: {}'.format(value), 'info')
    camera2RecallPreset.Trigger(command, value, qualifier)

@eventEx(devCamera1, ['Connected', 'Disconnected'])
def handleCamera1Connection(interface, state):
    """Subscribe to Camera1 status on connection"""
    if state == 'Connected':
        ProgramLog('Camera1 connected - subscribing to status', 'info')
        devCamera1.SubscribeStatus('PresetRecall', None, _camera1RecallPresetCallback)
     
        try:
            devCamera1.Update('PresetRecall')
          
        except Exception as exc:
            ProgramLog('Camera1 status update failed: {}'.format(exc), 'error')
    else:
        ProgramLog('Camera1 disconnected', 'warning')


@eventEx(devCamera2, ['Connected', 'Disconnected'])
def handleCamera2Connection(interface, state):
    """Subscribe to Camera2 status on connection"""
    if state == 'Connected':
        ProgramLog('Camera2 connected - subscribing to status', 'info')
        devCamera2.SubscribeStatus('PresetRecall', None, _camera2RecallPresetCallback)
     
        try:
            devCamera2.Update('PresetRecall')
          
        except Exception as exc:
            ProgramLog('Camera2 status update failed: {}'.format(exc), 'error')
    else:
        ProgramLog('Camera2 disconnected', 'warning')


def callCamera1Preset(preset_number: str):
    """Set the Camera1 to a specific preset number."""
    ProgramLog('Setting Camera1 to preset {}'.format(preset_number), 'info')
    devCamera1.Set('PresetRecall', preset_number)

def callCamera2Preset(preset_number: str):
    """Set the Camera2 to a specific preset number."""
    ProgramLog('Setting Camera2 to preset {}'.format(preset_number), 'info')
    devCamera2.Set('PresetRecall', preset_number)