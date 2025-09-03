from typing import Any, Dict, List
import requests
from typing import Any, Dict, List
import requests
import os

IPA_HOST = "ipa.timacad.ru"  # ваш FQDN FreeIPA‑сервера
IPA_URL = f"https://{IPA_HOST}/ipa"
LOGIN_URL = f"{IPA_URL}/session/login_password"
JSON_URL = f"{IPA_URL}/session/json"

ADMIN_USER = "admin"  # админский пользователь
ADMIN_PASS = os.getenv("IPA_ADMIN_PASS")  # пароль можно задать через env


admin_session = requests.Session()
admin_session.verify = False
admin_session.headers.update({"Referer": IPA_URL})


def ipa_admin_login() -> None:
    """ Логинит от админа, используются переменные окружения """
    r = admin_session.post(
        LOGIN_URL,
        data={"user": ADMIN_USER, "password": ADMIN_PASS},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    if r.status_code != 200 or "ipa_session" not in admin_session.cookies:
        raise RuntimeError("Ошибка логина админа в FreeIPA")


def ipa_call(method: str, params: List[Any] | None = None, **options) -> Dict[str, Any]:
    """ Позволяет вызвать методы FreeIPA """
    payload = {"method": method, "params": [params or [], options], "id": 0}
    r = admin_session.post(
        JSON_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=10
    )
    r.raise_for_status()
    data = r.json()
    if data.get("error"):
        raise RuntimeError(data["error"]["message"])
    return data["result"]


def get_ipauser(uid: str) -> dict:
    """ Логинит от админа, получает данные пользователя uid """
    ipa_admin_login()
    user = ipa_call("user_show", [uid])
    return user
