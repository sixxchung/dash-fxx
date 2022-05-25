# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), os.getenv("ENVIRONMENT_FILE", '.env.development'))
load_dotenv(dotenv_path=dotenv_path, override=True)


