from sqlmodel import SQLModel, Session, create_engine


engine=create_engine(
  "mysql+pymysql://root:@127.0.0.1:3306/payroll-service",
  echo=True
)



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session