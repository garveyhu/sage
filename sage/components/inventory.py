from sage.components.embeddings.embedding_factory import EmbeddingFactory
from sage.components.llms.llm_factory import LLMFactory
from sage.components.manager.elasticsearch import ElasticsearchManager
from sage.components.manager.redis import RedisManager
from sage.components.memory.elasticsearch import ElasticsearchMemory
from sage.components.memory.redis import RedisMemory
from sage.components.vector.elasticsearch import ElasticsearchVector


"""⭐llm⭐"""


def llm():
    """`LLMFactory`
    获取llm模型
    """
    return LLMFactory().create_llm()


"""⭐embedding⭐"""


def embedding():
    """`EmbeddingFactory`
    获取embedding模型
    """
    return EmbeddingFactory.create_embedding()


"""⭐manager⭐"""


def elasticsearch():
    """`ElasticsearchManager`
    获取elasticsearch客户端
    """
    return ElasticsearchManager().client


def redis():
    """`RedisManager`
    获取redis客户端
    """
    return RedisManager().client


"""⭐memory⭐"""


def es_summarize_memory(**kwargs):
    """`ElasticsearchMemory`
    对历史进行LLM总结，生成新的历史上下文

    Example:
        .. code-block:: python

            memory = es_summarize_memory()
            conversation_chain = ConversationChain(llm=llm, verbose=True, memory=memory)
            result = conversation_chain.predict(input=text)

    Args:
        buffer: str = ""
        memory_key: str = "history"
    """
    return ElasticsearchMemory().summarize_memory(**kwargs)


def es_buffer_window_memory(**kwargs):
    """`ElasticsearchMemory`
    对历史进行滑动窗口设置，生成窗口大小的历史上下文

    Example:
        .. code-block:: python

            memory = es_buffer_window_memory(k=3)
            conversation_chain = ConversationChain(llm=llm, verbose=True, memory=memory)
            result = conversation_chain.predict(input=text)

    Args:
        human_prefix: str = "Human"
        ai_prefix: str = "AI"
        memory_key: str = "history"
        k: int = 5
    """
    return ElasticsearchMemory().buffer_window_memory(**kwargs)


def redis_summarize_memory(**kwargs):
    """`RedisMemory`
    对历史进行LLM总结，生成新的历史上下文

    Example:
        .. code-block:: python

            memory = redis_summarize_memory()
            conversation_chain = ConversationChain(llm=llm, verbose=True, memory=memory)
            result = conversation_chain.predict(input=text)

    Args:
        buffer: str = ""
        memory_key: str = "history"
    """
    return RedisMemory().summarize_memory(**kwargs)


def redis_buffer_window_memory(**kwargs):
    """`RedisMemory`
    对历史进行滑动窗口设置，生成窗口大小的历史上下文

    Example:
        .. code-block:: python

            memory = redis_buffer_window_memory(k=3)
            conversation_chain = ConversationChain(llm=llm, verbose=True, memory=memory)
            result = conversation_chain.predict(input=text)

    Args:
        human_prefix: str = "Human"
        ai_prefix: str = "AI"
        memory_key: str = "history"
        k: int = 5
    """
    return RedisMemory().buffer_window_memory(**kwargs)


"""⭐vector⭐"""


def es_dialog_vector():
    """`ElasticsearchVector`
    会话向量Store

    Example:
        .. code-block:: python

            db = es_dialog_vector()
            db.add_documents(content)
            db.client.indices.refresh(index=ElasticsearchVector.dialog_index())

    """
    return ElasticsearchVector().dialog_vector()


def es_resource_vector():
    """`ElasticsearchVector`
    资源向量Store

    Example:
        .. code-block:: python

            db = es_resource_vector()
            db.add_documents(content)
            db.client.indices.refresh(index=ElasticsearchVector.resource_index())
    """
    return ElasticsearchVector().resource_vector()
