"""
The main program entrance file.  The contents of this should be:
* Identification of the platform and version.
* imports of the project components
* Call to initialize the system
"""

# Python imports

# Extron Library Imports
from extronlib import Platform, Version

print('ControlScript', Platform(), Version())

# Project imports
import variables
import devices
import ui.tlp
import control.av
import system
from devices import devTLP

devTLP.ShowPage('Intro')
devTLP.ShowPopup('PopupConnections')

system.Initialize()
