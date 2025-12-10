import threading
from bot import run_bot
from server import run_flask
import time

if __name__ == "__main__":
    web = threading.Thread(target=run_flask)
    web.daemon = True  
    web.start()

    run_bot()