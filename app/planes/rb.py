from datetime import date, time
class RBPlane:
    def __init__(self,
                 plane_id: int | None = None,
                 model:str | None = None,
                 capacity: int | None = None):
        self.id = plane_id
        self.model = model
        self.capacity = capacity


    def to_dict(self) -> dict:
        data = {
            'id': self.id,
            'model': self.model,
            'capacity': self.capacity
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data