from fastapi import APIRouter, Request, Form, HTTPException, Depends
import service.admin_page as service
from model.user import User
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.templating import Jinja2Templates
from ldap3 import Server, Connection, ALL
import os

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/admin")
os.environ["IPA_ADMIN_PASS"] = "ifconfig1"

"""
Пока что админка не сделана. Здесь хранятся мои наброски, что-то актуально, что-то неактуально
"""


# def get_current_user(request: Request) -> User:
#     uid = request.cookies.get("uid")
#     if not uid:
#         raise HTTPException(status_code=401, detail="Вы не авторизованы")
#     user_data = service.get_user_from_freeipa(uid)
#     return user_data


def full_name(cn):
    full_name = str(cn).split()
    while len(full_name) < 3:
        full_name.append("")
    return full_name
# у нас есть список, от 0 до 3 элементов. Нужно их запихивать в переменные

@router.get("/", response_class=HTMLResponse)
async def admin_panel(request: Request):
    # if user.group != "admins":
    #     raise HTTPException(status_code=403, detail="Доступ запрещён")
    try:


        LDAP_SERVER = "10.101.20.11"
        BIND_DN = "uid=admin,cn=users,cn=accounts,dc=ai,dc=timacad,dc=ru"
        BIND_PASSWORD = os.getenv("IPA_ADMIN_PASS")

        server = Server(LDAP_SERVER, get_info=None) # в приложении поставить get_info=None
        conn = Connection(server, user=BIND_DN, password=BIND_PASSWORD)
        # if not conn.bind():
            # print("Ошибка привязки:", conn.result) # тут обработать правильно
            # exit() # это sys.exit(), мне такое не нужно... лучше raise ConnectionError(f"Ошибка подключения: {conn.result}")

        search_base = "cn=users,cn=accounts,dc=ai,dc=timacad,dc=ru"
        search_filter = "(objectClass=person)"

        conn.search(search_base, search_filter, attributes=["uid", "cn", "telephonenumber", "mail", "memberOf", "nsAccountLock", "createTimestamp"], paged_size=50)
        # for entry in conn.entries:
        #     print(entry.uid, entry.cn, entry.mail) # тут тоже обработать правильно
        users = conn.entries
        for user in users:
            print(full_name(user.cn))
            last_name, first_name, middle_name = full_name(user.cn)
            user.append()

        return templates.TemplateResponse("admin_page.html", {"request": request, "users": users, "last_name": last_name, "first_name": first_name, "middle_name": middle_name})
    except Exception as exc:
        detail = str(exc)
        return templates.TemplateResponse("error.html", {"request": request, "detail": detail})
