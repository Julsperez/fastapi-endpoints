from pydantic import BaseModel, EmailStr #to validate recieved data
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class StatusEnum(str, Enum):
	ACTIVE = "active"
	INACTIVE = "inactive"


class Subscription(SQLModel, table=True):
	id: int | None = Field(primary_key=True)
	plan_id: int | None = Field(foreign_key="plan.id")
	customer_id: int | None = Field(foreign_key="customer.id")
	status: StatusEnum = Field(default=StatusEnum.ACTIVE)

class PlanBase(SQLModel):
	name: str = Field(default=None)
	price: int = Field(default=None)
	description: str = Field(default=None)

class Plan(PlanBase, table=True):
	id: int | None = Field(default=None, primary_key=True)
	customers: list["Customer"] = Relationship(
		back_populates="plans", 
		link_model=Subscription
	)

class PlanCreate(PlanBase):
	pass

class CustomerBase(SQLModel):
	name: str = Field(default=None)
	description: str | None = Field(default=None)
	email: EmailStr = Field(default=None)
	age: int = Field(default=None)

class Customer(CustomerBase, table=True):
	id: int | None = Field(default=None, primary_key=True)
	transactions: list["Transaction"] = Relationship(back_populates="customer")
	plans: list[Plan] = Relationship(
		back_populates="customers",
		link_model=Subscription
	)

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