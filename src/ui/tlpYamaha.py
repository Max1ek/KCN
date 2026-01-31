from extronlib.ui import Button, Label
from extronlib.system import MESet, ProgramLog
from modules.helper.ModuleSupport import eventEx
from devices import devTLP

import control.yamahaControl as controlYamaha

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

# Subscribe to Yamaha DSP status events
@eventEx(controlYamaha.yamahaRecallPreset, 'Triggered')
def handleYamahaRecallPresetChange(source, command, value, qualifier):
    """Update UI when Yamaha DSP recall preset status changes"""
    ProgramLog('Yamaha Recall Preset Status Changed: {}'.format(value), 'info')
    if value == '1':
       yamahaPresetGroup.SetCurrent(btnYamahaPreset1)
    elif value == '2':
        yamahaPresetGroup.SetCurrent(btnYamahaPreset2)
    elif value == '3':
        yamahaPresetGroup.SetCurrent(btnYamahaPreset3)