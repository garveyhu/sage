from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain_elasticsearch.chat_history import ElasticsearchChatMessageHistory

from sage.complex.config.inventory import dialog_id
from sage.components.inventory import elasticsearch, llm


class ElasticsearchMemory:
    """Elasticsearch存储聊天历史（只存储上下文文本，不向量化）."""

    def __init__(self):
        self.history = ElasticsearchChatMessageHistory(
            es_connection=elasticsearch(),
            index="chat_history",
            session_id=dialog_id(),
        )

    def summarize_memory(self, **kwargs):
        """对历史进行LLM总结，生成新的历史上下文."""
        return ConversationSummaryMemory.from_messages(
            llm=llm(),
            chat_memory=self.history,
            return_messages=True,
            **kwargs,
        )

    def buffer_window_memory(self, **kwargs):
        """对历史进行滑动窗口设置，生成窗口大小的历史上下文."""
        return ConversationBufferWindowMemory(
            chat_memory=self.history, return_messages=True, **kwargs
        )
