"""Escolhe banco e armazenamento conforme o que estiver acessível."""

import os
import sys
import warnings


def resolve_database(base_dir):
    """Usa Postgres quando a conexão abre. Caso contrário, cria um SQLite local."""
    if os.environ.get("DB_ENGINE", "").strip().lower() == "sqlite":
        warnings.warn("DB_ENGINE=sqlite. Usando o arquivo db.sqlite3.", stacklevel=2)
        return _sqlite(base_dir), True

    config = _postgres_config()
    if _postgres_reachable(config):
        return config, False

    warnings.warn(
        "Postgres indisponível. Os dados vão para o SQLite em db.sqlite3.",
        stacklevel=2,
    )
    return _sqlite(base_dir), True


def resolve_storage():
    """Usa S3 ou R2 quando o bucket responde. Caso contrário, a pasta media/."""
    if not _object_storage_configured():
        return "django.core.files.storage.FileSystemStorage", False
    if _object_storage_reachable():
        return "core.storage.S3CompatibleStorage", True
    warnings.warn(
        "S3/R2 indisponível. As imagens vão para a pasta media/.",
        stacklevel=2,
    )
    return "django.core.files.storage.FileSystemStorage", False


def ensure_sqlite_schema():
    """Cria as tabelas no SQLite de fallback na primeira subida."""
    if os.environ.get("SAMBAIBA_SQLITE_MIGRATED") == "1":
        return
    if any(cmd in sys.argv for cmd in ("migrate", "makemigrations", "showmigrations", "test")):
        return
    if "runserver" in sys.argv and os.environ.get("RUN_MAIN") != "true":
        return

    os.environ["SAMBAIBA_SQLITE_MIGRATED"] = "1"
    from pathlib import Path

    import sqlite3
    from django.conf import settings

    path = Path(settings.DATABASES["default"]["NAME"])
    if path.exists():
        with sqlite3.connect(path) as conn:
            found = {
                row[0]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table' AND name IN ('django_migrations', 'users_user')"
                )
            }
        if {"django_migrations", "users_user"} <= found:
            return

    from django.core.management import call_command

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="Accessing the database during app initialization is discouraged",
        )
        call_command("migrate", interactive=False, verbosity=1)


def _postgres_config():
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "sambaiba"),
        "USER": os.environ.get("POSTGRES_USER", "sambaiba"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "sambaiba"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "OPTIONS": {"connect_timeout": 3},
    }


def _sqlite(base_dir):
    path = base_dir / "db.sqlite3"
    path.parent.mkdir(parents=True, exist_ok=True)
    return {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": path,
    }


def _postgres_reachable(config) -> bool:
    try:
        import psycopg
    except ImportError as exc:
        warnings.warn(f"psycopg não está instalado ({exc}). Usando SQLite.", stacklevel=2)
        return False
    try:
        with psycopg.connect(
            dbname=config["NAME"],
            user=config["USER"],
            password=config["PASSWORD"],
            host=config["HOST"],
            port=config["PORT"],
            connect_timeout=3,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
        return True
    except Exception as exc:
        warnings.warn(f"Falha ao conectar no Postgres: {exc}", stacklevel=2)
        return False


def _object_storage_configured() -> bool:
    return all(
        os.environ.get(name, "").strip()
        for name in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_STORAGE_BUCKET_NAME")
    )


def _object_storage_reachable() -> bool:
    try:
        import boto3
        from botocore.config import Config
    except ImportError:
        warnings.warn("boto3 não está instalado. As imagens vão para a pasta media/.", stacklevel=2)
        return False
    try:
        client = boto3.client(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            region_name=os.environ.get("AWS_S3_REGION_NAME", "auto") or "auto",
            endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL") or None,
            config=Config(connect_timeout=3, read_timeout=3, retries={"max_attempts": 1}),
        )
        client.head_bucket(Bucket=os.environ["AWS_STORAGE_BUCKET_NAME"])
        return True
    except Exception as exc:
        warnings.warn(f"Falha ao acessar o bucket S3/R2: {exc}", stacklevel=2)
        return False
