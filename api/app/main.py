import time
# time.sleep(20)
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from apps.klasifikasi.main import app as app_klasifikasi
from apps.history.main import app as app_history
from apps.akurasi.main import app as app_akurasi
from fastapi.responses import HTMLResponse
from libs import services
services.create_database()
from settings import templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount('/klasifikasi', app_klasifikasi)
app.mount('/history', app_history)
# app.mount('/akurasi', app_akurasi)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
	contexts = {
		"request": request,
		'title'	: 'Home-page',

		'menu_home': 'active',
		'menu_test': '',
		'menu_history': '',
	}
	return templates.TemplateResponse("home/home.html", contexts)