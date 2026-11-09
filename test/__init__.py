import logging

# Keep test runs out of the real log file. Tests that check logging turn it back on themselves.
logging.disable(logging.CRITICAL)
