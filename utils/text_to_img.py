import base64
import pathlib
import re
import shutil
import uuid
from io import StringIO, BytesIO
from tempfile import NamedTemporaryFile

import markdown as markdown
from PIL import Image, ImageFont, ImageDraw
import os

from charset_normalizer import from_bytes
from loguru import logger
from pygments.formatters.html import HtmlFormatter
from pygments.styles.xcode import XcodeStyle
from mdx_math import MathExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.tables import TableExtension
import imgkit
from config import Config
from cqhttp.cq_code import CqImage
from utils.simple_to_img import create_img


class MdToImg:

    class DisableHTMLExtension(markdown.Extension):
        def extendMarkdown(self, md):
            md.inlinePatterns.deregister('html')
            md.preprocessors.deregister('html_block')

    @property
    def template_html(self):
        template_html = ''
        with open(os.path.join(Config.BasePath, "static/texttoimg/template.html"), "rb") as f:
            guessed_str = from_bytes(f.read()).best()
            if not guessed_str:
                raise ValueError("无法识别 Markdown 模板 template.html，请检查是否输入有误！")
            # 获取 Pygments 生成的 CSS 样式
            highlight_css = HtmlFormatter(style=XcodeStyle).get_style_defs('.highlight')
            template_html = str(guessed_str).replace("{highlight_css}", highlight_css)
        return template_html

    @staticmethod
    def make_extension(**kwargs):
        return MdToImg.DisableHTMLExtension(**kwargs)

    def md_to_html(self, text):
        extensions = [
            self.DisableHTMLExtension(),
            MathExtension(enable_dollar_delimiter=True),  # 开启美元符号渲染
            CodeHiliteExtension(linenums=False, css_class='highlight', noclasses=False, guess_lang=True),  # 添加代码块语法高亮
            TableExtension(),
            'fenced_code'
        ]
        md = markdown.Markdown(extensions=extensions)
        h = md.convert(text)
        # 获取 Pygments 生成的 CSS 样式
        css_style = HtmlFormatter(style=XcodeStyle).get_style_defs('.highlight')
        # 将 CSS 样式插入到 HTML 中
        h = f"<style>{css_style}</style>\n{h}"
        return h

    async def text_to_image(self, text):
        ok, image = False, None
        asset_folder = os.path.join(Config.BasePath, 'static', 'texttoimg')
        font_path = os.path.join(Config.BasePath, 'static', 'fonts', 'sarasa-mono-sc-regular.ttf')
        try:
            content = self.md_to_html(text)
            # 输出html到字符串io流
            with StringIO() as output_file:
                # 填充正文
                html = self.template_html.replace('{path_texttoimg}', pathlib.Path(asset_folder).as_uri())\
                    .replace("{content}", content) \
                    .replace("{font_size_texttoimg}", str(30)) \
                    .replace("{font_path_texttoimg}", pathlib.Path(font_path).as_uri())
                output_file.write(html)

                # 创建临时jpg文件
                temp_jpg_file = NamedTemporaryFile(mode='w+b', suffix='.png')
                temp_jpg_filename = temp_jpg_file.name
                temp_jpg_file.close()

            temp_html_file = NamedTemporaryFile(mode='w', suffix='.html', encoding='utf-8')
            imgkit_config = imgkit.config(wkhtmltoimage=shutil.which("wkhtmltoimage"))
            with StringIO(html) as input_file:
                ok = False
                try:
                    temp_html_file.write(html)
                    # 调用imgkit将html转为图片
                    ok = imgkit.from_file(
                        filename=input_file, config=imgkit_config,
                        options={
                            "enable-local-file-access": "",
                            "allow": asset_folder,
                            "width": 700,
                            "javascript-delay": "1000"
                        },
                        output_path=temp_jpg_filename
                    )
                    # 调用PIL将图片读取为 JPEG，RGB 格式
                    image = Image.open(temp_jpg_filename, formats=['PNG']).convert('RGB')
                    ok = True
                except Exception as e:
                    logger.error("Markdown 渲染失败，使用备用模式")
                    # logger.exception(e)
                finally:
                    # 删除临时文件
                    if os.path.exists(temp_jpg_filename):
                        os.remove(temp_jpg_filename)
        except Exception as e:
            # logger.exception(e)
            logger.error("Markdown 渲染失败，使用备用模式")
        if not ok:
            image = create_img(text)

        return image


async def to_image(text):
    img = await MdToImg().text_to_image(text=text)
    b = BytesIO()
    img.save(b, format="png")
    return CqImage(file="base64://"+base64.b64encode(b.getvalue()).decode()).cq

