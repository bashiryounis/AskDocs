import logging

def setup_logging():
    """
    Configure logging for the application.
    """
    logging.basicConfig(
        level=logging.INFO,  # Set the desired log level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Log to console
            logging.FileHandler('app.log')  # Log to file
        ]
    )
