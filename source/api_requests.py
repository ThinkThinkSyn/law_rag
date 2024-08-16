import aiohttp
import asyncio
from enum import Enum
from loguru import logger

from .config import CONFIG

ENDPOINT = CONFIG["endpoint"]['prod']


class Language(str, Enum):
    english = "en"
    chinese = "zh"


class RagMethod(str, Enum):
    DirectMatch = "DirectMatch"
    ParentDoc = "ParentDoc"
    NER = "NER"
    Hypothetical = "HypoQuery"


class RagType(str, Enum):
    Common = "Common"
    Fusion = "Fusion"
    

async def request_law_rag_chat(
    prompt: str,
    api_access_key: str,
    language: str = "zh",
    method: RagMethod = RagMethod.DirectMatch,
    rag_type: RagType = RagType.Common,
    top_k: int = 10,
    parent_level: int = 1,
):
    json = {
        "prompt": prompt,
        "lang": language,
        "method": method,
        "type_use": rag_type,
        "top_k": top_k,
        "parent_level": parent_level,
        "return_retrieved": True,
    }
    logger.info(
        f"Requesting chat with args {str(json)}"
    )
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=ENDPOINT,
            json=json,
            headers={
                "Authorization": f"Bearer {api_access_key}",
            },
        ) as response:
            if response.status == 200:
                response = await response.json()
                return response
            elif response.status == 401:
                raise ValueError("Invalid API Access Key")
            else:
                raise Exception(f"Failed to retrieve response from server. Status code: {response.status}")



if __name__ == "__main__":
    question = "What is the legal age to drink in Hong Kong?"
    print(asyncio.run(request_law_rag_chat(question)))
    
