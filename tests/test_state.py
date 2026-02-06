import time
from state import prune_state


class TestPruneState:
    def test_removes_stale_entries(self):
        state = {
            1: {"ts": time.time() - 1000},
            2: {"ts": time.time()},
        }
        prune_state(state, ttl_seconds=500)
        assert 1 not in state
        assert 2 in state

    def test_keeps_fresh_entries(self):
        state = {
            1: {"ts": time.time()},
            2: {"ts": time.time()},
        }
        prune_state(state, ttl_seconds=600)
        assert len(state) == 2

    def test_removes_all_stale(self):
        state = {
            1: {"ts": time.time() - 2000},
            2: {"ts": time.time() - 2000},
        }
        prune_state(state, ttl_seconds=100)
        assert len(state) == 0

    def test_empty_state(self):
        state = {}
        prune_state(state, ttl_seconds=100)
        assert len(state) == 0
