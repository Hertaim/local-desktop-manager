from dotenv import load_dotenv
import os

load_dotenv()

flask_secret_key = os.getenv("FLASK_SECRET_KEY")



