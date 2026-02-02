import subprocess
import threading
import time
from app.common import logger, CustomExceptions
from dotenv import load_dotenv

c_exceptions = CustomExceptions.CustomException
logger = logger.get_logger(__name__)

load_dotenv()

def run_backend():
    try:
        logger.info("Starting the backend server...!!!!")
        subprocess.run(["uvicorn","src.app.backend.api:app","--host","127.0.0.1", "--port", "8080"], check=True)
    except c_exceptions as e:
        logger.error(f"Problem with the application beacuse of the follwoing error {e}")
        raise c_exceptions("Failed to start the backend server for the following error",e)
    
def run_frontend():
    try:
        logger.info("Starting the frontend service...!!")
        subprocess.run(["streamlit","run","src/app/frontend/ui.py"],check=True)

    except c_exceptions as e:
        logger.error(f"Problem with the application beacuse of the follwoing error {e}")
        raise c_exceptions("Failed to start the frontend server for the following error",e)
    

if __name__=="__main__":
    try:
        threading.Thread(target=run_backend).start()
        time.sleep(3)
        run_frontend()
    except Exception as e:
        error_message = c_exceptions("unable to run the application",e)
        logger.error(str(error_message))