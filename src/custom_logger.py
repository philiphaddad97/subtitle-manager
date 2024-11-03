import logging


class CustomLogger:
    def __init__(self, name: str = "ApplicationLogger", level: int = logging.DEBUG, log_to_file: bool = False, log_file: str = "app.log"):
        """
        Initializes a custom logger.

        :param name: Name of the logger.
        :param level: Logging level (e.g., logging.DEBUG, logging.INFO).
        :param log_to_file: If True, logs are written to a file as well as console.
        :param log_file: Filename for log file if logging to file.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Check if handlers are already added to prevent duplicate logs
        if not self.logger.hasHandlers():
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

            # Optional file handler
            if log_to_file:
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(level)
                file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """Returns the configured logger instance."""
        return self.logger