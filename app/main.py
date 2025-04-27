from fastapi import FastAPI, APIRouter
from app.flights.router import router as router_flights
from app.planes.router import router as router_plane
from app.orders.router import router as router_orders
from app.tickets.router import router as router_tickets
from app.passengers.router import router as router_passengers

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
    app.include_router(router_orders)
    app.include_router(router_tickets)
    app.include_router(router_passengers)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Информационная система авиакомпании",
        description="API для управления рейсами, пользователями и билетами.",
        version="1.0.0"
    )
    register_routes(app)
    return app

app = create_app()







