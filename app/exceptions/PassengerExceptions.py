from fastapi import status, HTTPException


InformationNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Нет пассажиров, которые соответствуют условиям поиска"
)