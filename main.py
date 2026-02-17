# import zoneinfo
# from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from models import Customer, CustomerCreate, CustomerUpdate
from db_config import SessionDependency, create_all_tables
from sqlmodel import select

app = FastAPI(lifespan=create_all_tables)

@app.post('/customers/', response_model=Customer)
async def create(
	customer_data: CustomerCreate, 
	session: SessionDependency
):
	customer: Customer = Customer.model_validate(customer_data.model_dump())
	session.add(customer)
	session.commit()
	session.refresh(customer)

	return customer

@app.get('/customers/', response_model=list[Customer])
async def read_all(session: SessionDependency):
	return session.exec(select(Customer)).all()

@app.get('/customers/{customer_id}', response_model=Customer)
async def read_by_id(customer_id: int, session: SessionDependency):
	customer: Customer = session.get(Customer, customer_id)
	if not customer:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail="Customer does not exist"
		)
	return customer
	# customer = session.exec(select(Customer).where(Customer.customer_id == customer_id)).first()
	# return customer if customer else {"error": "Customer not found"}

@app.patch(
	'/customers/{customer_id}', 
	response_model=Customer,
	status_code=status.HTTP_201_CREATED)
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

@app.delete('/customers/{customer_id}')
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

# @app.post('/transactions/')
# async def create_transaction(transaction_data: Transaction):
#     return transaction_data

# @app.post('/invoices/')
# async def create_invoice(invoice_data: Invoice):
#     return invoice_data


# @app.get('/')
# async def root():
#     return {"message": "Hello Juls!"}

# @app.get('/date')
# async def get_date():
#     return {"date": datetime.now().isoformat()}

# country_timezones = {
#     "US": "America/New_York",
#     "JP": "Asia/Tokyo",
#     "GB": "Europe/London",
#     "MX": "America/Mexico_City",
#     "CO": "America/Bogota"
# }

# @app.get('/time/{iso_code}')
# async def get_time(iso_code: str):
#     iso_code = iso_code.upper()
#     time_zone_str = country_timezones.get(iso_code)
#     time_zone = zoneinfo.ZoneInfo(time_zone_str) if time_zone_str else zoneinfo.ZoneInfo("UTC")
#     return {"time": datetime.now(time_zone).strftime("%H:%M:%S")}

