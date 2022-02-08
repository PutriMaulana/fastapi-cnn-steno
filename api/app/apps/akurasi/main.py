from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from settings import templates
from uuid import uuid4
from libs import services, db
# from typing import Int
app = FastAPI()




@app.get("/", response_class=HTMLResponse)
async def akurasi(request: Request):
	with db.session() as db_:
		file_services = services.AkurasiDBServices(db_)
		akurasi = file_services.akurasi()
		db_files = file_services.read_all()
		contexts = {
			'request': request,
			'title' : 'akurasi-page',
			'message': '',
			'menu_home': '',
			'menu_akurasi': 'active',
			'menu_history': '',
			'akurasi': akurasi, 
			'files' : db_files
		}
		return templates.TemplateResponse("akurasi/akurasi.html", contexts)

@app.get("/tambah_data", response_class=HTMLResponse)
async def tambah_data(request: Request):
	classes = ['alis','baju', 'balon', 'botol', 'buku', 'dasi', 'jam', 'kaca', 'kuku', 'lampu', 'mata', 'meja', 'paku', 'papan', 'pohon', 'rok', 'spidol', 'tali', 'tangan', 'tas']
	contexts = {
		"request": request,
		'title' : 'Tambah-Data-page',
		'classes': classes,

		'menu_home': '',
		'menu_akurasi': 'active',
		'menu_history': '',
	}
	return templates.TemplateResponse("akurasi/tambah_data.html", contexts)


@app.post("/tambah_data", response_class=HTMLResponse)
async def tambah_data(request: Request):
	form = await request.form()
	file_name = F"{uuid4()}_{form['image'].filename}".replace(" ", "_")
	contents = await form["image"].read()

	with open(F"static/data_testing/{file_name}", "wb+") as file_object:
		file_object.write(contents)

	kwargs = {
		"name" : form['akurasi'],
		"name_file" : file_name,
		# "akurasi": "dasi"
	}
	
	with db.session() as db_:
		file_services = services.AkurasiDBServices(db_)
		file_services.create(kwargs)
		db_.commit()
		db_files = file_services.read_all()
		akurasi = file_services.akurasi()


		contexts = {
			'request': request,
			'title' : 'Tambah-Data-page',
			'message': F'Sukses upload file {form["image"].filename}',
			'menu_home': '',
			'menu_akurasi': 'active',
			'menu_history': '',
			'akurasi': akurasi, 
			
			'files' : db_files
		}
		return templates.TemplateResponse("akurasi/akurasi.html", contexts)

@app.get("/delete/{file_id}", response_class=RedirectResponse)
async def del_akurasi(request: Request, file_id : int):
	with db.session() as db_:
		file_services = services.AkurasiDBServices(db_)
		file_services.delete_by_id(file_id)
		
		
		return '/akurasi'

@app.get("/run/{file_id}", response_class=RedirectResponse)
async def run_klasifikasi(request: Request, file_id : int):
	with db.session() as db_:
		file_services = services.AkurasiDBServices(db_)
		db_file = file_services.klasifikasi(file_id)
		
		contexts = {
			"request": request,
			'title' : 'History-page',
			'file' : db_file,
			'menu_home': '',
			'menu_akurasi': 'active',
			'menu_history': '',
		}
		return templates.TemplateResponse("akurasi/result.html", contexts)