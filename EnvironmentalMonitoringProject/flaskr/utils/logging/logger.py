import logging
import os


def set_root_logger():
    try:
        # Create logs directory if it doesn't exist
        logs_dir = "app_logs"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # Create and configure root logger
        logging.basicConfig(filename=os.path.join(logs_dir, "env_mon_proj.log"),
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filemode='a+')

        # Get the logger instance
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)  # Set the threshold of logger to INFO

        return logger
    except Exception as e:
        print(f"Error setting up logger: {e}")


# Usage example:
logger = set_root_logger()
logger.info("Logger initialized successfully.")
