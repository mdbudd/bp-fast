from sqlalchemy.orm import Session
from api.db import engine1, Session1
# from api.db import engine2, Session2, table1, table2, sesh
from models.people import DBEmployee
from models.places import DBPlace, Place

def get_db():
    db = Session1()
    try:
        yield db
    finally:
        db.close()


# def get_db2():
#     db = Session2()
#     try:
#         yield db
#     finally:
#         db.close()


def get_place(db: Session, place_id: int):
    return db.query(DBPlace).where(DBPlace.id == place_id).first()


def get_places(db: Session):
    return db.query(DBPlace).all()


# def get_meta(page_id: int):
#     results = sesh.query(table1).filter(table1.c.page_id == page_id)
#     return results.all()


# def get_employee(srn: int):
#     results = sesh.query(table2).filter(table2.c.salaryref == srn)
#     return results.all()


def get_employee_a(db: Session, srn: int):
    results = db.query(DBEmployee).where(DBEmployee.salaryref == srn)
    return results.first()


def create_place(db: Session, place: Place):
    db_place = DBPlace(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)

    return db_place


# def get_data(db: Session, srn: int):
#     # return db.query(DBEmployee) .where(DBEmployee.salaryref.first()
#     as_df = False
#     query = """
#     SELECT * FROM DS_EMPLOYEE
#     WHERE SALARYREF = {}
#     """.format(
#         srn
#     )
#     df = pd.read_sql(query, engine2)
#     df.columns = map(str.lower, df.columns)
#     if "start_date" in df.columns:
#         df["start_date"] = df["start_date"].astype("string")
#     if "end_date" in df.columns:
#         df["end_date"] = df["end_date"].astype("string")
#     result = df
#     if not as_df:
#         result = json.loads(df.to_json(orient="records"))
#     return result