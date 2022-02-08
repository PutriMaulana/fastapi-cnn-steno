from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from settings import templates
from uuid import uuid4
from libs import services, db
# from typing import Int
app = FastAPI()




@app.get("/", response_class=HTMLResponse)
async def klasifikasi(request: Request):
	with db.session() as db_:
		classes = ['alis','baju', 'balon', 'botol', 'buku', 'dasi', 'jam', 'kaca', 'kuku', 'lampu', 'mata', 'meja', 'paku', 'papan', 'pohon', 'rok', 'spidol', 'tali', 'tangan', 'tas']

		file_services = services.FilesDBServices(db_)
		db_files = file_services.read_klasifikasi()
		db_files_clasified = file_services.read_clasified()
		contexts = {
			'request': request,
			'title' : 'Klasifikasi-page',
			'message': '',
			'menu_home': '',
			'menu_test': 'active',
			'menu_history': '',
			'classes': classes,
			'files' : db_files,
			'file_clasifieds' : db_files_clasified,
		}
		return templates.TemplateResponse("klasifikasi/klasifikasi.html", contexts)

@app.get("/tambah_data", response_class=HTMLResponse)
async def tambah_data(request: Request):
	print(request.method)
	contexts = {
		"request": request,
		'title' : 'Tambah-Data-page',

		'menu_home': '',
		'menu_test': 'active',
		'menu_history': '',
	}
	return templates.TemplateResponse("klasifikasi/tambah_data.html", contexts)


@app.post("/tambah_data", response_class=HTMLResponse)
async def tambah_data(request: Request):
	form = await request.form()
	if form["image"].filename is "":
		with db.session() as db_:
			file_services = services.FilesDBServices(db_)
			db_files = file_services.read_klasifikasi()
			db_files_clasified = file_services.read_clasified()


			contexts = {
				'request': request,
				'title' : 'Tambah-Data-page',
				'message': F'Failed',
				'menu_home': '',
				'menu_test': 'active',
				'menu_history': '',
				'file_clasifieds' : db_files_clasified,
				'files' : db_files
			}
			return templates.TemplateResponse("klasifikasi/klasifikasi.html", contexts)
	file_name = F"{uuid4()}_{form['image'].filename}".replace(" ", "_")
	contents = await form["image"].read()

	with open(F"static/data_testing/{file_name}", "wb+") as file_object:
		file_object.write(contents)

	kwargs = {
		"name" : form['image'].filename,
		"name_file" : file_name,
		# "klasifikasi": "dasi"
	}
	
	with db.session() as db_:
		file_services = services.FilesDBServices(db_)
		file_services.create(kwargs)
		db_.commit()
		db_files = file_services.read_klasifikasi()
		db_files_clasified = file_services.read_clasified()


		contexts = {
			'request': request,
			'title' : 'Tambah-Data-page',
			'message': F'Sukses upload file {form["image"].filename}',
			'menu_home': '',
			'menu_test': 'active',
			'menu_history': '',
			'file_clasifieds' : db_files_clasified,
			'files' : db_files
		}
		return templates.TemplateResponse("klasifikasi/klasifikasi.html", contexts)

@app.get("/delete/{file_id}", response_class=RedirectResponse)
async def klasifikasi(request: Request, file_id : int):
	with db.session() as db_:
		file_services = services.FilesDBServices(db_)
		file_services.delete_by_id(file_id)
		
		
		return '/klasifikasi'

@app.get("/run/{file_id}", response_class=RedirectResponse)
async def klasifikasi(request: Request, file_id : int):
	with db.session() as db_:
		file_services = services.FilesDBServices(db_)
		db_file = file_services.klasifikasi(file_id)
		
		contexts = {
			"request": request,
			'title' : 'History-page',
			'file' : db_file,
			'menu_home': '',
			'menu_test': 'active',
			'menu_history': '',
		}
		return templates.TemplateResponse("klasifikasi/result.html", contexts)

@app.get("/save/{file_id}", response_class=RedirectResponse)
async def klasifikasi(request: Request, file_id : int, true_class: str):
	with db.session() as db_:
		file_services = services.FilesDBServices(db_)
		file_services.save(file_id, true_class)
	return '/klasifikasi'