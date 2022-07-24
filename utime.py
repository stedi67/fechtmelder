import time
global_ms_tick = 0


def ticks_diff(t1: int, t2: int) -> int:
    return t1 - t2


def ticks_ms():
    return global_ms_tick


def sleep(time_delta):
    time.sleep(time_delta)
    global global_ms_tick
    global_ms_tick += time_delta * 1000


def sleep_ms(time_delta):
    time.sleep(time_delta / 1000)
    global global_ms_tick
    global_ms_tick += time_delta
