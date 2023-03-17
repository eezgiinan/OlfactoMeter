from threading import Event

event = Event()

if event.is_set():
    event.set()

    event.clear()

    event.wait()

    event.wait(timeout=5)