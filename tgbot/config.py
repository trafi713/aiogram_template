from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    user: str
    password: str
    database: str
    host: str
    port: int = 5432


@dataclass
class TgBot:
    token: str
    log_id: int


@dataclass
class Miscellaneous:
    use_redis: bool


@dataclass
class Config:
    db: DbConfig
    tg: TgBot
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        db=DbConfig(
            user=env.str('POSTGRES_USER'),
            password=env.str('POSTGRES_PASSWORD'),
            database=env.str('POSTGRES_DB'),
            host=env.str('POSTGRES_HOST'),
        ),
        tg=TgBot(
            token=env.str('BOT_TOKEN'),
            log_id=env.int('LOG')
        ),
        misc=Miscellaneous(
            use_redis=env.bool('USE_REDIS')
        ),

    )
