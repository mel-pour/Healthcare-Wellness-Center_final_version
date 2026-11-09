import logging
from pathlib import Path

# The log file lives in spa/logs/app.log. The folder is created if it is missing.
LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "app.log"
LOG_FILE.parent.mkdir(exist_ok=True)

logger = logging.getLogger("healthcare")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    # delay=True: the file is only opened when the first message is written.
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8", delay=True)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
