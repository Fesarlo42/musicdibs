from dotenv import load_dotenv
import os

load_dotenv() # load the variables

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_NAME = os.getenv("DATABASE_NAME", "musicdibs")

# DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}/{DATABASE_NAME}"
DATABASE_URL = (
    f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASS}@/{DATABASE_NAME}"
    f"?unix_socket={DATABASE_HOST}"
)