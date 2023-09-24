#!/usr/bin/env python3

import asyncio
from postgrest import AsyncPostgrestClient


async def main():
    async with AsyncPostgrestClient("http://localhost:3000") as client:
        # r = await client.schema("public").from_("todos").select("*").execute()
        r = await client.schema("api").from_("todos").select("*").execute()
        countries = r.data
        print(countries)

async def selectall():
    async with AsyncPostgrestClient("http://localhost:3000") as client:
        r = await client.schema("api").from_("ogginvendita").select("*").execute()
        print(r) 
        return r       

if __name__ == '__main__':
    '''
    BEGIN OF MAIN
    '''

asyncio.run(main())



# await client.from_("countries").insert({ "name": "Việt Nam", "capital": "Hà Nội" }).execute()

# r = await client.from_("countries").select("id", "name").execute()
# countries = r.data

# await client.from_("countries").update({"capital": "Hà Nội"}).eq("name", "Việt Nam").execute()

# await client.from_("countries").delete().eq("name", "Việt Nam").execute()