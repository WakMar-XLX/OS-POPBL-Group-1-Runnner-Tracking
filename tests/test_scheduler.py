"""Basic tests. Run with:  python -m pytest"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from scheduler import Wave, schedule, state_at

WAVES = [Wave("A", 0, 8, 2, 10), Wave("B", 1, 4, 1, 10), Wave("C", 2, 6, 3, 10)]


def runs(result):
    return [s for s in result["slices"] if s["type"] == "run"]


def test_fcfs_follows_arrival_order():
    r = schedule(WAVES, "FCFS", switch=0)
    assert [s["wave"] for s in runs(r)] == [0, 1, 2]


def test_priority_picks_lowest_number_next():
    r = schedule(WAVES, "Priority", switch=0)
    assert [s["wave"] for s in runs(r)] == [0, 1, 2]   # A is already on the line
    r2 = schedule([Wave("A", 0, 5, 3, 1), Wave("B", 0, 5, 1, 1)], "Priority", switch=0)
    assert runs(r2)[0]["wave"] == 1


def test_round_robin_respects_quantum():
    r = schedule(WAVES, "Round Robin", quantum=3, switch=0)
    assert all(s["end"] - s["start"] <= 3 for s in runs(r))


def test_waiting_equals_turnaround_minus_burst():
    r = schedule(WAVES, "FCFS", switch=0)
    # A:0-8, B:8-12, C:12-18 -> waiting 0, 7, 10 -> average 5.67
    assert round(r["avg_waiting"], 2) == 5.67


def test_states():
    r = schedule(WAVES, "FCFS", switch=0)
    assert state_at(WAVES, r, 2, 0) == "New"
    assert state_at(WAVES, r, 0, 0) == "Running"
    assert state_at(WAVES, r, 1, 3) == "Ready"
    assert state_at(WAVES, r, 0, 99) == "Terminated"
