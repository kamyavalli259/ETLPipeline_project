import logging

def setup_logger():
    # Create a logger
    logger = logging.getLogger("etl_pipeline")
    logger.setLevel(logging.DEBUG)  

    '''

    # Create a console handler to print logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    '''

    # Create a file handler to log to a file (optional)
    file_handler = logging.FileHandler("etl_pipeline.log")
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    #console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    #logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Create a single logger instance that other modules can import
logger = setup_logger()