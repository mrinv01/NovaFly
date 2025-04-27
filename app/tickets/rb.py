class RBTicket:
    def __init__(self,
                 order_id: int | None = None,
                 ticket_id: int | None = None,
                 flight_id: int | None = None,
                 seat_number: str | None = None,
                 price: int | None = None,
                 ):
        self.order_id = order_id
        self.ticket_id = ticket_id
        self.flight_id = flight_id
        self.seat_number = seat_number
        self.price = price

        def to_dict(self) -> dict:
            data = {
                'order_id': self.order_id,
                'ticket_id': self.ticket_id,
                'flight_id': self.flight_id,
                'seat_number': self.seat_number,
                'price': self.price
            }
            filtered_data = {key: value for key, value in data.items() if value is not None}
            return filtered_data