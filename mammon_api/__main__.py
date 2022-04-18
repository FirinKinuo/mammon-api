from logging import getLogger

from mammon_api.settings import config

log = getLogger("main")

if __name__ == "__main__":
    print(f"Start Mammon API at host: {config.API_HOST}:{config.API_PORT}")
