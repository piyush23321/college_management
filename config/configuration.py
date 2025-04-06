from fastapi import APIRouter

from config.base_settings import settings

router = APIRouter()

@router.get("/config")
def get_config():
    return {
        "database_url": settings.host,
        "database_port": settings.port,
        "database_name": settings.dbname,
        "database_user": settings.user,
        "database_password": settings.password,
        "secret_key": settings.secret_key
    }