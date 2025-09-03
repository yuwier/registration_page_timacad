from fastapi import APIRouter, Request, Form, HTTPException, FastAPI
from model.user import User
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import init
import urllib3
from fastapi.staticfiles import StaticFiles
from web.auth import router as auth_router
from web.admin_page import router as admin_router

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()
app.include_router(auth_router)
app.include_router(admin_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def redirect():
    return RedirectResponse("/auth/login", status_code=303)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
