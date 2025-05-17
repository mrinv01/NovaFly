from datetime import date, time
class RequestBodyFlight:
    def __init__(self,
                 plane_id: int | None = None,
                 departure_from: int | None = None,
                 arrival_to: int | None = None,
                 departure_date: date | None = None,
                 departure_time: time | None = None,
                 arrival_date: date | None = None,
                 arrival_time: time | None = None,
                 status: str | None = None):
        self.plane_id = plane_id
        self.departure_from = departure_from
        self.arrival_to = arrival_to
        self.departure_date = departure_date
        self.departure_time = departure_time
        self.arrival_date = arrival_date
        self.arrival_time = arrival_time
        self.status = status

    def to_dict(self) -> dict:
        data = {
            'plane_id': self.plane_id,
            'departure_from': self.departure_from,
            'arrival_to': self.arrival_to,
            'departure_date': self.departure_date,
            'departure_time': self.departure_time,
            'arrival_date': self.arrival_date,
            'arrival_time': self.arrival_time,
            'status': self.status
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data