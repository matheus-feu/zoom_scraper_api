import logging


def init_logs():
    """
    Initialize the logging configuration and return a logger instance.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log"),
        ],
    )
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("redis").setLevel(logging.INFO)

    return logging.getLogger("app")


logger = init_logs()
