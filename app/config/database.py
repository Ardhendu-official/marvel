from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL='mysql+mysqlconnector://root@localhost:3306/marvel'                      #localhost

SQLALCHEMY_DATABASE_URL='mysql+mysqlconnector://root:marvel@13.235.171.121:3306/marvel'                      #AWS

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20,pool_pre_ping= True,
    pool_recycle= 60 * 60, max_overflow=0)  # type: ignore

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()