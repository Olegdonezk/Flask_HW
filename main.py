from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, ValidationError
import json
import re


class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)


class User(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё ]+", value):
            raise ValueError("Имя должно содержать только буквы и пробелы")
        return value

    @model_validator(mode="after")
    def check_employment_age(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError(
                "Работающий пользователь должен быть от 18 до 65 лет"
            )
        return self


def process_user_registration(json_str: str) -> str:
    try:
        data = json.loads(json_str)
        user = User.model_validate(data)

        return json.dumps({
            "status": "success",
            "data": user.model_dump()
        }, ensure_ascii=False, indent=4)

    except ValidationError as e:
        # ВАЖНО: используем include_context=False чтобы не было ValueError внутри
        return json.dumps({
            "status": "validation_error",
            "errors": e.errors(include_context=False)
        }, ensure_ascii=False, indent=4)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False, indent=4)


json_success = """{
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "Main Street",
        "house_number": 10
    }
}"""

json_fail_age = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "Main Street",
        "house_number": 10
    }
}"""

json_fail_email = """{
    "name": "J1",
    "age": 25,
    "email": "not-email",
    "is_employed": false,
    "address": {
        "city": "B",
        "street": "St",
        "house_number": 5
    }
}"""


print("SUCCESS:")
print(process_user_registration(json_success))

print("\nFAIL AGE:")
print(process_user_registration(json_fail_age))

print("\nFAIL EMAIL:")
print(process_user_registration(json_fail_email))
