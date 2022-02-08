import os, random
from pprint import pprint  # pylint: disable=unused-import
import enum
from uuid import UUID, uuid4
from typing import List, Dict
import numpy as np

from sqlalchemy import Column, String, DateTime, text, func, Boolean, Enum, orm, Integer, Text
from sqlalchemy.exc import NoResultFound 
from fastapi import status, HTTPException
from libs import db, models, clasifier
from settings import settings

def create_database():
	return db.Base.metadata.create_all(bind=db.engine)

class FilesDBServices():
	def __init__(self, db_):
		self.db: orm.Session = db_

	def create(self, kwargs):
		db_files = models.FilesDB(**kwargs)
		self.db.add(db_files)

	def read_all(self):
		return self.db.query(models.FilesDB).all()

	def read_klasifikasi(self):
		return self.db.query(models.FilesDB).filter(models.FilesDB.klasifikasi=='notyet').all()

	def read_clasified(self):
		return self.db.query(models.FilesDB).filter(models.FilesDB.klasifikasi!='notyet', models.FilesDB.status=='notyet').all()

	def save(self, file_id: int, true_class: str):
		image_db = self.read_by_id(file_id)
		image_db.true_class = true_class
		if image_db.klasifikasi == true_class:
			image_db.status = 'Benar'
		else:
			image_db.status = 'Salah'

			


	def read_history(self):
		return self.db.query(models.FilesDB).filter(models.FilesDB.status!='notyet').all()

	def read_by_id(self, file_id: int):
		return self.db.query(models.FilesDB).filter(models.FilesDB.id == file_id).one()

	def delete_by_id(self, file_id: int):
		db_files = self.read_by_id(file_id)
		try:
			os.remove(F'static/data_testing/{db_files.name_file}')
		except:
			pass
		self.db.query(models.FilesDB).filter(models.FilesDB.id == file_id).delete()
		self.db.commit()

	def klasifikasi(self, file_id: int):
		labels = ['baju', 'balon', 'buku', 'dasi', 'jam', 'kaca', 'kuku', 'lampu', 'meja', 'paku', 'papan', 'pohon', 'spidol', 'tali', 'tas']
		db_files = self.read_by_id(file_id)
		db_files.klasifikasi = clasifier.clasifier.predict(F"static/data_testing/{db_files.name_file}")
		# db_files.klasifikasi = random.choice(labels)
		self.db.commit()
		return db_files

	def akurasi(self,):
		total_data = self.db.query(models.FilesDB).filter(models.FilesDB.status != 'notyet').count()
		datas = self.db.query(models.FilesDB).filter(models.FilesDB.status != 'notyet').all()
		total_data_benar = self.db.query(models.FilesDB).filter(models.FilesDB.status == 'Benar').count()
		files = []
		for data in datas:
			files.append((data.name_file, data.true_class))
		result = clasifier.clasifier.predict_all_history(files)
		try:
			akurasi = float(total_data_benar)*100/float(total_data)
		except:
			akurasi = 0
		return {'hasil_akurasi': result.data , 'akurasi': result.accuracy, 'data_benar':total_data_benar, 'total_data': total_data, 'data_salah':total_data - total_data_benar}



# class AkurasiDBServices():
# 	def _init(self, db):
# 		self.db: orm.Session = db_

# 	def create(self, kwargs):
# 		db_akurasi = models.AkurasiDB(**kwargs)
# 		self.db.add(db_akurasi)



# 	def read_by_id(self, file_id: int):
# 		return self.db.query(models.AkurasiDB).filter(models.AkurasiDB.id == file_id).one()


# 	def read_all(self):
# 		return self.db.query(models.AkurasiDB).all()

# 	def delete_by_id(self, file_id: int):
# 		db_files = self.read_by_id(file_id)
# 		try:
# 			os.remove(F'static/data_testing/{db_files.name_file}')
# 		except:
# 			pass
# 		self.db.query(models.AkurasiDB).filter(models.AkurasiDB.id == file_id).delete()
# 		self.db.commit()

# 	def klasifikasi(self, file_id: int):
# 		labels = ['baju', 'balon', 'buku', 'dasi', 'jam', 'kaca', 'kuku', 'lampu', 'meja', 'paku', 'papan', 'pohon', 'spidol', 'tali', 'tas']
# 		db_files = self.read_by_id(file_id)
# 		db_files.klasifikasi = clasifier.clasifier.predict(F"static/data_testing/{db_files.name_file}")
# 		# db_files.klasifikasi = random.choice(labels)
# 		if db_files.klasifikasi == db_files.name:
# 			db_files.status = 'true'
# 		else:
# 			db_files.status = 'false'

# 		self.db.commit()
# 		return db_files

# 	def akurasi(self,):
# 		total_data = self.db.query(models.AkurasiDB).filter(models.AkurasiDB.klasifikasi != 'notyet').count()
# 		total_data_benar = self.db.query(models.AkurasiDB).filter(models.AkurasiDB.status == 'True').count()
# 		try:
# 			akurasi = float(total_data_benar)*100/float(total_data)
# 		except:
# 			akurasi = 0
# 		return {'akurasi': akurasi, 'data_benar':total_data_benar, 'total_data': total_data}





# class UserDBService():

#     def _init(self, db):
#         self.db: orm.Session = db_

#     def create(self, **kwargs):
#         db_user = UserDB(**kwargs)
#         self.db.add(db_user)

#     def total(self) -> int:
#         return self.db.query(UserDB).count()

#     def read_all(self) -> List[UserDB]:
#         return self.db.query(UserDB).all()

#     def read_slice(self, start: int, stop: int) -> List[UserDB]:
#         return self.db.query(UserDB).slice(start, stop)

#     def read_slice_by_page(self, page: int, limit: int) -> List[UserDB]:
#         kwargs = {
#             'start': limit * (page-1),
#             'stop': (limit * page)
#         }
#         return self.read_slice(**kwargs)

#     def read_by_id(self, user_id: UUID) -> UserDB:
#         return self.db.query(UserDB).filter(UserDB.id == user_id).one()

#     def read_by_phone(self, user_phone: str) -> UserDB:
#         return self.db.query(UserDB).filter(UserDB.phone == user_phone).one()

#     def update(self, user_id: int, args):
#         db_user = self.read_by_id(user_id=user_id)

#         if args.real_name is not None:
#             db_user.real_name = args.real_name
#         if args.description is not None:
#             db_user.description = args.description
#         # self.db.commit()
#         # self.db.refresh(db_user)

#         return db_user

#     def delete(self, user_id: UUID):
#         db_user = self.read_by_id(user_id=user_id)

#         self.db.query(UserDB).filter(UserDB.id == db_user.id).delete()

#     def verify(self, user_id: UUID):
#         db_user = self.read_by_id(user_id=user_id)
#         db_user.verified = True

#     def unverify(self, user_id: UUID):
#         db_user = self.read_by_id(user_id=user_id)
#         db_user.verified = False