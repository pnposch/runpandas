"""
Test module for runpandas frame types (i.e. Activity)
"""


import os
import pytest
from pandas import Timedelta
from runpandas import reader

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


def test_ellapsed_time_frame(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_gpx = reader._read_file(gpx_file, to_df=False)
    assert frame_gpx.ellapsed_time == Timedelta("0 days 01:25:27")

    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    frame_tcx = reader._read_file(tcx_file, to_df=False)
    assert frame_tcx.ellapsed_time == Timedelta("0 days 00:33:11")

    fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    frame_fit = reader._read_file(fit_file, to_df=False)
    assert frame_fit.ellapsed_time == Timedelta("0 days 00:00:57")

def test_moving_time_frame(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_gpx = reader._read_file(gpx_file, to_df=False)
    assert frame_gpx.ellapsed_time == Timedelta("0 days 01:25:27")

    #tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    #frame_tcx = reader._read_file(tcx_file, to_df=False)
    #assert frame_tcx.ellapsed_time == Timedelta("0 days 00:33:11")

    #fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    #frame_fit = reader._read_file(fit_file, to_df=False)
    #assert frame_fit.ellapsed_time == Timedelta("0 days 00:00:57")