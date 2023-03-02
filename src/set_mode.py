# Define a function to set the mode and activate the corresponding pins for a certain duration

def set_mode(mode, duration):
    # Check if the mode is valid
    if mode not in Modes:
        print(f"Invalid mode: {mode}")
        return
    # Check if the duration is valid
    if duration <= 0:
        print(f"Invalid duration: {duration}")
        return
    # Get the pin values for the selected mode
    valves = mode.value
    # Activate the corresponding pins for the selected mode
    for i, valve in enumerate(PINS):
        valve.mode = pyfirmata.OUTPUT
        valve.write(valves[i])
    # Wait for the specified duration
    time.sleep(duration)
    # Deactivate all pins
    for pin in PINS:
        pin.write(CLOSE)
