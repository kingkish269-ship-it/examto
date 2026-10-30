# 02 — Write your own detection rule

Goal: add a rule that flags a **burst of HTTP 401/403 responses from one IP**
(credential stuffing or token brute force against an API).

## Steps

1. Open `detections.py`. Copy the shape of `detect_brute_force`.
2. Write `detect_auth_error_burst(events, threshold=10, window=60)`:
   - consider only `type == "http"` events with `status` in `{401, 403}`,
   - group by `src_ip`,
   - alert HIGH when one IP exceeds `threshold` within `window` seconds.
3. Add it to `ALL_RULES`.
4. Add sample events to `data/events.json`: a burst of 401s from one IP (should
   alert) and a couple of benign 401s from another IP (must not alert).
5. Add a test in `tests/test_detections.py` asserting the rule fires on the
   attack IP and stays quiet on the benign one.
6. Run:

```bash
python3 -m unittest discover -v
python3 run_detections.py
```

## The discipline this teaches

A good rule is judged on two errors at once:

- **False negatives** — it must catch the real attack.
- **False positives** — it must ignore normal behaviour.

Your test encodes both. That paired test (fires on attack, quiet on benign) is
what separates a production-ready detection from a noisy one.

## Going further

Translate your rule into Sigma (the vendor-neutral detection format) and note
how it would run as a Splunk or Sentinel query. The logic you wrote in Python
maps directly.
