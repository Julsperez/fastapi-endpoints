from pydantic import BaseModel, EmailStr #to validate recieved data

class CustomerBase(BaseModel):
    # customer_id: int #should be created in the BE
    name: str
    description: str | None
    email: EmailStr
    age: int 

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    customer_id: int | None = 24071996


class Transaction(BaseModel):
    transaction_id: int
    amount: int
    descritpion: str

class Invoice(BaseModel):
    invoice_id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    def total_amount(self) -> int:
        return sum(transaction.amount for transaction in self.transactions)