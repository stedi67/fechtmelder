from fechtmelder import (
    evaluate_florett,
    FlorettStatus,
    FLORETT_SPITZE_ON,
    KONTAKT_ON,
    FLORETT_SPITZE_OFF,
    KONTAKT_OFF,
    RED,
    GREEN,
)
import utime


def test_init():
    status = FlorettStatus(GREEN)
    assert status.color == GREEN
    assert status.status == 'init'


def test_check_values():
    status = FlorettStatus(GREEN)
    status.check(
        (FLORETT_SPITZE_OFF, KONTAKT_ON, FLORETT_SPITZE_ON, KONTAKT_OFF))
    assert status.last_spitze == FLORETT_SPITZE_OFF
    assert status.last_kontakt == KONTAKT_ON

    status = FlorettStatus(RED)
    status.check(
        (FLORETT_SPITZE_OFF, KONTAKT_ON, FLORETT_SPITZE_ON, KONTAKT_OFF))
    assert status.last_spitze == FLORETT_SPITZE_ON
    assert status.last_kontakt == KONTAKT_OFF


def test_treffer():
    status = FlorettStatus(GREEN)
    assert status.treffer_start is None
    status.check((FLORETT_SPITZE_ON, KONTAKT_OFF, None, None))
    assert status.treffer_start is not None
    assert status.status == 'init'
    utime.global_ms_tick = 16
    status.check((FLORETT_SPITZE_ON, KONTAKT_OFF, None, None))
    assert status.status == 'treffer_ok'
    utime.global_ms_tick = 100
    assert status.treffer_und_kontakt_start is None
    status.check((FLORETT_SPITZE_ON, KONTAKT_ON, None, None))
    assert status.status == 'treffer_und_kontakt'
    assert status.treffer_und_kontakt_start is not None


SUCCESSFUL_GREEN = (
    (0,
     (FLORETT_SPITZE_OFF, KONTAKT_ON, FLORETT_SPITZE_OFF, KONTAKT_OFF),
     (False, False, False, False)),
    (20,
     (FLORETT_SPITZE_ON, KONTAKT_ON, FLORETT_SPITZE_OFF, KONTAKT_OFF),
     (False, False, False, False)),
    (40,
     (FLORETT_SPITZE_ON, KONTAKT_ON, FLORETT_SPITZE_OFF, KONTAKT_OFF),
     (False, False, False, False)),
    (80,
     (FLORETT_SPITZE_ON, KONTAKT_ON, FLORETT_SPITZE_OFF, KONTAKT_OFF),
     (False, False, False, False)),
    (400,
     (FLORETT_SPITZE_ON, KONTAKT_ON, FLORETT_SPITZE_OFF, KONTAKT_OFF),
     (True, False, False, False)),
)


def test_florett_evaluation():
    status_gruen = FlorettStatus(GREEN)
    status_rot = FlorettStatus(RED)
    for time_delta, values, expected_result in SUCCESSFUL_GREEN:
        utime.global_ms_tick = time_delta
        result = evaluate_florett(status_gruen, status_rot, values)
        assert all(bool(x[0]) == x[1] for x in zip(result, expected_result)),\
            (time_delta, values, expected_result)
