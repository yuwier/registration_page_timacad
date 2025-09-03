from ldap3 import Server, Connection, ALL
import os
import re

os.environ["IPA_ADMIN_PASS"] = "ifconfig1"

LDAP_SERVER = "10.101.20.11"
BIND_DN = "uid=admin,cn=users,cn=accounts,dc=ai,dc=timacad,dc=ru"
BIND_PASSWORD = os.getenv("IPA_ADMIN_PASS")

server = Server(LDAP_SERVER, get_info=ALL) # в приложении поставить get_info=None
conn = Connection(server, user=BIND_DN, password=BIND_PASSWORD)
if not conn.bind():
    print("Ошибка привязки:", conn.result) # тут обработать правильно
    exit() # это sys.exit(), мне такое не нужно... лучше raise ConnectionError(f"Ошибка подключения: {conn.result}")

search_base = "cn=users,cn=accounts,dc=ai,dc=timacad,dc=ru"
search_filter = "(objectClass=person)"

conn.search(search_base, search_filter, attributes=["uid", "cn", "mail"], paged_size=50)
# for entry in conn.entries:
#     print(entry.uid, entry.cn, entry.mail) # тут тоже обработать правильно
users = conn.entries
# print(users)

def full_name(cn):
    full_name = str(cn).split()
    while len(full_name) < 3:
        full_name.append("")
    return full_name

# у нас есть список, от 0 до 3 элементов. Нужно их запихивать в переменные
for user in users:
    print(full_name(user.cn))
    last_name, first_name, middle_name = full_name(user.cn)
    print(user.uid)
    print(last_name)
    print(first_name)
    print(middle_name)
    
    groups_dn = user.memberOf.values  # список DN групп

    # Извлекаем только cn
    groups_cn = [re.search(r"cn=([^,]+)", dn).group(1) for dn in groups_dn]
