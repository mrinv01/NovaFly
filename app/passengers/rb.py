from datetime import date

class RBPassenger:
    def __init__(self,
                 id: int | None = None,
                 surname: str | None = None,
                 name: str | None = None,
                 patronymic: str | None = None,
                 date_of_birth: date | None = None,
                 document_number: str | None = None):
        self.id = id
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.date_of_birth = date_of_birth
        self.document_number = document_number

    def to_dict(self) -> dict:
        data ={
            "id": self.id,
            "surname": self.surname,
            "name": self.name,
            "patronymic": self.patronymic,
            "date_of_birth": self.date_of_birth,
            "document_number": self.document_number
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data