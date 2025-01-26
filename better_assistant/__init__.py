import os

from dotenv import load_dotenv

if os.getenv("ENV") == "TEST":
    load_dotenv(".env.test")
elif os.getenv("ENV") == "PROD":
    pass
else:  # in dev
    load_dotenv(".env.dev")
