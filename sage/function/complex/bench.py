from langchain_core.output_parsers import StrOutputParser
from loguru import logger

from sage.components.inventory import llm

chain = llm() | StrOutputParser()
response = chain.invoke("介绍一下塞尔达传说旷野之息")

logger.info(response)
