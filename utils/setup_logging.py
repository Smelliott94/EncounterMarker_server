import logging

# Define ANSI escape codes for colors
COLORS = {
    'DEBUG': '\033[94m',  # Blue
    'INFO': '\033[92m',   # Green
    'WARNING': '\033[93m',  # Yellow
    'ERROR': '\033[91m',   # Red
    'CRITICAL': '\033[91m\033[1m'  # Red and bold
}

RESET = '\033[0m'  # Reset color

# Create a custom formatter with color for the timestamp
class ColoredTimestampFormatter(logging.Formatter):
    def format(self, record):
        log_level = record.levelname
        color = COLORS.get(log_level, '')
        message = super(ColoredTimestampFormatter, self).format(record)
        timestamp = f"{color}{record.asctime}{RESET}"
        return message.replace(record.asctime, timestamp)

logger = logging.getLogger()
# Create a StreamHandler to display logs in the terminal
console_handler = logging.StreamHandler()

# Set the formatter for the console handler
console_formatter = ColoredTimestampFormatter("%(asctime)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(console_formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)

# Set the log level
logger.setLevel(logging.INFO)