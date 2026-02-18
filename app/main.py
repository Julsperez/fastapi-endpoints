# import zoneinfo
# from datetime import datetime
from fastapi import FastAPI
from db_config import create_all_tables
from .routers import customers, invoices, transactions, plans

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(invoices.router)
app.include_router(transactions.router)
app.include_router(plans.router)

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

