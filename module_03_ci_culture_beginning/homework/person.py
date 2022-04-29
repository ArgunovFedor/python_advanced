from datetime import datetime


class Person:
    def __init__(self, name: str, year_of_birth: datetime, address: str = '') -> None:
        self.name = name
        self.yob = year_of_birth
        self.address = address

    def get_age(self) -> int:
        now = datetime.now()
        return now.year - self.yob.year - 1

    def get_name(self) -> str:
        return self.name

    def set_name(self, name) -> None:
        self.name = self.name

    def set_address(self, address) -> None:
        self.address == address

    def get_address(self) -> datetime:
        return self.address

    def is_homeless(self) -> bool:
        '''
        returns True if address is not set, false in other case
        '''
        return self.address is None
