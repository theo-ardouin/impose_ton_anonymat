import logging


def init_global_logger(file_path: str | None) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s [ %(levelname)s ] (%(name)s) %(message)s")

    if file_path:
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    output_handler = logging.StreamHandler()
    output_handler.setLevel(logging.INFO)
    output_handler.setFormatter(formatter)
    logger.addHandler(output_handler)

    logging.getLogger("discord").setLevel(logging.WARNING)
