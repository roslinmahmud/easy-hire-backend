from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Format: "postgresql://username:password@localhost/easy-hire"
SQLALCHEMY_DATABASE_URL = f'postgresql://anonymous.jak:ZGKQbc0LqUo8@ep-broad-field-924328.us-east-2.aws.neon.tech/easy-hire'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()