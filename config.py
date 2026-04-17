from pathlib import Path
import logging
BASE_DIR = Path(__file__).resolve().parent

# must import config for logging to work
logging.basicConfig(
        level=logging.INFO, 
        handlers=[logging.FileHandler('pipeline.log'), logging.StreamHandler()],
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %I:%M:%S')