from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp
import os

# 注册插件元数据
@register(
    name="donate",
    author="你的名字",
    description="赞助插件，用户发送/赞助时返回收款码",
    version="1.0.0",
    repo_url="https://github.com/你的用户名/astrbot_plugin_donate"
)
class DonatePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 初始化时检查收款码图片是否存在
        self.qrcode_path = os.path.join(os.path.dirname(__file__), "qrcode.jpg")
        if not os.path.exists(self.qrcode_path):
            logger.warning(f"收款码图片不存在: {self.qrcode_path}")
            logger.warning("请将收款码图片命名为qrcode.jpg并放在插件目录下")

    # 注册/赞助指令处理函数
    @filter.command("赞助")
    async def donate_handler(self, event: AstrMessageEvent):
        """处理/赞助指令，返回收款码图片"""
        try:
            # 检查图片是否存在
            if not os.path.exists(self.qrcode_path):
                yield event.plain_result("抱歉，收款码图片未配置，请联系管理员。")
                return
            
            # 发送赞助提示和收款码
            yield event.chain_result([
                Comp.Plain("感谢您的支持！请扫描下方二维码进行赞助：\n"),
                Comp.Image.fromFileSystem(self.qrcode_path)
            ])
            
            # 可以添加额外的感谢信息
            yield event.plain_result("您的支持是我们持续开发的动力，非常感谢！")
            
        except Exception as e:
            logger.error(f"处理赞助指令时出错: {str(e)}")
            yield event.plain_result("处理请求时发生错误，请稍后再试。")

    # 插件卸载时执行的操作
    async def terminate(self):
        logger.info("赞助插件已停止运行")
