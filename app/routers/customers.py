from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select
from models import Customer, CustomerCreate, CustomerUpdate, Plan, StatusEnum, Subscription
from db_config import SessionDependency

router = APIRouter()

@router.post('/customers', status_code=status.HTTP_201_CREATED, response_model=Customer, tags=['Customers'])
async def create(
	customer_data: CustomerCreate, 
	session: SessionDependency
):
	customer: Customer = Customer.model_validate(customer_data.model_dump())
	session.add(customer)
	session.commit()
	session.refresh(customer)

	return customer

@router.get('/customers', response_model=list[Customer], tags=['Customers'])
async def get_all(session: SessionDependency):
	return session.exec(select(Customer)).all()

@router.get('/customers/{customer_id}', response_model=Customer, tags=['Customers'])
async def get_by_id(customer_id: int, session: SessionDependency):
	customer: Customer = session.get(Customer, customer_id)
	if not customer:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail="Customer does not exist"
		)
	return customer

@router.patch('/customers/{customer_id}', response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['Customers'])
async def update(
	customer_id: int, 
	customer_data: CustomerUpdate, 
	session: SessionDependency
):
	db_customer: Customer = session.get(Customer, customer_id)
	if not db_customer:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Customer does not exist"
		)
	update_data = customer_data.model_dump(exclude_unset=True)
	db_customer.sqlmodel_update(update_data)
	session.commit()
	session.refresh(db_customer)

	return db_customer

@router.delete('/customers/{customer_id}', tags=['Customers'])
async def delete_by_id(customer_id: int, session: SessionDependency):
	customer: Customer = session.get(Customer, customer_id)
	if not customer:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail="Customer does not exist"
		)
	session.delete(customer)
	session.commit()
	return {"deleted": True}

@router.post('/customers/{customer_id}/plans/{plan_id}', tags=['Customers'])
async def subscribe_to_plan(
	customer_id: int, 
	plan_id: int, 
	session: SessionDependency,
	plan_status: StatusEnum = Query()
):
	customer_db = session.get(Customer, customer_id)
	plan_db = session.get(Plan, plan_id)
	if not customer_db or not plan_db:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail="Customer or plan does not exist"
		)
	subscription = Subscription(plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status)
	session.add(subscription)
	session.commit()
	session.refresh(subscription)
	
	return subscription
	
@router.get('/customers/{customer_id}/plans', tags=['Customers'])
async def get_all_plans(
	customer_id: int, 
	session: SessionDependency,
	plan_status: Optional[StatusEnum] = Query(None, alias="plan_status")
):
	customer_db = session.get(Customer, customer_id)
	if not customer_db:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail="Customer does not exist"
		)
	
	query = (
		select(Subscription)
		.where(Subscription.customer_id == customer_id)
		.where(Subscription.status == plan_status)
	)
	plans = session.exec(query).all()
	
	return plans
