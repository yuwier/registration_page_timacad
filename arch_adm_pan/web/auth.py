from fastapi import APIRouter, Request, Form, HTTPException, Depends
import service.auth as service
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/auth")


# Страница с формой для регистрации
@router.get("/register", response_class=HTMLResponse)
async def registration_form(request: Request):
    return templates.TemplateResponse("registration_page.html", {"request": request})


# Получает данные, введенные пользователем для регистрации, регистрирует во FreeIPA
@router.post("/register/submit", response_class=HTMLResponse)
async def register_user(request: Request, first_name: str = Form(...), last_name: str = Form(...), middle_name: str = Form(...), groups: list[str] = Form(...), telephonenumber: str = Form(...), email: str = Form(...), userpassword: str = Form(...)):
    try:
        uid = service.gen_uid(first_name, middle_name, last_name)
        service.register_user(first_name=first_name, last_name=last_name, middle_name=last_name,
                              group=groups, telephonenumber=telephonenumber, email=email, userpassword=userpassword)
    except Exception as exc:
        detail = str(exc)
        return templates.TemplateResponse("error.html", {"request": request, "detail": detail})

    return templates.TemplateResponse("verification_page.html", {"request": request, "uid": uid})


# Страница с формой для входа
@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login_page.html", {"request": request})


# Получает данные для входа, нужно сделать так, чтобы логинил через ldap, сохранял его данные в сессию
@router.post("/login/submit", response_class=HTMLResponse)
async def login_form(response: Response, request: Request, login: str = Form(...), password: str = Form()):
    try:
        return RedirectResponse("/admin_page/", status_code=303)
    except Exception as exc:
        detail = str(exc)
        return templates.TemplateResponse("error.html", {"request": request, "detail": detail})
