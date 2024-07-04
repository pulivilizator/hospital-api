from environs import Env
from dataclasses import dataclass


@dataclass
class SMTP:
    host: str
    host_user: str
    password: str
    port: str


@dataclass
class Frontend:
    domain: str


@dataclass
class S3:
    selectel_url: str
    endpoint_url: str
    access_key_id: str
    secret_access_key: str
    bucket_name: str


@dataclass
class Database:
    dsn: str


@dataclass
class Django:
    secret_key: str
    debug: bool
    allowed_hosts: list
    csrf_trusted_origins: list
    cors_allowed_origins: list


@dataclass
class Config:
    smtp: SMTP
    frontend: Frontend
    s3: S3
    database: Database
    django: Django


def get_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        smtp=SMTP(
            host=env('EMAIL_HOST'),
            host_user=env('EMAIL_HOST_USER'),
            password=env('EMAIL_HOST_PASSWORD'),
            port=env('EMAIL_PORT'),
        ),

        frontend=Frontend(
            domain=env('FRONTEND_DOMAIN'),
        ),

        s3=S3(
            selectel_url=env('SELECTEL_CUSTOM_URL'),
            endpoint_url=env('S3_ENDPOINT_URL'),
            access_key_id=env('S3_ACCESS_KEY_ID'),
            secret_access_key=env('S3_SECRET_ACCESS_KEY'),
            bucket_name=env('STORAGE_BUCKET_NAME'),
        ),

        database=Database(
            dsn=env('DATABASE_URL'),
        ),
        django=Django(
            secret_key=env('DJANGO_SECRET_KEY'),
            debug=env.bool('DEBUG_MODE', default=False),
            allowed_hosts=env.list('ALLOWED_HOSTS', delimiter=' '),
            csrf_trusted_origins=env.list('CSRF_TRUSTED_ORIGINS', delimiter=' '),
            cors_allowed_origins=env.list('CORS_ALLOWED_ORIGINS', delimiter=' '),
        )
    )
