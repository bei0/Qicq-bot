import base64
import io
import re
from io import BytesIO
import requests
from PIL import Image
from PluginFrame.Plugins import BaseComponentPlugin
from PluginFrame.plugins_conf import registration_directive
from cqhttp.api import CQApiConfig
from aiocqhttp import MessageSegment
from cqhttp.request_model import SendPrivateMsgRequest, SendGroupMsgRequest, GetMessage


@registration_directive(matching=r'^\[CQ:reply,id=(-\d+|\d+)\](\[CQ:at,qq=(\d+)\]|)(| )(放大|缩小)(\d{1})倍',
                        message_types=("private", "group"))
class ImageVariationPlugin(BaseComponentPlugin):
    __name__ = 'ImageVariationPlugin'
    desc = "图片放大/缩小"
    docs = '引用图片消息 [放大/缩小][1-9]倍 【群内去掉At】'
    permissions = ("all",)
    plu_name = '图片插件'

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        message_id, _, qq, _, im_type, number = message_parameter.get("re_obj").groups()
        info = await GetMessage(message_id=message_id).send_request(api=CQApiConfig.message.get_msg.Api)
        if not info: return
        message_data = info.get("message")
        url = re.match(r"(| )\[CQ:image.*url=(.*)]", message_data).group(2)
        image_data, fmt = self.download_image(url)
        img_b64 = self.image_zoom(image_data, number, im_type, fmt=fmt)
        if not img_b64:
            await bot.send(event, MessageSegment.reply(event.message_id).__add__(
                MessageSegment.text("图片不合法")
            ))

        message = MessageSegment.reply(event.message_id).__add__(
            MessageSegment.image(file=f"base64://{img_b64}", type=fmt)
        )
        await bot.send(event, message)

    def download_image(self, url):
        try:
            response = requests.get(url)
            fmt = response.headers.get("Content-Type", 'image/jpeg')
            fmt = fmt.split("/")[1]
            with Image.open(BytesIO(response.content)) as _img:
                image_data = self.image_to_base64(_img, fmt=fmt)
            return image_data, fmt
        except:
            return None

    @staticmethod
    def image_to_base64(img, fmt='png'):
        output_buffer = BytesIO()
        img.save(output_buffer, format=fmt)
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode('utf-8')
        return base64_str

    def image_zoom(self, imgdata, scale=1, scale_type=None, fmt='png'):
        buffer = io.BytesIO()
        imgdata = base64.b64decode(imgdata)
        img = Image.open(io.BytesIO(imgdata))
        if scale_type == "缩小":
            new_img = img.resize((img.size[0]//int(scale), img.size[1]//int(scale)))
        elif scale_type == "放大":
            new_img = img.resize((img.size[0] * int(scale), img.size[1] * int(scale)))
        else:
            return
        new_img.save(buffer, format=fmt)
        img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return img_b64
