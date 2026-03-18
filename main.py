import random

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.core import AstrBotConfig
from astrbot.core.message.components import Reply, Plain
from astrbot.core.message.message_event_result import MessageEventResult, MessageChain
from .meihua import meihuaByNumber


@register("astrbot_plugin_meihua", "985892345", "梅花易数起卦断卦工具", "0.0.1")
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好，{user_name}!`
    @filter.command("梅花")
    async def meihua_command(self, event: AstrMessageEvent):
        """
        /梅花 [问题] | /梅花 [2-6 个数字] [问题]
        """  # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        message_str = event.message_str  # 用户发的纯文本消息字符串

        # 解析输入，拆分出第一部分
        parts = message_str.split(maxsplit=1)
        message = parts[1] if len(parts) > 1 else "未提供问题"
        args = message.split(maxsplit=1)
        first_part = args[0]
        
        # 判断第一部分是否为纯数字
        if first_part.isdigit():
            # 全是数字，作为起卦的数
            number = first_part
            question = args[1] if len(args) > 1 else "未提供问题"
            # 验证数字位数
            if len(number) < 2:
                yield event.plain_result(f"错误：数字位数不能小于两位，当前数字为 {number}")
                return
        else:
            number = "" # 后续生成随机数
            # 整个消息作为问题
            question = message

        result = self.meihua_send(event.get_sender_name(), question, number)
        result += f"大模型断卦中...\n"

        yield event.plain_result(result)

        umo = event.unified_msg_origin
        provider_id = self.context.get_provider_by_id(
            self.config.get("judge_provider_id", "")
        ) or self.context.get_current_chat_provider_id(umo)
        divination_judgment_prompt = self.config.get("divination_judgment_prompt", "")
        llm_resp = await self.context.llm_generate(
            chat_provider_id=provider_id,  # 聊天模型 ID
            prompt=f"{divination_judgment_prompt}\n{result}",
        )

        # 引用之前的卦象结果消息
        yield event.chain_result(
            [
                Reply(id=event.message_obj.message_id),
                Plain(text=llm_resp.completion_text)
            ]
        )

    @filter.llm_tool(name="meihua_llm")  # 如果 name 不填，将使用函数名
    async def meihua_llm(self, event: AstrMessageEvent, question: str = "未提供问题", number: str = ""):
        '''使用梅花易数排卦
        Args:
            question(string): 问题，未解析到问题时需要传入“未提供问题” !!!
            number(string): 数字，非必须，不传入时使用随机数断
        '''
        result = self.meihua_send(event.get_sender_name(), question, number)
        result += f"大模型断卦中...（该模式受人格限制为精简回复，详细模式请使用 /梅花）\n"

        await event.send(MessageChain().message(result))

        return f"你擅长各种玄学占卜，请使用梅花易数详细分析下求卦者的现状、过程、结果以及可能会发生的状况，要求 200 字以内：{result}"

    def meihua_send(self, sender_name: str, question: str, number: str):
        is_random = False
        if not number.isdigit():
            # 包含非数字字符，随机生成 3-6 位数字
            num_digits = random.randint(3, 6)
            number = ''.join([str(random.randint(0, 9)) for _ in range(num_digits)])
            is_random = True

        # 确定用卦（有动爻的卦为用卦，无动爻的卦为本卦）
        result = f"🌸 梅花易数占卜 🌸\n"
        result += f"问卜者：{sender_name}\n"
        result += f"问题：{question}\n"
        result += f"起卦数字：{number}{' (随机)' if is_random else ''}\n"
        result += f"--------------------\n"

        result += meihuaByNumber(number)
        # 发送卦象
        return result

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
