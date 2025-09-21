from .settings import component_settings, model_settings, url_settings, user_settings

"""⭐cases⭐"""


def case_llm():
    """获取使用的llm模型类型"""
    return model_settings.get("cases.llm")


def set_case_llm(value):
    """设置llm模型类型"""
    model_settings.set("cases.llm", value)


def case_embedding():
    """获取使用的embedding模型类型"""
    return model_settings.get("cases.embedding")


"""⭐keys⭐"""


def keys_openai():
    """获取openai keys"""
    config = model_settings.get("keys.openai")
    return config["OPENAI_API_KEY"]


def keys_deepseek():
    """获取deepseek keys"""
    config = model_settings.get("keys.deepseek")
    return config["DEEPSEEK_API_KEY"]


def keys_qwen():
    """获取qwen keys"""
    config = model_settings.get("keys.qwen")
    return config["QWEN_API_KEY"]


def keys_pinecone():
    """获取pinecone keys"""
    config = model_settings.get("keys.pinecone")
    return config["PINECONE_API_KEY"]


"""⭐models⭐"""


def models_llm():
    """获取llm模型列表"""
    return model_settings.get("models.llm")


def models_embedding():
    """获取embedding模型列表"""
    return model_settings.get("models.embedding")


def llm_temperature():
    """获取llm模型温度"""
    llm_list = models_llm()
    current_llm = case_llm()
    for model in llm_list:
        if model["name"] == current_llm:
            return float(model["temperature"])
    return None


def embedding_dimensions():
    """获取embedding模型维度"""
    embedding_list = models_embedding()
    current_embedding = case_embedding()
    for model in embedding_list:
        if model["name"] == current_embedding:
            return int(model["dimensions"])
    return None


"""⭐用户、会话、应用⭐"""


def user_id():
    """获取用户id"""
    return user_settings.get("user.id")


def set_user_id(value):
    """设置用户id"""
    user_settings.set("user.id", value)


def dialog_id():
    """获取会话id"""
    return user_settings.get("dialog.id")


def app_id():
    """获取应用id"""
    return user_settings.get("app.id")


"""⭐组件⭐"""


class ESSettings:
    """Elasticsearch配置"""

    TYPE = component_settings.get("elasticsearch.type")
    HOST_URL = component_settings.get("elasticsearch.host.url")
    USERNAME = component_settings.get("elasticsearch.host.username")
    PASSWORD = component_settings.get("elasticsearch.host.password")
    CLOUD_URL = component_settings.get("elasticsearch.cloud.url")
    API_KEY = component_settings.get("elasticsearch.cloud.api_key")


class MysqlSettings:
    """Mysql配置"""

    HOST = component_settings.get("mysql.host")
    PORT = component_settings.get("mysql.port")
    DB = component_settings.get("mysql.db")
    USER = component_settings.get("mysql.user")
    PASSWORD = component_settings.get("mysql.password")


class RedisSettings:
    """Redis配置"""

    HOST = component_settings.get("redis.host")
    PORT = component_settings.get("redis.port")
    DB = component_settings.get("redis.db")
    PASSWORD = component_settings.get("redis.password")
    TIMEOUT = component_settings.get("redis.socket_timeout")
    SENTINEL_MASTER = component_settings.get("redis.sentinel_master")
    SENTINEL_PASSWORD = component_settings.get("redis.sentinel_password")


"""⭐URL⭐"""


class UrlSettings:
    """Base_URL配置"""

    OPENAI_BASE_URL = url_settings.get("openai")
    QWEN_BASE_URL = url_settings.get("qwen")
    DEEPSEEK_BASE_URL = url_settings.get("deepseek")
