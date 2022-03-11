from .database import SessionLocal


def parse_sqlalchemy_query_output(output):
    return [row.__dict__ for row in output]


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
