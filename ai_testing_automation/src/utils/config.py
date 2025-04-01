import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Base URL for the demo site
BASE_URL = "https://demoblaze.com"

# Output file paths
ELEMENTS_JSON_PATH = "output/elements.json"
TEST_CASES_PATH = "output/test_cases.xlsx"
TEST_SCRIPTS_PATH = "output/test_scripts.xlsx"