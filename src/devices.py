"""
This is the place to define each of the devices in the system.
* Extron control devices (e.g. all extronlib.device objects)
* Non-control devices and services (e.g. device modules)
* User defined devices (e.g. all extronlib.interface objects or custom python coded devices)

Note: This is for definition only.  Connection and logic defined in system.py (see below).
"""

# Python imports
from extronlib.device import ProcessorDevice, UIDevice
from extronlib.interface import RelayInterface
from extronlib.system import Wait, ProgramLog

# Extron Library imports

# Project imports
from modules.helper.ConnectionHandler import GetConnectionHandler

import modules.device.barc_vp_UDM_4K_W_Series_v1_0_2_0 as modBarcoProjector
import modules.device.yama_dsp_QL1_QL5_v1_1_1_0 as modYamahaDSP
import modules.device.cham_lc_QuickQ_Series_v1_0_0_0 as modChamQuickQ
import modules.device.vadd_camera_RoboSHOT_v1_1_2_1 as modVaddCamera
import modules.device.extr_matrix_DTP_CrossPoint_82_84_4kSeriesv1872 as modExtronMatrix
import modules.device.extr_dsp_DMP_64_Plus_Series_v1_4_2_0 as modExtronDMP

from variables import (
    IP_BARCO_PROJECTOR, IP_YAMAHA_DSP, IP_QUICKQ, 
    IP_CAMERA1, IP_CAMERA2, IP_DTP_MATRIX, IP_DMP64,
    PORT_BARCO_PROJECTOR, PORT_YAMAHA_DSP, PORT_QUICKQ, 
    PORT_CAMERA, PORT_SSH
)


# Define devices
devIPCP = ProcessorDevice('ProcessorAlias')
devTLP = UIDevice('PanelAlias')

devBarcoProjector = modBarcoProjector.EthernetClass(IP_BARCO_PROJECTOR, PORT_BARCO_PROJECTOR, Model='UDM-4K22')
devBarcoProjector = GetConnectionHandler(devBarcoProjector,'ConnectionStatus')

devYamahaDSP = modYamahaDSP.EthernetClass(IP_YAMAHA_DSP, PORT_YAMAHA_DSP, Model='QL5')
devYamahaDSP = GetConnectionHandler(devYamahaDSP,'ConnectionStatus')

devQuickQ = modChamQuickQ.EthernetClass(IP_QUICKQ, PORT_QUICKQ, Model='QuickQ 30') 
devQuickQ = GetConnectionHandler(devQuickQ,'')

devCamera1 = modVaddCamera.EthernetClass(IP_CAMERA1, PORT_CAMERA, Model='RoboSHOT 12 HDMI')
devCamera1 = GetConnectionHandler(devCamera1,'ConnectionStatus')

devCamera2 = modVaddCamera.EthernetClass(IP_CAMERA2, PORT_CAMERA, Model='RoboSHOT 12 HDMI')
devCamera2 = GetConnectionHandler(devCamera2,'ConnectionStatus')

devDTP = modExtronMatrix.SSHClass(IP_DTP_MATRIX, PORT_SSH, Credentials=('admin', ''), Model='DTP CrossPoint 82 4K') 
devDTP = GetConnectionHandler(devDTP,'ConnectionStatus')

devScreenRelay = RelayInterface(devIPCP, 'RLY1')
devLiftRelay = RelayInterface(devIPCP, 'RLY2')

devDMP64 = modExtronDMP.SSHClass(IP_DMP64, PORT_SSH,Credentials=('admin', 'A2WYKA9'),Model='DMP 64 Plus C AT')
devDMP64 = GetConnectionHandler(devDMP64, 'PartNumber')

