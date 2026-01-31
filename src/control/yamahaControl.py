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
from modules.helper.ModuleSupport import GenericEvent, eventEx
from devices import devYamahaDSP

yamahaRecallPreset = GenericEvent('Yamaha Recall Preset')

def _yamahaRecallPresetCallback(command, value, qualifier):
    """Internal callback that triggers the GenericEvent"""
    ProgramLog('Yamaha Recall Preset status: {}'.format(value), 'info')
    yamahaRecallPreset.Trigger(command, value, qualifier)

@eventEx(devYamahaDSP, ['Connected', 'Disconnected'])
def handleYamahaConnection(interface, state):
    """Subscribe to Yamaha DSP status on connection"""
    if state == 'Connected':
        ProgramLog('Yamaha DSP connected - subscribing to status', 'info')
        devYamahaDSP.SubscribeStatus('PresetRecall', None, _yamahaRecallPresetCallback)
     
        try:
            devYamahaDSP.Update('PresetRecall')
          
        except Exception as exc:
            ProgramLog('Yamaha DSP status update failed: {}'.format(exc), 'error')
    else:
        ProgramLog('Yamaha DSP disconnected', 'warning')

def call_yamaha_preset(preset_number: str):
    """Set the Yamaha DSP to a specific preset number."""
    ProgramLog('Setting Yamaha DSP to preset {}'.format(preset_number), 'info')
    devYamahaDSP.Set('PresetRecall', preset_number)