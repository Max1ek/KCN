# KCN Device Module Notes

These notes summarize the Global Scripter module communication sheets in `docs/`.

## ConnectionHandler_v2x3x0b.pdf
- Purpose: connection-management helper that wraps serial/Ethernet interfaces and adds auto-reconnect plus keep-alive polling.
- Core handlers: ConnectionHandler, RawSimplePipeHandler, ModuleSimplePipeHandler, RawTcpHandler, ModuleTcpHandler, ServerExHandler.
- Key API: `GetConnectionHandler(Interface, keepAliveQuery=None, keepAliveQueryQualifier=None, DisconnectLimit=15, pollFrequency=1, connectRetryTime=5, serverTimeout=300)`.
- Notes: returned instance mirrors the original interface API and adds status/reconnect behavior; examples show using keep-alive queries to maintain sessions.

## barc_vp_UDM_4K_W_Series_v1_0_2_0.pdf
- Module: `barc_vp_UDM_4K_W_Series_v1_0_2_0.py`
- Device: Video projector (Barco UDM-4K22, UDM-W22). Revision 2/5/2025.
- Connections: SerialClass, SerialOverEthernetClass, EthernetClass.
- Module notes: `Unidirectional=True` if you do not need status; `connectionCounter` controls how many missed replies before `Disconnected`.
- Commands (sample): DesiredDisplayMode, Focus, Illumination, Input, Power, ConnectionStatus, LaserHours, OperationHours.

## cham_lc_QuickQ_Series_v1_0_0_0.pdf
- Module: `cham_lc_QuickQ_Series_v1_0_0_0.py`
- Device: Lighting control (Chamsys QuickQ 20/10/30 Console, QuickQ Rack). Revision 6/19/2023.
- Connections: EthernetClass (UDP; device listen port 6553).
- Commands: ActivatePlayback, ActivatePlaybackat100, ReleasePlayback, ReleasePlaybackat100, Toggle10SceneButton.

## extr_dsp_DMP_64_Plus_Series_v1_4_2_0.pdf
- Module: `extr_dsp_DMP_64_Plus_Series_v1_4_2_0.py`
- Device: Audio processor (Extron DMP 64 Plus series). Revision 10/8/2024. Firmware noted: 1.11.0000-b006.
- Connections: SerialClass, SerialOverEthernetClass, SSHClass.
- Module notes: `Unidirectional` and `connectionCounter` as above; set `deviceUsername`/`devicePassword` if login required; group commands depend on DSP Configurator setup.
- Commands (sample): AutoAnswerDelay/Mode, AutomixerGateSet, AuxInputGain/Mute, AuxOutputGain/Mute, DanteInputGain/Mute, DanteOutputAttenuation/Mute, Dial, DialDTMF, DoNotDisturb, ExpansionBusMixpointGain/Mute.

## extr_matrix_DTP_CrossPoint_82_84_4kSeriesv1872.pdf
- Module: `extr_matrix_DTP_CrossPoint_82_84_4k_Series_v1_8_7_2.py`
- Device: Matrix switcher (Extron DTP CrossPoint 82/84 4K series). Revision 5/15/2024. Firmware noted: 2.01.0009-b001.
- Connections: SerialClass, SerialOverEthernetClass, SSHClass.
- Module notes: `Unidirectional` and `connectionCounter` as above; set `devicePassword` if login required.
- Commands (sample): AmplifierAttenuationMA/SA, AmplifierMuteMA/SA, AspectRatio, AutoImage, ExecutiveMode, Freeze, GlobalVideoMute, HDCPInputAuthorization, HDCPOutputAuthorization, InputGain, InputMute, Logo, LogoAssignment.

## vadd_camera_RoboSHOT_v1_1_2_1.pdf
- Module: `vadd_camera_RoboSHOT_v1_1_2_1.py`
- Device: Camera (Vaddio RoboSHOT 12/20/30/40). Revision 12/1/2022.
- Connections: SerialClass, SerialOverEthernetClass, EthernetClass.
- Module notes: `Unidirectional` and `connectionCounter`; set `deviceUsername`/`devicePassword` if needed; set `DeviceID` (1-7) for serial control.
- Commands (sample): AutoFocus, Backlight, Focus, Freeze, Iris, Mute, PanTiltZoom, Power, PresetRecall, PresetSave, WhiteBalance, ConnectionStatus.

## yama_dsp_QL1_QL5_v1_1_1_0.pdf
- Module: `yama_dsp_QL1_QL5_v1_1_1_0.py`
- Device: Audio processor (Yamaha QL5, QL1). Revision 8/13/2019. Firmware noted: V5.10.
- Connections: EthernetClass.
- Module notes: `Unidirectional` and `connectionCounter`; use Update for proper level step sizing (device has multiple step ranges).
- Commands: DCAGroupLevel/Mute, InputLevel/Mute, MatrixLevel/Mute, MixLevel/Mute, PresetRecall/Save, StereoLevel/Mute, ConnectionStatus, DeviceStatus.

## ControlScriptFramework_v1x0x0-revL.pdf
- Purpose: overview of Extron ControlScript Programming Framework and recommended project structure.
- Key parts: Code Folder Structure, Module Support, Device Modules, Helper Modules.
- ModuleSupport.py: shared utilities for device/helper/project modules; includes eventEx and logging helpers.
- Version history: 1.0.0 (3/7/2023) initial release.
- Contents highlights: module communication sheets, using device modules in projects, module support API, and appendices.

## README.pdf
- Project overview: ControlScript project using Python 3 (noted 3.11.8 on Pro xi controllers) with focus on large multi-room deployment.
- Key considerations: f-strings supported but .format() recommended for parsing safety; type hints supported; memory management is important.
- Deployment goals: single codebase for ~150 rooms, standardized UI with fixed IDs, modular drivers loaded per room, JSON per-room configuration.
- Structure highlights: devices.py, variables.py, system.py, ui/, control/, drivers/, modules/ (ModuleSupport.py), helpers/, layout/, sound/, rfile/, ir/, configs/, docs/.
