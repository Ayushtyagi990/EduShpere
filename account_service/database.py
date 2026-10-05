from sqlmodel import SQLModel, Session, create_engine


# ============================================================
# DATABASE URL
# ============================================================

DATABASE_URL = (
    "mysql+pymysql://root:password@localhost:3306/account-service"
)


# ============================================================
# DATABASE ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    echo=True,
)


# ============================================================
# CREATE TABLES
# ============================================================

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# ============================================================
# DATABASE SESSION
# ============================================================

def get_session():
    with Session(engine) as session:
        yield session