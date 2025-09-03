import data.ipa_client as data
from model.user import gen_uid


def register_user(first_name: str, last_name: str, middle_name: str, email: str, groups: list[str], telephonenumber: str, userpassword: str):
    """ Регистрирует пользователя во FreeIPA """
    uid = gen_uid(first_name, middle_name, last_name)
    cn = f"{last_name} {first_name} {middle_name}"

    data.ipa_admin_login()

    data.ipa_call(
        "user_add",
        [uid],
        givenname=first_name,
        sn=last_name,
        cn=cn,
        mail=email,
        telephonenumber=telephonenumber,
        userpassword=userpassword,
        loginshell="/bin/bash",
    )

    for group in groups:
        data.ipa_call("group_add_member", [group], user=[uid])

    data.ipa_call("user_disable", [uid])


def get_user_from_freeipa(uid: str) -> dict:
    """ Возвращает словарь данных пользователя uid """
    user = data.get_ipauser(uid)
    # user = ipauser_to_user(ipa_user)
    return user
