from typing import Optional

from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain_community.chat_message_histories import (
    RedisChatMessageHistory as BaseRedisChatMessageHistory,
)
from redis import Redis

from sage.complex.config.inventory import dialog_id
from sage.components.llms.llm_factory import LLMFactory
from sage.components.manager.redis import RedisManager


class RedisMemory:
    """Redis存储聊天历史（只存储上下文文本，不向量化）."""

    def __init__(self):
        self.history = RedisChatMessageHistory(
            redis_client=RedisManager().client,
            key_prefix="chat_history",
            session_id=dialog_id(),
        )

    def summarize_memory(self, **kwargs):
        return ConversationSummaryMemory.from_messages(
            llm=LLMFactory.create_llm(),
            chat_memory=self.history,
            return_messages=True,
            **kwargs,
        )

    def buffer_window_memory(self, **kwargs):
        return ConversationBufferWindowMemory(
            chat_memory=self.history, return_messages=True, **kwargs
        )


class RedisChatMessageHistory(BaseRedisChatMessageHistory):
    """Using an external Redis client"""

    def __init__(
        self,
        redis_client: "Redis",
        session_id: str,
        key_prefix: str,
        ttl: Optional[int] = None,
    ):
        self.redis_client = redis_client
        self.session_id = session_id
        self.key_prefix = key_prefix
        self.ttl = ttl
