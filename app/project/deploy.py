from project.settings import *

load_dotenv(dotenv_path=f'{Path(__file__).parent.parent}/.env', override=True)

DEBUG = False
CORS_ALLOW_ALL_ORIGINS = False
