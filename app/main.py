from fastapi import FastAPI, APIRouter

from app.config import run_migrations
from app.api.flights_api import router as router_flights
from app.api.planes_api import router as router_plane
from app.api.tickets_api import router as router_tickets
from app.api.passengers_api import router as router_passengers
from app.api.airports_api import router as router_airports
from app.api.users_api import router as router_users
from app.api.auth_api import router as router_security

from app.repositories.role_repository import RoleRepository
from starlette.concurrency import run_in_threadpool

def register_routes(app: FastAPI) -> None:
    root_router = APIRouter()
    @root_router.get("/")
    def home_page():
        return {
            "message": "Добро пожаловать!"
        }

    app.include_router(root_router, tags=["Приветствие"])
    app.include_router(router_flights)
    app.include_router(router_plane)
    app.include_router(router_tickets)
    app.include_router(router_passengers)
    app.include_router(router_airports)
    app.include_router(router_users)
    app.include_router(router_security)



def create_app() -> FastAPI:
    app = FastAPI(
        title="Информационная система авиакомпании",
        description="API для управления рейсами, пользователями и билетами.",
        version="1.0.0"
    )
    register_routes(app)

    return app

app = create_app()

@app.on_event("startup")
async def startup_event():
    await run_in_threadpool(run_migrations)
    await RoleRepository.seed_roles()







