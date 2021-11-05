import os
import pathlib
from dotenv import load_dotenv

"""
You should create a .env file in the root folder.
Inside this file enter any sensitive information that you don't want track online, such as credentials.
WARNING: The .env file should be included inside the .gitignore file
"""

dotenv_path = pathlib.Path(__file__).parents[1] / '.env'
load_dotenv(dotenv_path)

VALID_USERNAME = os.environ.get("VALID_USERNAME")
VALID_PASSWORD = os.environ.get("VALID_PASSWORD")
