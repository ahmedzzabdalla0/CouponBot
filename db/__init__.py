from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# إنشاء محرك قاعدة البيانات
engine = create_engine('sqlite:///db/storeDB.db')

# إنشاء جلسة
Session = sessionmaker(bind=engine)


def get_db_session():
    return Session()
