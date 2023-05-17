import time
from aiocqhttp import MessageSegment
from loguru import logger
from PluginFrame.PluginManager import ModelComponent
from cqhttp.api import CQApiConfig
from cqhttp.request_model import SendGroupMsgRequest, SendPrivateMsgRequest, SendGroupNodeMsgRequest, \
    SendPrivateNodeMsgRequest, DeleteMsgRequest



class BaseComponentPlugin(ModelComponent):

    __name__ = 'BaseComponentPlugin'

    @staticmethod
    async def send_group_msg(group_id, message):
        return await SendGroupMsgRequest(group_id=group_id, message=message).send_request(
            CQApiConfig.message.send_group_msg.Api
        )

    @staticmethod
    async def send_private_msg(user_id, message):
        return await SendPrivateMsgRequest(user_id=user_id, message=message).send_request(
            CQApiConfig.message.send_private_msg.Api
        )

    @staticmethod
    async def send_group_node_msg(group_id, messages):
        return await SendGroupNodeMsgRequest(group_id=group_id, messages=messages).send_request(
            CQApiConfig.message.send_group_forward_msg.Api
        )

    @staticmethod
    async def send_private_node_msg(user_id, messages):
        return await SendPrivateNodeMsgRequest(user_id=user_id, messages=messages).send_request(
            CQApiConfig.message.send_private_forward_msg.Api
        )

    @staticmethod
    def send(func, user_id=None, group_id=None):
        async def send_req(*s_args, **s_kwargs):
            if user_id:
                return await func(user_id, *s_args, **s_kwargs)
            else:
                return await func(group_id, *s_args, **s_kwargs)
        return send_req

    @staticmethod
    def send_wait(func, user_id=None, group_id=None):

        async def send_req(message_id, message, *s_args, **s_kwargs):
            wait_message = f"""{MessageSegment.reply(message_id)} {message}"""
            if user_id:
                return await func(user_id, wait_message)
            else:
                return await func(group_id, wait_message)
        return send_req

    @staticmethod
    async def del_wait(message_id):
        time.sleep(2)
        info = await DeleteMsgRequest(message_id=message_id).send_request(
            CQApiConfig.message.delete_msg.Api
        )
        return info

    # @staticmethod
    # def response(event, is_group: bool, bot):
    #     async def respond(resp):
    #         logger.debug(f"[OneBot] 尝试发送消息：{str(resp)}")
    #         try:
    #             if not isinstance(resp, (MessageChain, Image, Plain, Voice)):
    #                 resp = MessageChain(resp)
    #
    #             if isinstance(resp, Image):
    #                 resp = MessageSegment.image(f"base64://{resp.base64}")
    #             else:
    #                 resp = transform_from_message_chain(resp)
    #
    #             if config.response.quote and '[CQ:record,file=' not in str(resp):  # skip voice
    #                 resp = MessageSegment.reply(event.message_id) + resp
    #             await bot.send(event, resp)
    #
    #         except Exception as e:
    #             logger.exception(e)
    #             logger.warning("原始消息发送失败，尝试通过转发发送")
    #             if is_group:
    #                 return await BaseComponentPlugin.send_group_node_msg(
    #                     group_id=event.group_id,
    #                     messages=[
    #                         MessageSegment.node_custom(event.self_id, "ChatGPT", resp)
    #                     ]
    #                 )
    #             else:
    #                 return await BaseComponentPlugin.send_private_node_msg(
    #                     user_id=event.user_id,
    #                     messages=[
    #                         MessageSegment.node_custom(event.self_id, "ChatGPT", resp)
    #                     ]
    #                 )
    #
    #     return respond
