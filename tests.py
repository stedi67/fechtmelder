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
