from prettyconf import config


class Settings:
    DATABASE_URL = config("DATABASE_URL")
    TEST_DATABASE_URL = config("TEST_DATABASE_URL")
    TEST_ENV = config("TEST_ENV", default=False, cast=config.boolean)
    SECRET_KEY = config("SECRET_KEY")
    ALGORITHM = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default="30", cast=config.eval)


settings = Settings()
