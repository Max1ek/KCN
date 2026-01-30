# Extron ControlScript — Codex Agent Playbook (from provided PDFs)

This markdown is meant to be dropped into a **Codex Agent** (or any code-assistant) as “project context” so it generates Extron ControlScript code that matches Extron’s recommended structure and common helper modules.

---

## 1) Runtime & constraints (what the controller is really running)

- ControlScript on **IPCP Pro xi** runs **Python 3** (example project notes Python **3.11.8** on Pro xi controllers).  
- Embedded controller constraints matter: keep memory usage modest; avoid huge imports and long-lived buffers.
- Practical gotcha from the example project: f-strings are supported but can cause parsing issues in some pipelines—prefer `"{}".format()` in “safest” code paths.

(From README project overview PDF)

### Pro xi API conventions that trip people up (from ControlScript Pro xi 1.9r7 docs)

- **Properties are read-only** unless explicitly stated otherwise; treat them like state you *observe*.
- Wherever a **float** is specified, an **int is also accepted**.
- All time durations are **seconds** and represented as **floats**.
- A property that doesn’t apply to the current mode/product returns **None** when read; attempting to set it generates a **log entry**.
- For physical devices, some properties may be **None until known** (e.g., before a device becomes *Online*).
- For interface send methods that accept `str` or `bytes`:
  - If a **string** is passed, it is encoded using the default `.encode()` before sending.
  - If a **bytes** object is passed, it is sent as-is.
- **Interfaces can only be instantiated once** (don’t create multiple `SerialInterface(...)` objects for the same port).
- On Pro xi processors/panels, some **connection events can fire immediately upon handler assignment** based on current connection state.

(From ControlScript Pro xi 1.9r7 docs in index_merged.pdf)

---

## 2) Recommended project structure (Framework “code folder structure”)

Extron’s ControlScript Framework recommends a consistent partitioning for supportability:

```
<code_folder_path>/   (often "src")
|_ modules/
|  |_ device/         # Device modules (drivers)
|  |_ helper/         # Helper modules, incl. ModuleSupport.py
|  |_ project/        # Project-wide reusable classes/tools (not device/helper)
|_ ui/                # One module per UI device (touchpanels etc.)
|_ control/            # “Concerns” (AV, lighting, HVAC, etc.)
|_ main.py
|_ variables.py
|_ devices.py
|_ system.py
|_ user_defined_*.py   # optional extra files (imported by system.py)
```

Key intent:
- **modules/device**: device modules/drivers.
- **modules/helper**: Extron helper modules (ModuleSupport.py, ConnectionHandler, etc.).
- **modules/project**: project-wide utilities/classes (not device/helper).
- **ui**: UI objects + event handlers + navigation + feedback.
- **control**: “separation of concerns” (AV vs lighting vs HVAC …).

(From ControlScript Framework PDF)

---

## 3) Core file responsibilities (how to wire the whole system)

### `main.py` (entry point)
Framework expectation:
1) Identify platform/version  
2) Import project components  
3) Call system initialization

Example:
- `print('ControlScript', Platform(), Version())`
- import `variables`, `devices`, `ui.*`, `control.*`, `system`
- `system.Initialize()`

### `variables.py`
Shared global data/state (static constants, dynamic state, shared objects).  
Import `variables` anywhere to read/update.

### `devices.py`
**Definitions only**: instantiate extronlib devices/interfaces, instantiate device modules, name things.  
**No connection logic** here (do that in `system.py`).

### `system.py`
The orchestrator:
- Provide `Initialize()` called by `main.py`
- Connection startup (Connect calls)
- Timers/clocks/scheduled events
- Service setup (servers, CLIs)
- System-level automation and state machine hooks

### Extra files
If `system.py` gets large, create `user_defined_*.py` or folders under src, but:
- import them into `system.py`
- avoid cross-import tangles; route shared data through `system.py`

(From ControlScript Framework PDF)

---

## 4) Event handling: prefer `eventEx` for scalable projects

Extron’s `ModuleSupport.py` provides **`eventEx`**, which is compatible with `extronlib.event` but extends it:

- Multiple handlers can be attached to the same event (order = assignment order)
- Stacking decorators is supported
- You can pass lists of objects and lists of event names
- EventName can refer to *method names* too (not only properties)

Use `eventEx` as a drop-in replacement when you want more flexibility.

(From ControlScript Framework PDF)

---

## 5) Manual Events (when you want your own event sources)

The Framework describes “Manual Events” for events you trigger from your own code:

### `GenericEvent`
Use this when you want to `Trigger(...)` an event and handle it with `@event` / `@eventEx`.

Typical use: bridging a callback API to a standard event handler.

### `WatchVariable`
Wrap a variable so changes can trigger handlers (async notifications).
Pattern:
- Store the real value in `variables.py`
- Store a `WatchVariable` alongside it
- Call `Change(new_value)` from wherever the state changes
- Handle with `@eventEx(CallStatusWatch, 'Changed')`

(From ControlScript Framework PDF)

---

## 6) Logging strategy (centralize and make optional)

Framework guidance:
- Instantiate **one** logger (or few) and pass/import it to modules that need it.
- Logger options include Trace, Program Log, and TCP logging (e.g., DataViewer).
- New loggers are swappable if they implement `Log(self, *recordobjs, sep=' ', severity='info')`.

Recommended pattern in classes:
- Accept optional `logger=None` in constructor
- Wrap logging calls via a `_Log(...)` helper that no-ops when logger is None

(From ControlScript Framework PDF)

Also note: `ProgramLog(message, Severity='Info'|'Warning'|'Error')` exists in `extronlib.system` and can show Trace output if Trace is active.

(From “Extron Control System Programming Using Python” PDF)

---

## 7) Connection management: use ConnectionHandler module (auto reconnect + keepalive)

The **Connection Handler** helper module wraps interfaces or some device modules to:
- Provide consistent **Connected/Disconnected** style events
- Run **periodic keep-alive polling**
- Optionally **auto reconnect**
- Provide `SendAndWait(...)` for blocking request/response (where supported)

**Do not instantiate the handler classes directly.** Use:

> `GetConnectionHandler(Interface, keepAliveQuery, ...)`

The helper chooses the right wrapper based on interface type and protocol.

### 7.1) Interface → handler type mapping (from the docs)
- EthernetClientInterface TCP/SSH → **RawTcpHandler**
- EthernetClientInterface UDP → **RawSimplePipeHandler**
- SerialInterface / SPInterface → **RawSimplePipeHandler**
- EthernetServerInterfaceEx (TCP only) → **ServerExHandler**
- Global Scripter Module types map to **ModuleTcpHandler** or **ModuleSimplePipeHandler** depending on transport
- DanteInterface → **RawTcpHandler** (Pro xi only; *no* SendAndWait)

(From ConnectionHandler PDF)

### 7.2) Core API that matters in practice

Common fields / properties:
- `ConnectionStatus` → `'Connected' | 'Disconnected' | 'Unknown'`
- `DisconnectLimit` → missed-response threshold (default noted as 15 in docs)
- `PollTimer` → an `extronlib.system.Timer` used internally for keepalive polling
- `Interface` → underlying wrapped interface/module

Key methods:
- `Connect(timeout=None)` → attempt connection + start polling loop
- `AutoReconnect` (bool) → whether to reconnect after disconnect (where supported)
- `Send(data)` → send without waiting
- `SendAndWait(data, timeout, **delimiter)` → send + wait for response (may return empty bytes)
  - delimiter options:
    - `deliLen` (int) expected length
    - `deliTag` (byte) suffix
    - `deliRex` (compiled regex) match
- `ResponseAccepted()` → reset the missed-response counter (call when you confirm a valid keepalive response)

Events:
- `Connected` / `Disconnected`
- `ConnectFailed` (TCP connect failures; provides a “reason” string)
- `ReceiveData` (bytes)

(From ConnectionHandler PDF)

### 7.3) Keepalive + “real world” link loss nuance
From the Extron Python programming guide:
- You often use `StartKeepAlive(interval, query)` after a connection to prevent device idle timeout.
- When using only connect/disconnect events, note:
  - Loss of comms due to network/cabling issues may **not** trigger a `Disconnected` event in some scenarios.
  - A practical strategy is to implement “last response” watchdog logic (restart a Timer on each `ReceiveData`, and if it expires, explicitly `Disconnect()` and reconnect).

(From “Extron Control System Programming Using Python” PDF)

---

## 8) Timing primitives you’ll use constantly

ControlScript provides:
- `Timer` — repeat at interval
- `Wait` — delay a call
- `Clock` — schedule specific times/days

Example pattern for polling:
- Use `@Timer(5)` decorator for a forever poll
- Or create a named `Timer(5, func)` so you can `Stop() / Pause() / Restart()` based on system state.

(From “Extron Control System Programming Using Python” PDF)

### 8.1) `Timer` (periodic scheduling) — exact behavior

From the Pro xi API docs:

- Handler signature must be **exactly**: `(timer, count)`.
- **Minimum interval is 0.1 seconds**.
- If the handler hasn’t finished when the next interval expires, the handler is **skipped** (it’s not queued) and `count` is **not** incremented for that missed interval.

Common operations:

- `Change(new_interval)` — apply to future triggers
- `Pause()` — stop calling the function *without* resetting `count`
- `Resume()` — resume after pause/stop
- `Restart()` — reset `count` and schedule the next run
- `Stop()` — stop and reset `count`
- `State` is `'Running'|'Paused'|'Stopped'` and a `StateChanged` event fires on transitions

### 8.2) `Wait` (one-shot delay, non-blocking)

`Wait` lets you delay actions **without blocking other processor activity**.

Patterns:
- As a decorator (`@Wait(5)`) for a one-shot call
- As a named instance you can reuse and modify

Important methods:
- `Add(seconds)` — adds time to the *current* countdown (does **not** change the base Time)
- `Change(seconds)` — set a new Time for current and future runs
- `Cancel()` — prevent the function from executing when time expires

(From ControlScript Pro xi 1.9r7 docs in index_merged.pdf)

---

## 9) UI patterns: MESet and feedback loops

### 9.1) Mutually Exclusive Sets (`MESet`)
Useful for “one selected at a time” UI states (inputs, modes, relay directions).  
Call `.SetCurrent(obj)` to set one active and clear others.

Useful Pro xi API details:

- `Objects` → list of tracked objects
- `GetCurrent()` → current selected object (or `None`)
- `Append(obj)` / `Remove(obj_or_index)`
- `SetCurrent(obj_or_index_or_None)` → selects; passing `None` deselects all
- `SetStates(obj_or_index, offState, onState)` → override default off/on states (default 0/1)

(From “Extron Control System Programming Using Python” PDF)

### 9.2) Framework example: use MESet only for UI feedback
The Framework doc explicitly notes MESet is for **visual feedback** on UI and doesn’t change device behavior by itself; pair it with actual device `.Set(...)` calls.

(From ControlScript Framework PDF)

### 9.3) “status → UI” via `GenericEvent` bridging
Framework example pattern:
- subscribe device module status to a `GenericEvent.Trigger`
- attach `@eventEx(genericEvent, 'Triggered')` to update a `Level` or other UI object
- optionally poll with a `Timer` calling `.Update('Volume')`

(From ControlScript Framework PDF)

### 9.4) UI object event signatures (so handlers don’t crash)

- `Button`: common events include `Pressed`, `Released`, `Repeated`, `Tapped`.
  - `Tapped` handler signature: `(button, state)` where `state` is a string like `'Tapped'`.
- `Slider`: `Pressed`, `Released`, `Changed` handler signature: `(slider, state, value)`.
- `Knob`: `Turned` handler signature: `(knob, direction)` where direction is signed steps (positive = clockwise).
- `Level`:
  - default range **0–100**, step 1; change with `SetRange(min, max, step=1)`.
  - for multi-state levels, set the range to match the number of states.

(From ControlScript Pro xi 1.9r7 docs in index_merged.pdf)

---

## 10) Multi-room / scalable deployment pattern (from the sample project README)

If you’re building many rooms with one codebase:

- Single shared source tree in `src/`
- Per-room JSON configuration files (one per room) that define:
  - processor & touchpanel type
  - IP addresses / ports / aliases
  - device list + which driver modules to load
  - file paths to shared layouts/resources
- Shared GUI layouts with fixed control IDs across rooms
- Drivers are modular and loaded only when needed
- Deployment via ControlScript Deployment Utility

(From README.pdf)

---

## 11) GlobalViewer Enterprise (GVE) integration (from the sample project README)

For fleet monitoring:
- Use Extron’s `gve_interface` helper module
- Connect all rooms to a shared GVE server
- Map each device to unique GVE IDs via room JSON
- Send status updates (Power, Connection, Lamp hours, etc.)
- Handle remote commands via ReceiveGVECommand event

(From README.pdf)

---

## 12) Codex Agent “generation rules” (copy/paste into your agent)

When generating ControlScript code for this project:

1) Follow the Framework file roles strictly:
   - instantiate in `devices.py`
   - orchestrate connections/timers/services in `system.py` / `Initialize()`
   - UI objects + handlers in `ui/*.py`
   - control logic split by concern in `control/*.py`

2) Prefer `eventEx` (ModuleSupport.py) over `extronlib.event` when:
   - multiple handlers per event are needed
   - you want lists of objects/events in a single handler
   - you want consistent scalable patterns across modules

3) For network/serial controlled devices:
   - wrap the interface with `GetConnectionHandler(...)`
   - implement keepalive polling
   - on `ReceiveData`, parse and call `ResponseAccepted()` when a valid keepalive response is confirmed
   - consider a watchdog if device doesn’t reliably raise Disconnected on link loss

4) Keep UI state and device state separate:
   - MESet for button state feedback only
   - device modules for actual behavior (`Set`, `Update`, status subscriptions)

5) Use timers deliberately:
   - named Timers for start/stop based on system state
   - avoid “always polling everything” when the room is off

6) Logging:
   - accept optional logger in classes
   - centralize logging configuration so it can be disabled without code edits
   - prefer ProgramLog severities appropriately

---

## 13) Source PDFs used
- ControlScriptFramework_v1x0x0-revL.pdf
- ConnectionHandler_v2x3x0b.pdf
- Extron_Cntrl_Sys_Prog_Using_Python_C.pdf
- README.pdf (sample multi-room ControlScript project notes)
- index_merged.pdf (ControlScript Pro xi 1.9r7 library reference)
