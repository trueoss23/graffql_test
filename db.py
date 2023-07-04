from sqlalchemy import create_engine, Integer, String, Column, Table
from sqlalchemy import MetaData, insert
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql


Base = declarative_base()


class TaskTable(Base):
    __tablename__ = 'Tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    assignee_id = Column(Integer)


class DbTools():
    def __init__(self, user, password, host, db_name) -> None:
        self.engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{db_name}')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.task_table = TaskTable()

    def add_new_row(self, new_row):
        new_row = TaskTable(name='new', assignee_id=100)
        self.session.add(new_row)
        self.session.commit()
        return new_row.id

    def get_list_table(self, table_name):
        meta = MetaData()
        task_table = Table(table_name,
                           meta,
                           autoload_with=self.engine,
                           mysql_autoload=True)
        with self.engine.connect() as conn:
            select_query = task_table.select()
            result = conn.execute(select_query)
            rows = result.fetchall()
            return rows

    def delete_row(self, id_):
        condition = self.task_table.c.id == id_
        delete_statement = self.task_table.delete().where(condition)
        with self.engine.connect() as conn:
            conn.execute(delete_statement)

# Base.metadata.create_all(engine)
