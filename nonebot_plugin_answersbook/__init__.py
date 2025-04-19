import random
from pathlib import Path

from nonebot import on_startswith
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
from nonebot.params import EventPlainText
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State

__plugin_meta__ = PluginMetadata(
    name="答案之书",
    description="这是一本治愈系的心灵解惑书，它将带给你的不止是生活的指引，还有心灵的慰藉。",
    usage=("· /答案之书 <问题>  # 翻看这个问题的答案\n· <回复一条消息> /答案之书  # 翻看这个问题的答案\n"),
)

answers_path = Path(__file__).parent / "answersbook.txt"
answers = answers_path.read_text("utf-8").splitlines()

# 只使用 on_startswith
look_answer = on_startswith("/答案之书")

@look_answer.handle()
async def answersbook(
    event: MessageEvent, state: T_State, message: str = EventPlainText()
) -> None:
    state["user_id"] = event.user_id

    # 如果有回复的消息，进入提问流程
    if event.reply or message.strip() != "/答案之书":
        state["question"] = True

    # 如果消息是 "/答案之书" 且没有后续问题
    elif message.strip() == "/答案之书":
        # 直接提示用户输入问题
        await look_answer.finish(
        MessageSegment.at(event.user_id)
        + MessageSegment.text(" 你想问什么问题呢？请重试一次吧~")
    )
@look_answer.got("question", prompt=Message.template("{user_id:at} 你想问什么问题呢？"))
async def question(event: MessageEvent) -> None:
    reply_id = event.reply.message_id if event.reply else event.message_id
    await look_answer.finish(
        MessageSegment.reply(reply_id)
        + MessageSegment.at(event.user_id)
        + MessageSegment.text(" ")
        + MessageSegment.text(random.choice(answers))
    )
