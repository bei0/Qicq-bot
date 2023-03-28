from cqhttp import ApiField


class CqBotAccountConfig:
    set_qq_profile = ApiField("设置登录号资料", "set_qq_profile")
    get_login_info = ApiField("获取登录号信息", "get_login_info")
    qidian_get_account_info = ApiField("获取企点账号信息", "qidian_get_account_info")
    get_model_show = ApiField("获取在线机型", "_get_model_show")
    set_model_show = ApiField("设置在线机型", "_set_model_show")
    get_online_clients = ApiField("获取当前账号在线客户端列表", "get_online_clients")


class CqFriendInfoConfig:
    set_qq_profile = ApiField("获取陌生人信息", "get_stranger_info")
    get_friend_list = ApiField("获取好友列表", "get_friend_list")
    get_unidirectional_friend_list = ApiField("获取单向好友列表", "get_unidirectional_friend_list")


class CqFriendOperateConfig:
    delete_friend = ApiField("删除好友", "delete_friend")
    delete_unidirectional_friend = ApiField("删除单向好友", "delete_unidirectional_friend")
    set_friend_add_request = ApiField("处理加好友请求", "set_friend_add_request")
    set_group_add_request = ApiField("处理加群请求／邀请", "set_group_add_request")


class CqMessageConfig:
    send_private_msg = ApiField("发送私聊消息", "send_private_msg")
    send_group_msg = ApiField("发送群聊消息", "send_group_msg")
    send_msg = ApiField("发送消息", "send_msg")
    get_msg = ApiField("获取消息", "get_msg")
    delete_msg = ApiField("撤回消息", "delete_msg")
    mark_msg_as_read = ApiField("标记消息已读", "mark_msg_as_read")
    get_forward_msg = ApiField("获取合并转发内容", "get_forward_msg")
    send_group_forward_msg = ApiField("发送合并转发 ( 群聊 )", "send_group_forward_msg")
    send_private_forward_msg = ApiField("发送合并转发 ( 好友 )", "send_private_forward_msg")
    get_group_msg_history = ApiField("获取群消息历史记录", "get_group_msg_history")


class CqMultimediaConfig:
    get_image = ApiField("获取图片", "get_image")
    can_send_image = ApiField("检查是否可以发送图片", "can_send_image")
    ocr_image = ApiField("图片 OCR", "ocr_image")
    get_record = ApiField("获取语音", "get_record")
    can_send_record = ApiField("检查是否可以发送语音", "can_send_record")


class CqGroupIndoConfig:
    get_group_info = ApiField("获取群信息", "get_group_info")
    get_group_list = ApiField("获取群列表", "get_group_list")
    get_group_member_info = ApiField("获取群成员信息", "get_group_member_info")
    get_group_member_list = ApiField("获取群成员列表", "get_group_member_list")
    get_group_honor_info = ApiField("获取群荣誉信息", "get_group_honor_info")
    get_group_system_msg = ApiField("获取群系统消息", "get_group_system_msg")
    get_essence_msg_list = ApiField("获取精华消息列表", "get_essence_msg_list")
    get_group_at_all_remain = ApiField("获取群 @全体成员 剩余次数", "get_group_at_all_remain")


class CqGroupSettingsConfig:
    set_group_name = ApiField("设置群名", "set_group_name")
    set_group_portrait = ApiField("设置群头像", "set_group_portrait")
    set_group_admin = ApiField("设置群管理员", "set_group_admin")
    set_group_card = ApiField("设置群名片 ( 群备注 )", "set_group_card")
    set_group_special_title = ApiField("设置群组专属头衔", "set_group_special_title")


class CqGroupOperateConfig:
    set_group_ban = ApiField("群单人禁言", "set_group_ban")
    set_group_whole_ban = ApiField("群全员禁言", "set_group_whole_ban")
    set_group_anonymous_ban = ApiField("群匿名用户禁言", "set_group_anonymous_ban")
    set_essence_msg = ApiField("设置精华消息", "set_essence_msg")
    delete_essence_msg = ApiField("移出精华消息", "delete_essence_msg")
    send_group_sign = ApiField("群打卡", "send_group_sign")
    set_group_anonymous = ApiField("群设置匿名", "set_group_anonymous")
    send_group_notice = ApiField("发送群公告", "_send_group_notice")
    get_group_notice = ApiField("发送群公告", "_get_group_notice")
    set_group_kick = ApiField("群组踢人", "set_group_kick")
    set_group_leave = ApiField("退出群组", "set_group_leave")


class CQApiConfig:
    account = CqBotAccountConfig()  # 账号相关
    friend_info = CqFriendInfoConfig()  # 好友信息相关
    friend_operate = CqFriendOperateConfig()    # 好友操作
    message = CqMessageConfig()     # 消息相关
    multimedia = CqMultimediaConfig()   # 多媒体相关
    group_info = CqGroupIndoConfig()    # 群信息相关
    group_settings = CqGroupSettingsConfig()    # 群设置
    group_operate = CqGroupOperateConfig()  # 群操作
