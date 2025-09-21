from langchain_core.output_parsers import StrOutputParser
from loguru import logger

from sage.components.inventory import llm

chain = llm() | StrOutputParser()
response = chain.invoke("杭州明天的天气怎么样？")

logger.info(response)
