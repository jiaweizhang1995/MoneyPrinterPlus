# 设置 tongyi API 的基础 URL 和 API 密钥
import os

from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

# 导入PyQt6版本的配置管理器
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.config_manager import config_manager
from services.llm.llm_service import MyLLMService
from tools.utils import must_have_value


class MyTongyiServiceQt(MyLLMService):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数来初始化父类的属性
        
        # 从PyQt6配置管理器获取通义千问配置
        tongyi_config = config_manager.get_llm_config('Tongyi')
        self.TONGYI_API_KEY = tongyi_config.get('api_key', '')
        self.TONGYI_MODEL_NAME = tongyi_config.get('model_name', 'qwen-turbo')
        
        must_have_value(self.TONGYI_API_KEY, "请设置tongyi API 密钥")
        must_have_value(self.TONGYI_MODEL_NAME, "请设置tongyi API model")
        os.environ["DASHSCOPE_API_KEY"] = self.TONGYI_API_KEY

    def generate_content(self, topic: str, prompt_template: PromptTemplate, language: str = None, length: str = None):
        # 创建 Tongyi 的 LLM 实例
        llm = Tongyi(model=self.TONGYI_MODEL_NAME)

        description = llm.invoke(prompt_template.format(topic=topic, language=language, length=length))

        return description.strip()