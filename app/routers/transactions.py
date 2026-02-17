from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from models import Customer, Transaction, TransactionCreate
from db_config import SessionDependency

router = APIRouter()

@router.post('/transactions', status_code=status.HTTP_201_CREATED, tags=['Transactions'])
async def create(
	transaction_data: TransactionCreate,
	session: SessionDependency
):
	transaction_data_dict = transaction_data.model_dump()
	customer_id = transaction_data_dict.get('customer_id')
	customer = session.get(Customer, customer_id)
	if not customer:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail="Customer does not exist"
		)

	transaction_db = Transaction.model_validate(transaction_data_dict)
	session.add(transaction_db)
	session.commit()
	session.refresh(transaction_db)
	
	return transaction_db

@router.get('/transactions', tags=['Transactions'])
async def get_all(
	session: SessionDependency
):
	return session.exec(select(Transaction)).all()
    