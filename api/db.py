import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
# from sqlalchemy import Boolean, Column, Float, String, Integer, MetaData, Table

config = configparser.SafeConfigParser()
config.read("envfile.ini")

oracle_username = config["DEFAULT"]["ORACLE_USERNAME"]
oracle_password = config["DEFAULT"]["ORACLE_PASSWORD"]
ORACLEDB = config["DEFAULT"]["ORACLEDB"]
oracle_host = config["DEFAULT"]["ORACLE_HOST"]
oracle_port = config["DEFAULT"]["ORACLE_PORT"]
dsnStr = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={})(PORT={}))(CONNECT_DATA=(SERVICE_NAME={})))".format(
    oracle_host, oracle_port, ORACLEDB
)


# SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///data.db"
DATABASE_URL = "oracle://* + oracle_username + ':' + oracle_password + '@" + dsnStr
engine1 = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
# engine2 = create_engine(DATABASE_URL)
# table1meta = MetaData(engine2)
# table1 = Table("VP_META PAGES", table1meta, autoload=True)
# table2 = Table("DS_EMPLOYEE", table1meta, autoload=True, schema="HIR_OWNER")
Session1 = sessionmaker(autocommit=False, autoflush=False, bind=engine1)
# Session2 = sessionmaker(bind=engine2)
# Basel = declarative_base()
# Base2 = declarative_base()
Base = declarative_base()
# sesh = Session2()

# results = sesh.query(table2).filter(table2.c. salaryref
# print(table1)
# print(results.all())


# Sqlalchemy Setup
# SQLALCHEMY_DATABASE_URL = "sqlite:///data.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, ech
# SessionLocal = Sessionmaker(autocommit-False, autoflush=False, bind=engine)
# Base = declarative_base()
