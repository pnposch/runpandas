"""
Test module for runpandas frame types (i.e. Activity)
"""


import os
import pytest
import numpy as np
from pandas import Timedelta, Timestamp
from runpandas import reader

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


def test_ellapsed_time_frame(dirpath):

    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_gpx = reader._read_file(gpx_file, to_df=False)
    reset_gpx_file = frame_gpx.reset_index()
    with pytest.raises(AttributeError):
        _ = reset_gpx_file.ellapsed_time

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
    reset_gpx_file = frame_gpx.reset_index()
    with pytest.raises(AttributeError):
        _ = reset_gpx_file.moving_time

    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_without_moving = reader._read_file(gpx_file, to_df=False)
    with pytest.raises(AttributeError):
        _ = frame_without_moving.moving_time

    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx["distpos"] = frame_gpx.compute.distance(correct_distance=False)
    frame_gpx["speed"] = frame_gpx.compute.speed(from_distances=True)
    frame_gpx_only_moving = frame_gpx.only_moving()
    assert frame_gpx_only_moving.moving_time == Timedelta("0 days 01:14:46")

    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    frame_tcx = reader._read_file(tcx_file, to_df=False)
    frame_tcx["distpos"] = frame_tcx.compute.distance(correct_distance=False)
    frame_tcx["speed"] = frame_tcx.compute.speed(from_distances=True)
    frame_tcx = frame_tcx.only_moving()
    assert frame_tcx.moving_time == Timedelta("0 days 00:33:05")

    fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    frame_fit = reader._read_file(fit_file, to_df=False)
    frame_fit_only_moving = frame_fit.only_moving()
    assert frame_fit_only_moving.moving_time == Timedelta("0 days 00:00:55")


def test_distance_frame(dirpath):

    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_no_distance = reader._read_file(gpx_file, to_df=False)
    with pytest.raises(KeyError):
        _ = frame_no_distance.distance

    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx["distpos"] = frame_gpx.compute.distance(correct_distance=False)
    assert round(frame_gpx.distance, 2) == 12594.65

    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    frame_tcx = reader._read_file(tcx_file, to_df=False)
    assert round(frame_tcx.distance, 2) == 4686.31

    fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    frame_fit = reader._read_file(fit_file, to_df=False)
    assert round(frame_fit.distance, 2) == 157.56

    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    assert round(activity_tcx.distance, 2) == 12007.99


def test_mean_speed_frame(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_no_speed = reader._read_file(gpx_file, to_df=False)
    with pytest.raises(AttributeError):
        _ = frame_no_speed.mean_speed()

    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx["distpos"] = frame_gpx.compute.distance(correct_distance=False)
    frame_gpx["speed"] = frame_gpx.compute.speed(from_distances=True)
    frame_gpx_only_moving = frame_gpx.only_moving()

    #Calculate the mean speed with only moving  and smoothing using speed (m/s)
    assert (frame_gpx_only_moving.mean_speed(only_moving=True, smoothing=True)) == 2.7966895287728653
    #Calculate the mean speed with only moving  and no smoothing (total distance)
    assert (frame_gpx_only_moving.mean_speed(only_moving=True, smoothing=False)) == 2.7966895287728653

    #Calculate the mean speed with all data  and no smoothing (total distance)
    assert (frame_gpx_only_moving.mean_speed(only_moving=False, smoothing=False)) == 2.4565339871605874
    #Calculate the mean speed with all data  and smoothing (total distance)
    assert (frame_gpx_only_moving.mean_speed(only_moving=False, smoothing=True)) == 2.4565339871605874


def test_mean_heartrate_frame(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame = reader._read_file(gpx_file, to_df=False)
    frame_no_hr = frame.drop(['hr'], axis=1)
    with pytest.raises(AttributeError):
        _ = frame_no_hr.mean_heart_rate()


    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx["distpos"] = frame_gpx.compute.distance(correct_distance=False)
    frame_gpx["speed"] = frame_gpx.compute.speed(from_distances=True)

    frame_gpx_only_moving = frame_gpx.only_moving()

    assert (frame_gpx_only_moving.mean_heart_rate(only_moving=False)) == 151.22097819681792
    assert (frame_gpx_only_moving.mean_heart_rate(only_moving=True)) == 151.90203327171903


def test_mean_cadence_frame(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame = reader._read_file(gpx_file, to_df=False)
    frame_no_cadence = frame.drop(['cad'], axis=1)
    with pytest.raises(AttributeError):
        _ = frame_no_cadence.mean_cadence()


    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx["distpos"] = frame_gpx.compute.distance(correct_distance=False)
    frame_gpx["speed"] = frame_gpx.compute.speed(from_distances=True)

    frame_gpx_only_moving = frame_gpx.only_moving()

    assert (frame_gpx_only_moving.mean_cadence(only_moving=False)) == 84.99764289923394
    assert (frame_gpx_only_moving.mean_cadence(only_moving=True)) == 85.96118299445472


def test_mean_pace_frame(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame = reader._read_file(gpx_file, to_df=False)
    with pytest.raises(AttributeError):
        _ = frame.mean_pace()


    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx["distpos"] = frame_gpx.compute.distance(correct_distance=False)
    frame_gpx["speed"] = frame_gpx.compute.speed(from_distances=True)

    frame_gpx_only_moving = frame_gpx.only_moving()

    #Calculate the mean pace with only moving  and smoothing using speed (m/s)
    assert (frame_gpx_only_moving.mean_pace(only_moving=True, smoothing=True)) == Timedelta('0 days 00:00:00.357566')
    #Calculate the mean pace with only moving  and no smoothing (total distance)
    assert (frame_gpx_only_moving.mean_pace(only_moving=True, smoothing=False)) == Timedelta('0 days 00:00:00.357566')

    #Calculate the mean pace with all data  and no smoothing (total distance)
    assert (frame_gpx_only_moving.mean_pace(only_moving=False, smoothing=False)) == Timedelta('0 days 00:00:00.407078')
    #Calculate the mean pace with all data  and smoothing (total distance)
    assert (frame_gpx_only_moving.mean_pace(only_moving=False, smoothing=True)) == Timedelta('0 days 00:00:00.407078')


def convert_pace_secmeters2minkms(seconds):
    pace_min = int((seconds * 1000)/60)
    pace_sec = int(seconds * 1000 - (pace_min*60))
    total_seconds = (pace_min * 60) + pace_sec
    return Timedelta(seconds=total_seconds)

def test_full_activity(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    frame_tcx = reader._read_file(tcx_file, to_df=False)

    #test_hr_values_are_correct
    assert frame_tcx['hr'].iloc[-1] == 180
    assert frame_tcx['hr'].iloc[0] == 62

    #test_altitude_points_are_correct
    assert frame_tcx['alt'].iloc[-1] == 166.4453125
    assert frame_tcx['alt'].iloc[0] == 178.942626953

    #test_time_values_are_correct
    assert frame_tcx.index[-1] ==  Timedelta('0 days 00:33:11')
    assert frame_tcx.index[0] == Timedelta('0 days 00:00:00')

    #test_time_values_are_correct
    assert frame_tcx.start ==  Timestamp("2012-12-26 21:29:53+00:00")

    #test_latitude_is_correct
    assert frame_tcx['lat'].iloc[0] == 35.951880198
    assert frame_tcx['lon'].iloc[0] == -79.0931872185

    #test_distance_is_correct
    assert frame_tcx.distance ==  4686.31103516

    #test_duration_is_correct (we don't consider fraction time)
    assert frame_tcx.ellapsed_time.total_seconds() ==  1991

    #test_hr_max
    assert frame_tcx['hr'].max() == 189

    #test_hr_min
    assert frame_tcx['hr'].min() == 60

    #test_hr_avg
    assert int(frame_tcx['hr'].mean()) == 156

    #test_speed
    frame_tcx['distpos'] = frame_tcx.compute.distance()
    frame_tcx['speed'] = frame_tcx.compute.speed(from_distances=True)
    assert frame_tcx.mean_speed() == 2.3545989706033197

    #test_pace (converted to seconds) "07:04"
    pace_min_km = convert_pace_secmeters2minkms(frame_tcx.mean_pace().total_seconds())
    assert  pace_min_km  == Timedelta('0 days 00:07:04')

    #test_altitude_avg_is_correct
    assert frame_tcx['alt'].mean() == 172.02005618422717

    #test_altitude_max_is_correct
    assert frame_tcx['alt'].max() == 215.95324707

    #test_altitude_min_is_correct
    assert frame_tcx['alt'].min() == 157.793579102

    #test_ascent_is_correct
    assert frame_tcx['alt'].ascent.sum() == 153.80981445000003

    #test_descent_is_correct
    assert frame_tcx['alt'].descent.sum() == -166.30712890300003

    #test_distance_values_are_correct
    frame_tcx['dist'] = frame_tcx['distpos'].to_distance()
    assert frame_tcx['dist'].fillna(0).iloc[0] == 0.0  #(NaN number for position 0)
    assert frame_tcx['dist'].iloc[-1] == 4688.006550471207  #4686.31103516 (Precision?)