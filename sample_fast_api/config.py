from prettyconf import config


class Settings:
    DATABASE_URL = config("DATABASE_URL")
    TEST_DATABASE_URL = config("TEST_DATABASE_URL")
    TEST_ENV = config("TEST_ENV", default=False, cast=config.boolean)


settings = Settings()
