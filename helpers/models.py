from dataclasses import dataclass, field


@dataclass(frozen=True)
class Credentials:
    email: str
    password: str = field(repr=False)

    def registration_payload(self):
        return {'email': self.email, 'password': self.password, 'submitPassword': self.password}

    def login_payload(self):
        return {'email': self.email, 'password': self.password}


@dataclass(frozen=True)
class User:
    id: int
    email: str
    credentials: Credentials = field(repr=False)
    token: str = field(repr=False)
