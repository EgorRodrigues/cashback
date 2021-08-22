from dataclasses import InitVar, dataclass, field

from passlib.context import CryptContext


@dataclass
class Name:
    first: str
    last: str

    @property
    def full(self) -> str:
        return f"{self.first} {self.last}"


@dataclass
class Reseller:
    first_name: InitVar[str]
    last_name: InitVar[str]
    cpf: str
    email: str
    plain_password: InitVar[str]
    name: Name = field(init=False)
    _password: str = field(init=False)

    def __post_init__(
        self,
        first_name: str,
        last_name: str,
        plain_password: str,
    ) -> None:
        self.set_name(first_name, last_name)
        self.password = plain_password

    @property
    def full_name(self) -> str:
        return self.name.full

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        context = self._get_pwd_context()
        self._password = context.using().hash(password)

    def set_name(self, first, last) -> None:
        self.name = Name(first, last)

    def verify_password(self, plain_password):
        context = self._get_pwd_context()
        return context.verify(plain_password, self.password)

    @staticmethod
    def _get_pwd_context() -> CryptContext:
        return CryptContext(schemes=["bcrypt"], deprecated="auto")
