import logging

logger = logging.getLogger("audit")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler("audit.log")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def audit(action: str, details: str):
    logger.info(f"{action} | {details}")
