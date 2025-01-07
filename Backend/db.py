import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

URL_DATABASE = 'mysql+pymysql://root:Root123!!@localhost:3306/chatbotapp'

engine = sql.create_engine(URL_DATABASE)
sessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative.declarative_base()

