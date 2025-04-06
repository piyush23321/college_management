from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config.configuration import get_config

# ✅ Create the base class for SQLAlchemy models
Base = declarative_base()


class DbConnection:

    @staticmethod
    def construct_db_url():
        configure = get_config()
        database_url, database_port, database_name, database_user, database_password, _ = configure.values()
        return f"postgresql://{database_user}:{database_password}@{database_url}:{database_port}/{database_name}"

    @classmethod
    def connection(cls):
        engine = create_engine(
            cls.construct_db_url(),
            echo=True,
            pool_size=10,
            max_overflow=20
        )
        return engine