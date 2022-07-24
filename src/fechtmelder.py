from machine import Pin
import utime


def timer_delta(timer):
    if timer:
        return utime.ticks_diff(timer, utime.ticks_ms())


class FlorettStatus:

    def __init__(self, color):
        self.color = color
        self.reset()

    def check(self, check_values):
        # mit timer sind wir mindestens 15 ms mit geschlossener Spitze
        if self.color == 'gruen':
            spitze, kontakt = check_values[:2]
        else:
            spitze, kontakt = check_values[2:]
        if spitze == 0 and self.treffer_start is not None:
            self.status = 'treffer_ok'
        # Noch kein timer
        elif spitze == 0:
            self.treffer_start = utime.ticks_ms()
        if kontakt == 1 and self.kontakt_start is not None:
            self.kontakt_start = utime.ticks_ms()
        if kontakt == 1:
            if self.status == 'treffer_ok':
                self.status = 'treffer_und_kontakt'
                self.treffer_und_kontakt_start = utime.ticks_ms()
            else:
                self.status = 'kontakt'

    def reset(self):
        self.status = 'init'
        self.treffer_start = None
        self.kontakt_start = None
        self.treffer_und_kontakt_start = None


class FechtController:

    def __init__(self):
        self.buzzer = Pin(15, Pin.OUT, Pin.PULL_UP)
        self.gruen_spitze = Pin(10, Pin.IN, Pin.PULL_DOWN)
        self.gruen_kontakt = Pin(11, Pin.IN, Pin.PULL_DOWN)
        self.rot_spitze = Pin(12, Pin.IN, Pin.PULL_DOWN)
        self.rot_kontakt = Pin(13, Pin.IN, Pin.PULL_DOWN)
        self.led_gruen_farbe = Pin(20, Pin.OUT)
        self.led_gruen_weiss = Pin(21, Pin.OUT)
        self.led_rot_farbe = Pin(19, Pin.OUT)
        self.led_rot_weiss = Pin(18, Pin.OUT)
        self.reset_buzzer()

    def reset_buzzer(self):
        utime.sleep(.1)
        self.buzzer.value(1)
        utime.sleep(.1)

    def reset(self):
        self.reset_buzzer()
        self.led_gruen_farbe.off()
        self.led_gruen_weiss.off()
        self.led_rot_farbe.off()
        self.led_rot_weiss.off()

    def test_led(self, led):
        led.on()
        utime.sleep(1)
        led.off()

    def buzz(self, time_delta):
        self.buzzer.value(0)
        utime.sleep(time_delta)
        self.buzzer.value(1)

    def test(self):
        self.buzzer.value(0)
        utime.sleep(1)
        self.reset_buzzer()
        self.test_led(self.led_gruen_farbe)
        self.test_led(self.led_gruen_weiss)
        self.test_led(self.led_rot_farbe)
        self.test_led(self.led_rot_weiss)

    def evaluate_florett(self, florett_gruen, florett_rot):
        florett_gruen.check(self.value_check())
        florett_rot.check(self.value_check())
        delta_gruen = timer_delta(florett_gruen.treffer_und_kontakt_start)
        delta_rot = timer_delta(florett_rot.treffer_und_kontakt_start)
        ungueltig_gruen = timer_delta(florett_gruen.treffer_start)
        ungueltig_rot = timer_delta(florett_rot.treffer_start)
        if delta_gruen and delta_rot:
            return florett_gruen, florett_rot, None, None
        if delta_gruen and delta_gruen > 300:
            return florett_gruen, None, None, None
        if delta_rot and delta_rot > 300:
            return None, florett_rot, None, None
        if ungueltig_rot and ungueltig_rot > 350:
            return None, None, None, florett_rot
        if ungueltig_gruen and ungueltig_gruen > 350:
            return None, None, florett_gruen, None
        return None, None, None, None

    def run_florett(self):
        florett_gruen = FlorettStatus('gruen')
        florett_rot = FlorettStatus('rot')
        while True:
            self.tick()
            gruen, rot, gruen_ungueltig, rot_ungueltig = self.evaluate_florett(
                florett_gruen,
                florett_rot,
            )
            do_break = False
            if gruen:
                self.led_gruen_farbe.on()
                do_break = True
            if rot:
                self.led_rot_farbe.on()
                do_break = True
            if gruen_ungueltig:
                self.led_gruen_weiss.on()
                do_break = True
            if rot_ungueltig:
                self.led_rot_weiss.on()
                do_break = True
            if do_break:
                break

    def run(self):
        while True:
            self.run_florett()
            self.buzz(2)
            utime.sleep(5)
            self.reset()

    def tick(self):
        utime.sleep_ms(15)

    def value_check(self):
        return (
            self.gruen_spitze.value(),
            self.gruen_kontakt.value(),
            self.rot_spitze.value(),
            self.rot_kontakt.value(),
        )


def test_ticks():
    t0 = utime.ticks_ms()
    for i in range(10):
        t1 = utime.ticks_ms()
        print(utime.ticks_diff(t0, t1))
        t0 = t1


def fechtmelder():
    controller = FechtController()
    controller.test()

    return controller
