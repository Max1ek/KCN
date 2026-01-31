from extronlib.ui import Button, Label
from extronlib.system import MESet, ProgramLog
from modules.helper.ModuleSupport import eventEx
from devices import devTLP

import control.quickQControl as controlQuickQ

btnQuickQ30Preset1 = Button(devTLP, 35)
btnQuickQ30Preset2 = Button(devTLP, 33)
btnQuickQ30Preset3 = Button(devTLP, 34)

quickQ30PresetGroup = MESet([btnQuickQ30Preset1, btnQuickQ30Preset2, btnQuickQ30Preset3])

@eventEx(quickQ30PresetGroup.Objects,'Pressed')
def quickQ30PresetGroup_Pressed(button:Button, state:str):
        quickQ30PresetGroup.SetCurrent(button)
        if button == btnQuickQ30Preset1:
            controlQuickQ.callQuickQPreset('1')
        elif button == btnQuickQ30Preset2:
            controlQuickQ.callQuickQPreset('2')
        elif button == btnQuickQ30Preset3:
            controlQuickQ.callQuickQPreset('3')