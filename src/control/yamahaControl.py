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
from modules.helper.ModuleSupport import eventEx
from devices import devYamahaDSP


def call_yamaha_preset(preset_number: str):
    """Set the Yamaha DSP to a specific preset number."""
    ProgramLog(f'Setting Yamaha DSP to preset {preset_number}', 'info')
    devYamahaDSP.Set('PresetRecall', preset_number)