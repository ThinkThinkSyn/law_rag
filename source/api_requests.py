import aiohttp
import asyncio
from loguru import logger
from typing import Optional

from .config import CONFIG
from .data_types import RagMethod, RagType, Language

ENDPOINT = CONFIG["endpoint"]['prod']


async def request_law_rag_chat(
    prompt: str,
    api_access_key: str,
    language: Language = Language.english,
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
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"{ENDPOINT}/legalexp/rag/chat",
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


async def submit_review(
    api_access_key: str,
    rating: int,
    comment: str,
    configuration: Optional[str] = None,
):
    json = {
        "rating": rating,
        "comment": comment,
        "configuration": configuration or "",
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"{ENDPOINT}/legalexp/review/submit",
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
    
