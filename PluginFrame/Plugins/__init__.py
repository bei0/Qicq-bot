from PluginFrame.PluginManager import ModelComponent
from cqhttp.api import CQApiConfig
from cqhttp.request_model import SendGroupMsgRequest, SendPrivateMsgRequest, SendGroupNodeMsgRequest, \
    SendPrivateNodeMsgRequest


class BaseComponentPlugin(ModelComponent):

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
