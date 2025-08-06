from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp
import os

@register(
    "donate", 
    "10XuQ", 
    "赞助插件，用户发送/赞助时返回收款码",  
    "1.0.0",  
    "https://github.com/10XuQ/astrbot_plugin_donate"  
)
class DonatePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.qrcode_path = os.path.join(os.path.dirname(__file__), "qrcode.jpg")
        if not os.path.exists(self.qrcode_path):
            logger.warning(f"收款码图片不存在: {self.qrcode_path}")

    @filter.command("赞助")
    async def donate_handler(self, event: AstrMessageEvent):
        try:
            if not os.path.exists(self.qrcode_path):
                yield event.plain_result("抱歉，收款码图片未配置，请联系管理员。")
                return
            
            yield event.chain_result([
                Comp.Plain("感谢您的支持！请扫描下方二维码进行赞助：\n"),
                Comp.Image.fromFileSystem(self.qrcode_path)
            ])
            yield event.plain_result("您的支持是我们持续开发的动力，非常感谢！")
            
        except Exception as e:
            logger.error(f"处理赞助指令时出错: {str(e)}")
            yield event.plain_result("处理请求时发生错误，请稍后再试。")

    async def terminate(self):
        logger.info("赞助插件已停止运行")
