from pydantic import BaseModel, EmailStr #to validate recieved data
from sqlmodel import SQLModel, Field

class CustomerBase(SQLModel):
	# customer_id: int #should be created in the BE
	name: str = Field(default=None)
	description: str | None = Field(default=None)
	email: EmailStr = Field(default=None)
	age: int = Field(default=None) 

class Customer(CustomerBase, table=True):
	customer_id: int | None = Field(default=None, primary_key=True)

class CustomerCreate(CustomerBase):
	pass

class CustomerUpdate(CustomerBase):
	pass

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