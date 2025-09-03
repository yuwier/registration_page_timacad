from pydantic import BaseModel, field_validator
import re

"""
Хотела использовать модель пользователя, превращая словарь получаемый из данных от FreeIPA. Но ничего толкового не получилось, и это только усложняло все. Отсюда используется gen_uid в других модулях
"""

TRANSLIT_MAP = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "c",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}
TRANSLIT = str.maketrans(TRANSLIT_MAP)


def translit(text: str) -> str:
    """Кириллица → латиница"""
    return text.lower().translate(TRANSLIT)


def gen_uid(first: str,  middle: str, last: str) -> str:
    """f + m + last (латиницей): Сергей Михайлович Лапшин → smlapshin"""
    uid_raw = f"{translit(first)[0]}{translit(middle)[0]}{translit(last)}"
    uid_clean = re.sub(r"[^a-zA-Z0-9_.\-$]", "", uid_raw)
    return uid_clean


class User(BaseModel):
    uid: str = ""
    first_name: str
    last_name: str
    middle_name: str
    cn: str = ""
    email: str
    group: str
    telephonenumber: str

    @field_validator("cn", mode="after")
    @classmethod
    def generate_cn(clas, value, info):
        first_name = info.data.get("first_name", "")
        last_name = info.data.get("last_name", "")
        middle_name = info.data.get("middle_name", "")
        return f"{last_name} {first_name} {middle_name}"

    @field_validator("uid", mode="after")
    @classmethod
    def generate_uid(clas, value, info):
        first = info.data.get("first_name", "")
        middle = info.data.get("middle_name", "")
        last = info.data.get("last_name", "")
        return gen_uid(first, middle, last)
