import sqlalchemy

URL = "sqlite:///./oil.db"

engine = sqlalchemy.create_engine(URL,connect_args={"check_same_thread":False})
SessionLocal = sqlalchemy.orm.sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = sqlalchemy.orm.declarative_base()