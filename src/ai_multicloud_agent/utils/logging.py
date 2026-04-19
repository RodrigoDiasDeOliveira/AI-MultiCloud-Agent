import logging
from typing import Union


def setup_logging(level: Union[str, int] = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
