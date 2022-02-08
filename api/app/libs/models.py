from uuid import UUID, uuid4
from typing import List, Dict
from libs import db
from sqlalchemy import Column, String, DateTime, text, func, Boolean, Enum, orm, Integer, Text

class FilesDB(db.Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    name_file = Column(String(255))
    klasifikasi = Column(String(255), server_default="notyet")
    true_class = Column(String(255), server_default="notyet")
    status = Column(String(255), server_default="notyet")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# class AkurasiDB(db.Base):
#     __tablename__ = 'akurasi'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255))
#     name_file = Column(String(255))
#     klasifikasi = Column(String(255), server_default="notyet")
#     status = Column(String(255), server_default="notyet")
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())