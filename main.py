import zoneinfo
from fastapi import FastAPI
from datetime import datetime
from models import Customer, Transaction, Invoice, CustomerCreate



app = FastAPI()

current_id: int = 24071996
db_customers: list[Customer] = []

@app.post('/customers/', response_model=Customer)
async def create_customer(customer_data: CustomerCreate):
    customer: Customer = Customer.model_validate(customer_data.model_dump())
    customer.customer_id = len(db_customers)
    db_customers.append(customer)
    return customer

@app.get('/customers/', response_model=list[Customer])
async def get_customers_list():
    return db_customers

@app.get('/customers/{customer_id}', response_model=Customer)
async def get_customer(customer_id: int):
    for customer in db_customers:
        if customer.customer_id == customer_id:
            return customer
    return {"error": "Customer not found"}



@app.post('/transactions/')
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post('/invoices/')
async def create_invoice(invoice_data: Invoice):
    return invoice_data


@app.get('/')
async def root():
    return {"message": "Hello Juls!"}

@app.get('/date')
async def get_date():
    return {"date": datetime.now().isoformat()}

country_timezones = {
    "US": "America/New_York",
    "JP": "Asia/Tokyo",
    "GB": "Europe/London",
    "MX": "America/Mexico_City",
    "CO": "America/Bogota"
}

@app.get('/time/{iso_code}')
async def get_time(iso_code: str):
    iso_code = iso_code.upper()
    time_zone_str = country_timezones.get(iso_code)
    time_zone = zoneinfo.ZoneInfo(time_zone_str) if time_zone_str else zoneinfo.ZoneInfo("UTC")
    return {"time": datetime.now(time_zone).strftime("%H:%M:%S")}

