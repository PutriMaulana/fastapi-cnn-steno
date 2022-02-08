from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from settings import templates
from libs import services, db
app = FastAPI()




@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    with db.session() as db_:
        file_services = services.FilesDBServices(db_)
        db_files = file_services.read_history()
        
        contexts = {
            "request": request,
            'title' : 'History-page',
            'files' : db_files,
            'menu_home': '',
            'menu_test': '',
            'menu_history': 'active',
        }
        return templates.TemplateResponse("history/history.html", contexts)

@app.get("/akurasi", response_class=RedirectResponse)
async def klasifikasi(request: Request):
    with db.session() as db_:
        file_services = services.FilesDBServices(db_)
        akurasi = file_services.akurasi()
        contexts = {
            "request": request,
            'title' : 'History-page',
            'akurasi' : akurasi,
            'menu_home': '',
            'menu_test': '',
            'menu_history': 'active',
        }
        return templates.TemplateResponse("history/akurasi.html", contexts)
        
        return '/history'



    

@app.get("/delete/{file_id}", response_class=RedirectResponse)
async def klasifikasi(request: Request, file_id : int):
    with db.session() as db_:
        file_services = services.FilesDBServices(db_)
        file_services.delete_by_id(file_id)
        
        
        return '/history'



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
            'menu_test': '',
            'menu_history': 'active',
        }
        return templates.TemplateResponse("history/re-klasifikasi.html", contexts)
        # return '/klasifikasi'
