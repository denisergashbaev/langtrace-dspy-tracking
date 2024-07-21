import shutil
from pathlib import Path

from loguru import logger


def main() -> None:
    # same dir as defined in "dsp.modules.cache_utils"
    path = Path.home().joinpath("cachedir_joblib")
    if not (path.exists() or path.is_dir()):
        logger.error(f"Path {path} does not exist or is not a directory")
        return
    logger.info(f"Removing {path}")
    shutil.rmtree(path)


if __name__ == "__main__":
    main()
