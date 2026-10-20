# from pathlib import Path

# PROJECT_ROOT = Path(__file__).resolve().parent.parent

# DATA_DIR = PROJECT_ROOT / "data"
# RAW_DATA = DATA_DIR / "raw" / "ai4i2020.csv"
# TRAIN_DATA = DATA_DIR / "processe" / "train.csv"
# TEST_DATA = DATA_DIR / "processe" / "test.csv"

# MODEL_PATH = PROJECT_ROOT / "models" / "model.pkl"

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Main directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processe"

MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "model.pkl"

# Dataset paths
RAW_DATA_PATH = RAW_DATA_DIR / "ai4i2020.csv"
TRAIN_DATA_PATH = PROCESSED_DATA_DIR / "train.csv"
TEST_DATA_PATH = PROCESSED_DATA_DIR / "test.csv"