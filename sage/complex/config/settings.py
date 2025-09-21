from .base_settings import CONFIG_PATH, BaseSettings


class URLSettings(BaseSettings):
    """BASE_URL配置"""

    URL_PATH = CONFIG_PATH / "baseurl.json"

    def __init__(self):
        super().__init__()
        self.load()

    def load(self):
        self.data = self.from_json(self.URL_PATH).data


class MODELSettings(BaseSettings):
    """MODEL配置"""

    MODEL_PATH = CONFIG_PATH / "model.json"

    def __init__(self):
        super().__init__()
        self.load()

    def load(self):
        self.data = self.from_json(self.MODEL_PATH).data


class COMPONENTSettings(BaseSettings):
    """COMPONENT配置"""

    COMPONENT_PATH = CONFIG_PATH / "component.json"

    def __init__(self):
        super().__init__()
        self.load()

    def load(self):
        self.data = self.from_json(self.COMPONENT_PATH).data


class USERSettings(BaseSettings):
    """USER配置"""

    USER_PATH = CONFIG_PATH / "user.json"

    def __init__(self):
        super().__init__()
        self.load()

    def load(self):
        self.data = self.from_json(self.USER_PATH).data


url_settings = URLSettings()
model_settings = MODELSettings()
component_settings = COMPONENTSettings()
user_settings = USERSettings()
