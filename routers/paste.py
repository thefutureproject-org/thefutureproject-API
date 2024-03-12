import aiohttp


async def spacebin(txt):
  async with aiohttp.ClientSession() as session:
    u="https://spaceb.in/api/v1/documents/"
    jso={"content": txt, "extension":"txt"}
    async with session.post(u, json=jso) as resp:
      r=await resp.json(content_type=None)
      id_=r["payload"]["id"]
      url="https://spaceb.in/"+id_
      return url

