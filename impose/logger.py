import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s [ %(levelname)s ] %(message)s")

file_handler = logging.FileHandler("impose.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
LOGGER.addHandler(file_handler)

output_handler = logging.StreamHandler()
output_handler.setLevel(logging.INFO)
output_handler.setFormatter(formatter)
LOGGER.addHandler(output_handler)
