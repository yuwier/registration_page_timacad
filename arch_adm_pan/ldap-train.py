# from ldap3 import Server, Connection, ALL

# server = Server("10.101.20.11")
# conn = Connection(server,
#                   user="uid=admin,cn=users,cn=accounts,dc=ai,dc=timacad,dc=ru", password="ifconfig1")
# conn.bind()
# print(server.info)

# search_base = "cn=users,cn=accounts,dc=ai,dc=timacad,dc=ru"
# search_filter = "(uid=rskulik)"

# msg_id = conn.search(search_base, search_filter, attributes=["nsAccountLock"])
# print(conn.entries)

# # msg_id = conn.search()
# # response = conn.get_response()
# print(conn.extend.standard.who_am_i())

# ------------------

# import httpx
# import asyncio


# async def fetch(url):
#     async with httpx.AsyncClient() as client:
#         r = await client.get(url)
#         return r.status_code


# async def main():
#     urls = ["https://example.com",
#             "https://www.youtube.com", "https://bing.com"]
#     tasks = [fetch(url) for url in urls]
#     results = await asyncio.gather(*tasks)
#     print(results)

# asyncio.run(main())

# ------------------

from fastapi import FastAPI, Query
import httpx
import asyncio

app = FastAPI()


async def fetch_url(url: str) -> str:
    """Делает запрос по httpx к url асинхронно, возвращает status_code"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return f"{url} → {response.status_code}"


async def fetch_urls(urls: list[str]) -> list[str]:
    """Параллельно делает запросы к списку URL"""
    tasks = [fetch_url(url) for url in urls]
    return await asyncio.gather(*tasks)


@app.get("/ping-all")
async def ping_all(urls: list[str] = Query(...)):
    return await fetch_urls(urls)
