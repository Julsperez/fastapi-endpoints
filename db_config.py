from typing import Annotated
from sqlmodel import Session, create_engine, SQLModel
from fastapi import Depends, FastAPI

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url)

def create_all_tables(app: FastAPI):
	SQLModel.metadata.create_all(engine)
	yield

def get_session():
	with Session(engine) as session:
		yield session

SessionDependency = Annotated[Session, Depends(get_session)]