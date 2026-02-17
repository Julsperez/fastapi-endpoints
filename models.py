from pydantic import BaseModel, EmailStr #to validate recieved data
from sqlmodel import SQLModel, Field, Relationship

# Base models
class CustomerBase(SQLModel):
	# customer_id: int #should be created in the BE
	name: str = Field(default=None)
	description: str | None = Field(default=None)
	email: EmailStr = Field(default=None)
	age: int = Field(default=None)

class Customer(CustomerBase, table=True):
	id: int | None = Field(default=None, primary_key=True)
	transactions: list["Transaction"] = Relationship(back_populates="customer")

class CustomerCreate(CustomerBase):
	pass

class CustomerUpdate(CustomerBase):
	pass

class TransactionBase(SQLModel):
	amount: int
	description: str

class Transaction(TransactionBase, table=True):
	id: int | None = Field(default=None, primary_key=True)
	customer_id: int = Field(foreign_key="customer.id")
	customer: Customer = Relationship(back_populates="transactions")

class TransactionCreate(TransactionBase):
	customer_id: int = Field(foreign_key="customer.id")

class Invoice(BaseModel):
	invoice_id: int
	customer: Customer
	transactions: list[Transaction]
	total: int

	def total_amount(self) -> int:
			return sum(transaction.amount for transaction in self.transactions)