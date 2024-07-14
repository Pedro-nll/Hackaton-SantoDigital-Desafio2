from pydantic import BaseModel

class Customer_schema(BaseModel):
    educationLevel: str
    occupation: str
    homeOwner: bool
    customerKey: int
    prefix: str
    firstName: str
    lastName: str
    birthDate: str
    maritalStatus: str
    gender: str
    emailAddress: str
    annualIncome: float
    totalChildren: int
