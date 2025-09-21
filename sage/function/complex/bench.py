from langchain_core.output_parsers import StrOutputParser
from langchain_qwq import ChatQwen
from loguru import logger

from sage.complex.config.inventory import UrlSettings, keys_qwen

llm = ChatQwen(
    base_url=UrlSettings.QWEN_BASE_URL,
    api_key=keys_qwen(),
    model="qwen-plus",
)
chain = llm | StrOutputParser()
response = chain.invoke("杭州明天的天气怎么样？")

logger.info(response)
