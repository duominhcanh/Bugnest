from app import App
from module import logger

if __name__ == '__main__':
    logger.init()
    while True:
        try:
            app= App()
            app.run()
        except Exception as ex: 
            logger.error(ex, 'main')