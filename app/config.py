from prettyconf import config


class Settings:
    DATABASE_URL = config("DATABASE_URL")


settings = Settings()
