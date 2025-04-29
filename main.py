from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import httpx
from datetime import datetime, timedelta
@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("电子冷却状态")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)      
        async with httpx.AsyncClient() as client:
            now = datetime.now()
            fromtime=now - timedelta(hours=8)
            params = {
                "pv": "SRing:VA84VGC01.PRE1",  # 输入百度搜索的内容
                "from":fromtime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "to":now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
            response = await client.get("http://100.67.254.31:8080/retrieval/data/getData.json", params=params)
            response.encoding = response.charset_encoding
            yield event.plain_result(response.text) # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
