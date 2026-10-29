import unittest

from tests._loader import load_drill

MODULE = load_drill("drill_06_retry")


class RetryTests(unittest.TestCase):
    def test_returns_immediate_success(self):
        self.assertEqual(MODULE.call_with_retry(lambda: "ok", sleep_fn=lambda seconds: None), "ok")

    def test_retries_temporary_errors_with_backoff(self):
        attempts = []
        delays = []

        def operation():
            attempts.append(1)
            if len(attempts) < 3:
                raise TimeoutError("temporary")
            return "recovered"

        result = MODULE.call_with_retry(operation, max_attempts=3, sleep_fn=delays.append)
        self.assertEqual(result, "recovered")
        self.assertEqual(len(attempts), 3)
        self.assertEqual(delays, [1, 2])

    def test_reraises_after_last_attempt(self):
        with self.assertRaises(ConnectionError):
            MODULE.call_with_retry(lambda: (_ for _ in ()).throw(ConnectionError("down")), max_attempts=2, sleep_fn=lambda seconds: None)

    def test_does_not_retry_programming_error(self):
        calls = []

        def operation():
            calls.append(1)
            raise ValueError("bad input")

        with self.assertRaises(ValueError):
            MODULE.call_with_retry(operation, sleep_fn=lambda seconds: None)
        self.assertEqual(len(calls), 1)

    def test_rejects_zero_attempts(self):
        with self.assertRaises(ValueError):
            MODULE.call_with_retry(lambda: "ok", max_attempts=0)


if __name__ == "__main__":
    unittest.main()
