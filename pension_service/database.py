from sqlmodel import create_engine, Session, SQLModel

engine=create_engine(
  "mysql+pymysql://root:@127.0.0.1:3306/pension-service",
  echo=True
)
def get_session():
  with Session(engine) as session:
    yield session



SQLModel.metadata.create_all(engine)