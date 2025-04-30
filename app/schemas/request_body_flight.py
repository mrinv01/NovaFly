from datetime import datetime
class RequestBodyFlight:
    def __init__(self,
                 plane_id: int | None = None,
                 departure_from: int | None = None,
                 arrival_to: int | None = None,
                 departure: datetime | None = None,
                 arrival: datetime | None = None,
                 status: str | None = None):
        self.plane_id = plane_id
        self.departure_from = departure_from
        self.arrival_to = arrival_to
        self.departure = departure
        self.arrival = arrival
        self.status = status

    def to_dict(self) -> dict:
        data = {
            'plane_id': self.plane_id,
            'departure_from': self.departure_from,
            'arrival_to': self.arrival_to,
            'departure': self.departure,
            'arrival': self.arrival,
            'status': self.status
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data