import aiocqhttp
from aiocqhttp import MessageSegment
from PluginFrame.chace_data import get_cache
from cqhttp.api import CQApiConfig
from cqhttp.request_model import SendRequest, SendGroupMsgRequest
from cqhttp import bot


class NoticeDispose:

    async def dispose(self, event: aiocqhttp.Event):
        if event.detail_type == "group_increase":
            return await self.join_the_group_prompt(event)
        if event.detail_type == "group_decrease":
            infos = get_cache("group_exit") or []
            if event.group_id in infos:
                if event.sub_type == "leave":
                    message = MessageSegment.text(f'成员<{event.user_id}>退群了！')
                elif event.sub_type == "kick":
                    message = MessageSegment.text(f'管理员<{event.operator_id}>将成员<{event.user_id}>T出群聊！')
                else:
                    message = MessageSegment.text(f'成员<{event.user_id}>被封退出群聊！')
                return await bot.send(event, message)

    async def join_the_group_prompt(self, event: aiocqhttp.Event):
        text = get_cache(str(event.group_id))
        if text:
            message_info = f"""🎉欢迎加入本群🎉亲爱的{MessageSegment.at(event.user_id)}\n{text}
            """.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")

            return await SendGroupMsgRequest(
                message=message_info,
                group_id=event.group_id
            ).send_request(CQApiConfig.message.send_group_msg.Api)
