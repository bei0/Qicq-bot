# -*- coding:utf-8 -*-

""" 模板语言"""
import base64
import os
import shutil
from io import StringIO, BytesIO
from tempfile import NamedTemporaryFile
from PIL import Image
import imgkit
from charset_normalizer import from_bytes
from loguru import logger

# TOKEN相关的定义
TOKEN_S_BRACE = "{"
TOKEN_S_BLOCK = "%"
TOKEN_EXPRESSION_L = "{{"
TOKEN_EXPRESSION_R = "}}"
TOKEN_BLOCK_L = "{%"
TOKEN_BLOCK_R = "%}"
TOKEN_KEY_SET = "set"
TOKEN_KEY_RAW = "raw"
TOKEN_KEY_IF = "if"
TOKEN_KEY_ELIF = "elif"
TOKEN_KEY_ELSE = "else"
TOKEN_KEY_FOR = "for"
TOKEN_KEY_WHILE = "while"
TOKEN_KEY_END = "end"
TOKEN_KEY_BREAK = "break"
TOKEN_KEY_CONTINUE = "continue"
TOKEN_SPACE = " "
TOKEN_COLON = ":"
# Token标记 {{}} {% %}
TOKEN_FLAG_SET = {TOKEN_S_BRACE, TOKEN_S_BLOCK}
# 简单的语句
TOKEN_KEY_SET_SIMPLE_EXPRESSION = {TOKEN_KEY_SET, TOKEN_KEY_RAW}
# 前置条件
TOKEN_KEY_PRE_CONDITION = {
    # end 必须在if/elif/else/for/while 后面
    TOKEN_KEY_END: {TOKEN_KEY_IF, TOKEN_KEY_ELIF, TOKEN_KEY_ELSE,
                    TOKEN_KEY_FOR, TOKEN_KEY_WHILE},
    # elif 必须在if 后面
    TOKEN_KEY_ELIF: {TOKEN_KEY_IF},
    # else 必须在if/elif 后面
    TOKEN_KEY_ELSE: {TOKEN_KEY_IF, TOKEN_KEY_ELIF, TOKEN_KEY_FOR, TOKEN_KEY_WHILE},
}
# 循环语句
TOKEN_KEY_LOOP = {TOKEN_KEY_WHILE, TOKEN_KEY_FOR}
# 循环的控制break continue
TOKEN_KEY_LOOP_CTRL = {TOKEN_KEY_BREAK, TOKEN_KEY_CONTINUE}


class ParseException(Exception):
    pass


class TemplateCode(object):
    def __init__(self):
        self.codeTrees = {"parent": None, "nodes": []}
        self.cursor = self.codeTrees
        self.compiled_code = None

    def create_code(self):
        """创建一个代码子块"""
        child_codes = {"parent": self.cursor, "nodes": []}
        self.cursor["nodes"].append(child_codes)
        self.cursor = child_codes

    def close_code(self):
        """ 关闭一个代码子块 """
        assert self.cursor["parent"] is not None, "overflow"
        self.cursor = self.cursor["parent"]

    def append_text(self, text):
        """ 添加文本 """
        # 排除空行
        self.cursor["nodes"].append("_add(%r)" % text)

    def append_express(self, express, raw=False):
        """ 表达式 """
        if raw:
            temp_exp = "_t_exp = _str_(%s)" % express
        else:
            temp_exp = "_t_exp = _esc_(%s)" % express
        self.cursor["nodes"].append(temp_exp)
        self.cursor["nodes"].append("_add(_t_exp)")

    def append_statement(self, statement):
        """ 语句 """
        temp_statement = "%s" % statement
        self.cursor["nodes"].append(temp_statement)

    def reset(self):
        self.codeTrees = {"parent": None, "nodes": []}
        self.cursor = self.codeTrees
        self.compiled_code = None

    def build_code(self, filename):
        temp_code_buff = []
        self.write_buff_with_indent(temp_code_buff, "def _template_render():", 0)
        self.write_buff_with_indent(temp_code_buff, "_codes = []", 4)
        self.write_buff_with_indent(temp_code_buff, "_add = _codes.append", 4)
        self.write_codes(temp_code_buff, self.codeTrees, 4)
        self.write_buff_with_indent(temp_code_buff, "return ''.join(_codes)", 4)
        temp_code = "".join(temp_code_buff)
        self.compiled_code = compile(temp_code,filename, "exec", dont_inherit=True)

    def write_codes(self, code_buff, codes, indent):
        for node in codes.get("nodes", []):
            if isinstance(node, dict):
                self.write_codes(code_buff, node, indent+4)
            else:
                self.write_buff_with_indent(code_buff, node, indent)

    def generate(self, **kwargs):
        temp_namespace = {}
        temp_namespace['_str_'] = self.to_utf8
        temp_namespace['_esc_'] = self.to_safe_utf8
        temp_namespace.update(kwargs)
        exec(self.compiled_code, temp_namespace)
        return temp_namespace['_template_render']()

    @staticmethod
    def write_buff_with_indent(code_buff, raw_str, indent):
        """"""
        temp = (" " * indent) + raw_str + "\n"
        code_buff.append(temp)

    @staticmethod
    def to_utf8(raw_str):
        """ 转换 """
        if isinstance(raw_str, str):
            return raw_str
        elif isinstance(raw_str, bytes):
            return raw_str.decode()
        return str(raw_str)

    @staticmethod
    def to_safe_utf8(raw_str):
        """ 过滤html转义 """
        text = TemplateCode.to_utf8(raw_str)
        return text.replace("&", "&").replace("<", "<").replace(">", ">")

class Template(object):
    """模板类"""
    def __init__(self, input_obj,filename="<string>", **namespace):
        """模板初始化"""
        self.namespace = {}
        self.namespace.update(namespace)
        # 将数据丢进去解析生成编译代码
        self.lexer = TemplateLexer(input_obj, filename)

    def render(self, **kwargs):
        """渲染模板 """
        temp_name_space = {}
        temp_name_space.update(self.namespace)
        temp_name_space.update(kwargs)
        # 执行渲染
        return self.lexer.render(**kwargs)


class TemplateLexer(object):
    """模板语法分析器 """
    def __init__(self, input_obb, filename="<string>"):
        if hasattr(input_obb, "read"):
            self.raw_string = input_obb.read()
        else:
            self.raw_string = input_obb
        self.filename = filename
        # 记录当前的位置
        self.pos = 0
        # 记录原始数据的总长度
        self.raw_str_len = len(self.raw_string)
        # 记录解析的数据
        self.code_data = TemplateCode()
        # 开始解析
        self.parse_template()

    def match(self, keyword, pos=None):
        return self.raw_string.find(keyword, pos if pos is not None else self.pos)

    def cut(self, size=-1):
        """剪取数据 size切割数据的大小，-1表示全部"""
        if size == -1:
            new_pos = self.raw_str_len
        else:
            new_pos = self.pos + size
        s = self.raw_string[self.pos: new_pos]
        self.pos = new_pos
        return s

    def remaining(self):
        """获取剩余大小 """
        return self.raw_str_len - self.pos

    def function_brace(self):
        """ 获取{{  / {% """
        skip_index = self.pos
        while True:
            index = self.match(TOKEN_S_BRACE, skip_index)  # {% {{
            # 没找到
            if index == -1:
                return None, -1
            # 末尾
            if index >= self.raw_str_len:
                return None, -1
            # 匹配类型
            next_value = self.raw_string[index + 1:index + 2]
            if next_value not in TOKEN_FLAG_SET:
                skip_index = index + 1
                # 说明不是关键类型
                continue
            brace = self.raw_string[index: index + 2]
            return brace, index
        return None, -1

    def read_content_with_token(self, index, begin_token, end_token):
        """
        读取匹配token的内容
        """
        end_index = self.match(end_token)
        if end_index == -1:
            return ParseException("{0} missing end token {1}".format(begin_token, end_token))
        # 过滤 begin_token
        self.pos = index + len(begin_token)
        content = self.cut(end_index - self.pos)
        # 去除末尾 end_token
        self.cut(len(end_token))
        return content

    def add_simple_block_statement(self, operator, suffix):
        if not suffix:
            raise ParseException("{0} missing content".format(operator))
        if operator == TOKEN_KEY_SET:
            self.code_data.append_statement(suffix)
        elif operator == TOKEN_KEY_RAW:
            self.code_data.append_express(suffix, True)
        else:
            raise ParseException("{0} is undefined".format(operator))

    def parse_template(self):
        """解析模板 """
        # TODO 检查模板文件是否更改过，如果没有则不需要重新解析
        self.code_data.reset()
        # 解析模板原文件
        self.__parse()
        # 生成编译code
        self.__compiled_code()

    def render(self, **kwargs):
        return self.code_data.generate(**kwargs)

    def __parse(self, control_operator=None, in_loop=False):
        """开始解析"""
        while True:
            if self.remaining() <= 0:
                if control_operator or in_loop:
                    raise ParseException("%s missing {%% end %%}" % control_operator)
                break
            # 读取 {{ {%
            brace, index = self.function_brace()
            # 说明没有找到
            if not brace:
                text = self.cut(index)
                self.code_data.append_text(text)
                continue
            else:
                text = self.cut(index - self.pos)
                if text:
                    self.code_data.append_text(text)

            if brace == TOKEN_EXPRESSION_L:
                content = self.read_content_with_token(index, TOKEN_EXPRESSION_L, TOKEN_EXPRESSION_R).strip()
                if not content:
                    raise ParseException("Empty Express")
                self.code_data.append_express(content)
                continue
            elif brace == TOKEN_BLOCK_L:
                content = self.read_content_with_token(index, TOKEN_BLOCK_L, TOKEN_BLOCK_R).strip()
                if not content:
                    raise ParseException("Empty block")

                # 得到表达式 for x in x ;  if x ;  elif x ;  else ;  end ;  set ;  while x ;
                operator, _, suffix = content.partition(TOKEN_SPACE)
                if not operator:
                    raise ParseException("block missing operator")

                suffix = suffix.strip()
                # 简单语句，set / raw
                if operator in TOKEN_KEY_SET_SIMPLE_EXPRESSION:
                    self.add_simple_block_statement(operator, suffix)
                elif operator in TOKEN_KEY_LOOP_CTRL:
                    if not in_loop:
                        raise ParseException("{0} must in loop block".format(operator))
                    self.code_data.append_statement(operator)
                else:
                    # 控制语句 检查匹配if 后面可以跟elif/else
                    pre_condition = TOKEN_KEY_PRE_CONDITION.get(operator, None)
                    if pre_condition:
                        # 里面就是elif/else/end
                        if control_operator not in pre_condition:
                            raise ParseException("{0} must behind with {1}".format(operator, pre_condition))
                        elif operator == TOKEN_KEY_END:
                            # 遇到{% end %}则结束
                            self.code_data.close_code()
                            return
                        else:
                            # 由于是依据if 进入 来计算elif ，因此elif与if是同级的
                            self.code_data.close_code()
                            self.code_data.append_statement(content + TOKEN_COLON)
                            self.code_data.create_code()
                            self.__parse(operator, in_loop or (operator in TOKEN_KEY_LOOP))
                            break
                    # 添加控制语句及内部语句体 if for while
                    self.code_data.append_statement(content + TOKEN_COLON)
                    self.code_data.create_code()
                    self.__parse(operator, in_loop or (operator in TOKEN_KEY_LOOP))
            else:
                raise ParseException("Unkown brace")
        return

    def __compiled_code(self):
        """生成 编译code """
        self.code_data.build_code(self.filename)


def template_html(template_name):

    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    if not os.path.exists(os.path.join(base_path, f"static/{template_name}/index.html")):
        raise ValueError(f"无法识别模板名称 {template_name} ！")

    with open(os.path.join(base_path, f"static/{template_name}/index.html"), "r", encoding="utf-8") as f:
        guessed_str = f.read()
        guessed_str = guessed_str.replace("{html_path}", os.path.join(base_path, f"static/{template_name}"))
        if not guessed_str:
            raise ValueError("无法识别文件 index.html ！")
        return guessed_str


def html_to_png(template_name, data):


    t = Template(template_html(template_name))
    html = t.render(data=data)

    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    temp_html_file = NamedTemporaryFile(mode='w', suffix='.html', encoding='utf-8')
    imgkit_config = imgkit.config(wkhtmltoimage=shutil.which("wkhtmltoimage"))
    temp_jpg_file = NamedTemporaryFile(mode='w+b', suffix='.png')
    temp_jpg_filename = temp_jpg_file.name
    temp_jpg_file.close()
    with StringIO(html) as input_file:
        try:
            temp_html_file.write(html)
            # 调用imgkit将html转为图片
            ok = imgkit.from_file(
                filename=input_file, config=imgkit_config,
                options={
                    "enable-local-file-access": "",
                    "allow": os.path.join(base_path, f"static/{template_name}"),
                    "width": 700,
                    "javascript-delay": "1000"
                },
                output_path=temp_jpg_filename
            )
            # 调用PIL将图片读取为 JPEG，RGB 格式
            img = Image.open(temp_jpg_filename, formats=['PNG']).convert('RGB')
            b = BytesIO()
            img.save(b, format="png")
            return base64.b64encode(b.getvalue()).decode()

        except Exception as e:
            logger.error("Markdown 渲染失败")



# if __name__ == "__main__":
    # data = {'音频插件': {'MusicPlugin': '点歌系统（网易云）'}, 'BOT管理插件': {'DelFriendBlacklistPlugin': '移除禁用某QQ使用机器人'}, '表情包插件': {'EmoticonListPlugin': '表情包列表'}, 'ChatGpt插件': {'privateMessage': '私聊GPT回答机器人'}, 'QQ群提示插件': {'DelGroupExitPlugin': '关闭退群提醒'}, '帮助插件': {'ListPlugin': '插件列表'}, '图片插件': {'ImageVariationPlugin': '图片放大/缩小'}, '网络插件': {'PingHostPlugin': 'Ping域名'}, '娱乐插件': {'AnimeWallpapersPlugin': '舔狗日记'}, '塔罗牌插件': {'TarotFormationPlugin': '塔罗牌阵'}, '视频插件': {'VideoPlugin': '视频搜索(支持动漫、电影)'}}
    # print(html_to_png("help", data))
