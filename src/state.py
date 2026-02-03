import time

def prune_state(state_by_user, ttl_seconds: int):
    now = time.time()
    stale = [k for k, v in state_by_user.items() if now - v["ts"] > ttl_seconds]
    for k in stale:
        state_by_user.pop(k, None)
