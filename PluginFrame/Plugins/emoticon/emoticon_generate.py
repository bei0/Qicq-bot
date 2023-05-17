from aiocqhttp import MessageSegment

from PluginFrame.Plugins import BaseComponentPlugin
from PluginFrame.plugins_conf import registration_directive
from utils.html_to_image import html_to_png
from utils.text_to_img import to_image

sj = {
    '看这个': {'url': 'http://api.caonm.net/api/txmb/5.php?qq=', 'liang': 0},
    '抱': {'url': 'https://api.xingzhige.com/API/baororo/?qq=', 'liang': 0},
    '咬': {'url': 'https://api.xingzhige.com/API/bite/?qq=', 'liang': 0},
    '登记': {'url': 'http://bh.ayud.top/img/jh.php?qq=', 'liang': 0},
    '吞': {'url': 'https://bg.suol.cc/API/chi/?uin=', 'liang': 0},
    '顶一顶': {'url': 'http://bg.suol.cc/API/ding/?uin=', 'liang': 0},
    '拍': {'url': 'https://api.xingzhige.com/API/paigua/?qq=', 'liang': 0},
    '抓': {'url': 'https://api.xingzhige.com/API/grab/?qq=', 'liang': 0},
    '顶': {'url': 'https://api.xingzhige.com/API/dingqiu/?qq=', 'liang': 0},
    '一起笑': {'url': 'https://api.xingzhige.com/API/LaughTogether/?qq=', 'liang': 0},
    '搂': {'url': 'https://api.xingzhige.com/API/FortuneCat/?qq=', 'liang': 0},
    '摇摇': {'url': 'https://api.xingzhige.com/API/DanceChickenLeg/?qq=', 'liang': 0},
    '打拳': {'url': 'https://api.andeer.top/API/gif_beat.php?qq=', 'liang': 0},
    '捣': {'url': 'https://api.xingzhige.com/API/pound/?qq=', 'liang': 0},
    '撕': {'url': 'http://api.caonm.net/api/sit/s.php?qq=', 'liang': 0},
    '加框': {'url': 'http://ovooa.caonm.net/API/head/?QQ=', 'liang': 0},
    '小马赞': {'url': 'http://ovooa.caonm.net/API/zan/api.php?QQ=', 'liang': 0},
    '丢': {'url': 'http://ovooa.caonm.net/API/diu/api.php?QQ=', 'liang': 0},
    '遗照': {'url': 'http://lkaa.top/API/yi/?QQ=', 'liang': 0},
    '牵': {'url': 'http://api.tangdouz.com/wz/qian.php?q=', 'liang': 1},
    '坏': {'url': 'http://api.tangdouz.com/wz/py.php?q=', 'liang': 0},
    '鄙视': {'url': 'http://xiaobai.klizi.cn/API/ce/bishi.php?qq=', 'liang': 0},
    '捶': {'url': 'http://xiaobai.klizi.cn/API/gif/hammer.php?qq=', 'liang': 0},
    '报时': {'url': 'http://xiaobai.klizi.cn/API/ce/msg.php?qq=', 'liang': 0},
    '忘了他': {'url': 'http://api.caonm.net/api/shoux/h.php?qq=', 'liang': 0},
    '儿子': {'url': 'http://api.caonm.net/api/wrz/r.php?qq=', 'liang': 0},
    '拒绝': {'url': 'http://api.caonm.net/api/wjj/j.php?qq=', 'liang': 0},
    '原谅': {'url': 'http://api.caonm.net/api/lmz/l.php?qq=', 'liang': 0},
    '我老婆': {'url': 'http://api.caonm.net/api/nmy/n.php?qq=', 'liang': 0},
    '女儿': {'url': 'http://api.caonm.net/api/wnr/n.php?qq=', 'liang': 0},
    '让你': {'url': 'http://api.caonm.net/api/bgz/g.php?qq=', 'liang': 0},
    '广告牌': {'url': 'http://api.caonm.net/api/dal/l.php?qq=', 'liang': 0},
    '耍帅': {'url': 'http://api.caonm.net/api/zhua/h.php?qq=', 'liang': 0},
    '黑化': {'url': 'http://api.caonm.net/api/whh/h.php?qq=', 'liang': 0},
    '脆弱': {'url': 'http://api.caonm.net/api/cuir/c.php?qq=', 'liang': 0},
    '寄': {'url': 'http://api.caonm.net/api/jim/j.php?qq=', 'liang': 0},
    '坤投篮': {'url': 'http://api.caonm.net/api/kunk/k.php?qq=', 'liang': 0},
    '安妮亚': {'url': 'http://api.caonm.net/api/any/any.php?qq=', 'liang': 0},
    '估价': {'url': 'http://api.caonm.net/api/qgj/index.php?qq=', 'liang': 0},
    '心碎': {'url': 'http://api.caonm.net/api/xins/x.php?qq=', 'liang': 0},
    '最帅': {'url': 'http://api.caonm.net/api/zuis/z.php?qq=', 'liang': 0},
    '嫁我': {'url': 'http://api.caonm.net/api/qiuh/q.php?qq=', 'liang': 0},
    'okk': {'url': 'http://api.caonm.net/api/okk/k.php?qq=', 'liang': 0},
    '勾引': {'url': 'http://api.caonm.net/api/gouy/g.php?qq=', 'liang': 0},
    '比心': {'url': 'http://api.caonm.net/api/bix/b.php?qq=', 'liang': 0},
    '跟我处对象': {'url': 'http://api.caonm.net/api/xie/x.php?qq=', 'liang': 0},
    '圈钱跑路': {'url': 'http://api.caonm.net/api/pao/p.php?qq=', 'liang': 0},
    '膜拜': {'url': 'http://ovooa.caonm.net/API/face_worship/?QQ=', 'liang': 0},
    '摸': {'url': 'http://ovooa.caonm.net/API/face_petpet/?QQ=', 'liang': 0},
    '幻想': {'url': 'http://api.caonm.net/api/x_3/x.php?qq=', 'liang': 0},
    '吃掉': {'url': 'http://ovooa.caonm.net/API/face_bite/?QQ=', 'liang': 0},
    '什么东西': {'url': 'http://api.caonm.net/api/peng/p.php?qq=', 'liang': 0},
    '2吃': {'url': 'http://api.caonm.net/api/bgz/g.php?qq=', 'liang': 0},
    '咀嚼': {'url': 'http://api.caonm.net/api/chi/e.php?qq=', 'liang': 0},
    '来一下': {'url': 'http://api.caonm.net/api/pdl/c.php?qq=', 'liang': 0},
    '平板': {'url': 'http://api.caonm.net/api/wyx/p2.php?qq=', 'liang': 0},
    '玩游戏': {'url': 'http://api.caonm.net/api/wyx/p.php?qq=', 'liang': 0},
    '拿着': {'url': 'http://api.caonm.net/api/kan/kan_3.php?qq=', 'liang': 0},
    '2举': {'url': 'http://api.caonm.net/api/kan/kan_4.php?qq=', 'liang': 0},
    '3举': {'url': 'http://api.caonm.net/api/kan/kan_5.php?qq=', 'liang': 0},
    '叽': {'url': 'http://api.caonm.net/api/kan/kan_6.php?qq=', 'liang': 0},
    '道歉': {'url': 'http://api.caonm.net/api/kan/kan_8.php?qq=', 'liang': 0},
    '手机': {'url': 'http://api.caonm.net/api/kan/kan_9.php?qq=', 'liang': 0},
    '4举': {'url': 'http://h.xiaocha.fun/api/ju.php?qq=', 'liang': 0},
    '拿牌': {'url': 'http://api.caonm.net/api/kan/kan.php?qq=', 'liang': 0},
    '警察': {'url': 'http://api.caonm.net/api/jcz2/p.php?qq=', 'liang': 0},
    '警官': {'url': 'http://api.caonm.net/api/jcz/index.php?qq=', 'liang': 0},
    '嘴': {'url': 'http://api.caonm.net/api/jiujiu/jiujiu.php?qq=', 'liang': 0},
    '舔': {'url': 'http://api.caonm.net/api/tn/t.php?qq=', 'liang': 0},
    '遮脸': {'url': 'http://api.caonm.net/api/huanl/h.php?qq=', 'liang': 0},
    '疑问': {'url': 'http://api.caonm.net/api/mb/wh.php?qq=', 'liang': 0},
    '上电视': {'url': 'http://api.caonm.net/api/kds/k.php?qq=', 'liang': 0},
    '这像画吗': {'url': 'http://api.caonm.net/api/hua/h.php?qq=', 'liang': 0},
    '垃圾': {'url': 'http://api.caonm.net/api/ljt/l.php?qq=', 'liang': 0},
    '为什么艾特我': {'url': 'http://api.caonm.net/api/why/at.php?qq=', 'liang': 0},
    '墙纸': {'url': 'http://api.caonm.net/api/bz/w.php?qq=', 'liang': 0},
    '求婚': {'url': 'http://ovooa.caonm.net/API/face_propose/?QQ=', 'liang': 0},
    '感动哭了': {'url': 'http://ovooa.caonm.net/API/face_touch/?QQ=', 'liang': 0},
    '高质量': {'url': 'http://ovooa.caonm.net/API/face_gao/?QQ=', 'liang': 0},
    '咸鱼': {'url': 'http://ovooa.caonm.net/API/face_yu/?QQ=', 'liang': 0},
    '快逃': {'url': 'http://xiaobai.klizi.cn/API/gif/escape.php?qq=', 'liang': 0},
    '要钱钱': {'url': 'http://api.caonm.net/api/wyqq/q.php?qq=', 'liang': 0},
    '瑟瑟': {'url': 'https://xiaobai.klizi.cn/API/gif/erotic.php?qq=', 'liang': 0},
    '随机证书': {'url': 'https://xiaobai.klizi.cn/API/ce/zs.php?qq=', 'liang': 0},
    '滚出': {'url': 'http://api.caonm.net/api/gun/index.php?qq=', 'liang': 0},
    '羡慕': {'url': 'http://api.wqwlkj.cn/wqwlapi/xianmu.php?qq=', 'liang': 0},
    '摸狗狗': {'url': 'http://api.caonm.net/api/wus/w.php?qq=', 'liang': 0},
    '网络公主': {'url': 'http://api.caonm.net/api/yyy/y.php?qq=', 'liang': 0},
    '删库': {'url': 'http://h.xiaocha.fun/api/pao.php?qq=', 'liang': 0},
    '看电视': {'url': 'http://h.xiaocha.fun/api/kan.php?qq=', 'liang': 0},
    '美女抬': {'url': 'http://h.xiaocha.fun/api/tai.php?qq=', 'liang': 0},
    '难办': {'url': 'http://h.xiaocha.fun/api/ban.php?qq=', 'liang': 0},
    '女拿': {'url': 'http://h.xiaocha.fun/api/na.php?qq=', 'liang': 0},
    '拍死你': {'url': 'http://h.xiaocha.fun/api/pai.php?qq=', 'liang': 0},
    '快溜': {'url': 'http://h.xiaocha.fun/api/liu/liu.php?QQ=', 'liang': 0},
    '怒': {'url': 'http://h.xiaocha.fun/api/nu/nu.php?QQ=', 'liang': 0},
    '不想上学': {'url': 'http://h.xiaocha.fun/api/xue/xue.php?QQ=', 'liang': 0},
    '露脸': {'url': 'http://h.xiaocha.fun/api/lou/lou.php?QQ=', 'liang': 0},
    '滑稽捶': {'url': 'http://h.xiaocha.fun/api/chui/chui.php?QQ=', 'liang': 0},
    '咬2': {'url': 'http://h.xiaocha.fun/api/yao/yao.php?QQ=', 'liang': 0},
    '心碎2': {'url': 'http://h.xiaocha.fun/api/sui/sui.php?QQ=', 'liang': 0},
    '乡下人': {'url': 'http://api.caonm.net/api/txmb/6.php?qq=', 'liang': 0},
    '灵动岛': {'url': 'http://api.caonm.net/api/txmb/3.php?qq=', 'liang': 0},
    '流汗': {'url': 'http://api.caonm.net/api/txmb/1.php?qq=', 'liang': 0},
    '纱雾举牌': {'url': 'http://api.caonm.net/api/wus/w.php?qq=', 'liang': 0},
    '整一个': {'url': 'http://apicaonm.net/api/zyg/gei.php?qq=', 'liang': 0},
    '老干妈': {'url': 'http://api.caonm.net/api/lgm/index.php?qq=', 'liang': 0},
    '拿手机': {'url': 'http://h.xiaocha.fun/api/sj.php?qq=', 'liang': 0},
    '我的人': {'url': 'http://h.xiaocha.fun/api/wode.php?qq=', 'liang': 0},
    '喝饮料': {'url': 'http://h.xiaocha.fun/api/xi.php?qq=', 'liang': 0},
    '看淡了': {'url': 'http://h.xiaocha.fun/api/dan.php?qq=', 'liang': 0},
    '坤证': {'url': 'http://api.caonm.net/api/txmb/7.php?qq=', 'liang': 0},
    '懒羊羊': {'url': 'http://api.caonm.net/api/lyy/l.php?qq=', 'liang': 0},
    '摇摆': {'url': 'http://api.caonm.net/api/ajl/y.php?qq=', 'liang': 0},
    '颜色': {'url': 'http://api.caonm.net/api/sjbc/y.php?qq=', 'liang': 0},
    '走路': {'url': 'http://api.caonm.net/api/zoul/y.php?qq=', 'liang': 0},
    '女装协议': {'url': 'http://api.caonm.net/api/jqxy/n.php?qq=', 'liang': 0},
    '进群协议': {'url': 'http://api.caonm.net/api/jqxy/j.php?qq=', 'liang': 0},
    '亲亲': {'url': 'http://api.caonm.net/api/ddqq/y.php?qq=', 'liang': 0},
    '按下': {'url': 'http://api.caonm.net/api/anniu/a.php?qq=', 'liang': 0},
    '50': {'url': 'http://api.caonm.net/api/v50/b.php?qq=', 'liang': 0},
    '涩图': {'url': 'http://api.caonm.net/api/mstl/s.php?qq=', 'liang': 0},
    '杜蕾斯': {'url': 'http://api.caonm.net/api/byt/b.php?qq=', 'liang': 0},
    '打篮球': {'url': 'http://www.xiaoqiandtianyi.tk/api/cxk.php?QQ=', 'liang': 0},
    '挥拳': {'url': 'http://api.caonm.net/api/hq/chui.php?qq=', 'liang': 0},
    '写代码': {'url': 'http://api.wqwlkj.cn/wqwlapi/jwxdm.php?qq=', 'liang': 0},
    '安排': {'url': 'http://api.wqwlkj.cn/wqwlapi/anpai.php?qq=', 'liang': 0},
    '萌新一个': {'url': 'http://api.wqwlkj.cn/wqwlapi/wsmx.php?qq=', 'liang': 0},
    '差评': {'url': 'http://api.wqwlkj.cn/wqwlapi/cp.php?qq=', 'liang': 0},
    '好评': {'url': 'http://api.wqwlkj.cn/wqwlapi/hp.php?qq=', 'liang': 0},
    '坤举旗': {'url': 'http://api.wqwlkj.cn/wqwlapi/kunjuqi.php?qq=', 'liang': 0},
    '开始摆烂': {'url': 'http://api.luanmo.top/API/tu_bailan?qq=', 'liang': 0},
    '保护': {'url': 'http://api.luanmo.top/API/tu_dog2?qq=', 'liang': 0},
    '地图头像': {'url': 'http://api.wqwlkj.cn/wqwlapi/zgdt.php?qq=', 'liang': 0},
    '小c酱': {'url': 'http://api.caonm.net/api/xc/index.php?', 'liang': 0},
    'mc酱': {'url': 'http://api.caonm.net/api/mc/index.php?', 'liang': 0},
    '兽猫酱': {'url': 'http://api.caonm.net/api/smj/index.php?', 'liang': 0},
    '柴郡': {'url': 'http://api.caonm.net/api/chai/c.php?', 'liang': 0},
    'ikun': {'url': 'http://api.caonm.net/api/kun/k.php?', 'liang': 0},
    '龙图': {'url': 'http://api.caonm.net/api/long/l.php?', 'liang': 0},
    '变魔术': {'url': 'http://api.caonm.net/api/tax/y.php?qq=', 'liang': 0},
    '结婚': {'url': 'https://api.caonm.net/api/jhzz/j.php?qq=', 'liang': 2},
    '两只猫': {'url': 'https://api.caonm.net/api/xmmz/y.php?qq=', 'liang': 0},
    '煮': {'url': 'https://api.caonm.net/api/huos/y.php?qq=', 'liang': 0},
    '画画': {'url': 'https://api.caonm.net/api/huaa/h.php?qq=', 'liang': 0},
    '打鸡蛋': {'url': 'https://api.caonm.net/api/chaof/y.php?qq=', 'liang': 0},
    '2舔': {'url': 'https://api.caonm.net/api/chixg/y.php?qq=', 'liang': 0},
    '枕头': {'url': 'https://api.caonm.net/api/zhent/y.php?qq=', 'liang': 0},
    'IKUN': {'url': 'http://api.caonm.net/api/ikz/i.php?qq=', 'liang': 0},
    '滚': {'url': 'http://api.caonm.net/api/gund/g.php?qq=', 'liang': 0},
    '注意身份': {'url': 'http://api.caonm.net/api/zynsf/z.php?qq=', 'liang': 0},
    '翻画板': {'url': 'http://api.caonm.net/api/dakai/a.php?qq=', 'liang': 0},
    '街舞': {'url': 'https://api.caonm.net/api/tmcw/y.php?qq=', 'liang': 0},
    '蹭': {'url': 'https://api.caonm.net/api/cence/y.php?qq=', 'liang': 0},
    '2拍': {'url': 'https://api.caonm.net/api/paid/y.php?qq=', 'liang': 0},
    '装高手': {'url': 'http://www.xiaoqiandtianyi.tk/api/z.php?qq=', 'liang': 0},
    '追': {'url': 'https://api.caonm.net/api/zhuid/y.php?qq=', 'liang': 0},
    '2敲': {'url': 'https://api.caonm.net/api/qiaod/y.php?qq=', 'liang': 0},
    '上吊': {'url': 'https://api.caonm.net/api/shangd/y.php?qq=', 'liang': 0},
    '跳舞': {'url': 'http://api.caonm.net/api/tiaow/y.php?qq=', 'liang': 0},
    '诈尸': {'url': 'http://api.caonm.net/api/zhas/y.php?qq=', 'liang': 0},
    '踢球': {'url': 'https://api.caonm.net/api/tiqiu/y.php?qq=', 'liang': 0},
    '骗子': {'url': 'https://api.caonm.net/api/pianzi/c.php?qq=', 'liang': 0},
    '导管': {'url': 'https://api.caonm.net/api/daoguan/c.php?qq=', 'liang': 0},
    '强行瑟瑟': {'url': 'https://api.caonm.net/api/kapian/c.php?qq=', 'liang': 0},
    '我牛子呢': {'url': 'https://api.caonm.net/api/kapian/c2.php?qq=', 'liang': 0},
    '恶魔': {'url': 'https://api.caonm.net/api/kapian/c3.php?qq=', 'liang': 0},
    '演员': {'url': 'https://api.caonm.net/api/madou/c2.php?qq=', 'liang': 0},
    '狗呢': {'url': 'https://api.caonm.net/api/asc/c.php?qq=', 'liang': 0},
    '不幸': {'url': 'https://api.caonm.net/api/asc/c2.php?qq=', 'liang': 0},
    '老实点': {'url': 'https://api.caonm.net/api/asc/c3.php?qq=', 'liang': 0},
    '动漫画画': {'url': 'https://api.caonm.net/api/asc/c4.php?qq=', 'liang': 0},
    '木鱼': {'url': 'https://api.caonm.net/api/muyu/y.php?qq=', 'liang': 0},
    '金钱攻击': {'url': 'https://api.caonm.net/api/jingq/y.php?qq=', 'liang': 0},
    '安全感': {'url': 'http://api.caonm.net/api/anqg/c.php?qq=', 'liang': 0},
    '陪睡券': {'url': 'https://api.caonm.net/api/asc/c5.php?qq=', 'liang': 0},
    '男同': {'url': 'https://api.caonm.net/api/asc/c6.php?qq=', 'liang': 0},
    '掀墙纸': {'url': 'https://api.andeer.top/API/gif_wallpaper.php?qq=', 'liang': 0},
    '胡桃咬': {'url': 'https://api.andeer.top/API/gif_hutao_bite.php?qq=', 'liang': 0},
    '可莉吃': {'url': 'https://api.andeer.top/API/gif_klee_eat.php?qq=', 'liang': 0},
    '崇拜': {'url': 'https://api.andeer.top/API/gif_worship.php?qq=', 'liang': 0},
    '嘎达': {'url': 'https://api.andeer.top/API/img_tr.php?qq=', 'liang': 0},
    '要亲亲': {'url': 'https://api.andeer.top/API/img_kiss_1.php?qq=', 'liang': 0},
    '宝可梦': {'url': 'https://api.andeer.top/API/img_pokemon.php?qq=', 'liang': 0},
    '可爱': {'url': 'https://api.andeer.top/API/img_cute.php?qq=', 'liang': 0},
    '蒙娜丽莎': {'url': 'https://api.andeer.top/API/img_mnls.php?qq=', 'liang': 0},
    '精神涣散': {'url': 'https://api.andeer.top/API/no_attention.php?qq=', 'liang': 0},
    '贴贴': {'url': 'https://api.andeer.top/API/img_kiss1.php?bqq=', 'liang': 3},
    '击剑': {'url': 'https://api.andeer.top/API/gif_beat_j.php?bqq=', 'liang': 3},
    '过来洗头': {'url': 'https://api.andeer.top/API/moca.php?bqq=', 'liang': 3},
    '正在加载': {'url': 'https://api.andeer.top/API/img_loading.php?qq=', 'liang': 0},
    '体操服': {'url': 'http://api.caonm.net/api/jupai/m.php?qq=', 'liang': 0},
    '技能': {'url': 'http://api.caonm.net/api/jineng/y.php?qq=', 'liang': 0},
    'GKD': {'url': 'http://api.caonm.net/api/kapian/c5.php?qq=', 'liang': 0},
    '无法瑟瑟': {'url': 'http://api.caonm.net/api/kapian/c4.php?qq=', 'liang': 0},
    '目录': {'url': 'http://api.caonm.net/api/asc/c9.php?qq=', 'liang': 0},
    '床上一躺': {'url': 'http://api.caonm.net/api/asc/c8.php?qq=', 'liang': 0},
    '啊！': {'url': 'http://api.caonm.net/api/asc/c7.php?qq=', 'liang': 0},
    '包夜': {'url': 'http://api.caonm.net/api/guoy/g.php?qq=', 'liang': 0},
    '报警了': {'url': 'http://api.caonm.net/api/baon/1.php?qq=', 'liang': 0},
    '超市': {'url': 'http://api.caonm.net/api/chaop/j.php?qq=', 'liang': 2},
    '星期四': {'url': 'http://api.caonm.net/api/kfc/50.php?qq=', 'liang': 0},
    '女同': {'url': 'http://api.caonm.net/api/asc/c66.php?qq=', 'liang': 0},
    '芙蓉王': {'url': 'http://api.caonm.net/api/yan/y.php?qq=', 'liang': 0},
    '望远镜': {'url': 'https://api.caonm.net/api/wyj/w.php?qq=', 'liang': 0},
    '完美': {'url': 'http://api.caonm.net/api/meiyou/c.php?qq=', 'liang': 0},
    '汤姆猫': {'url': 'http://api.caonm.net/api/tmgx/y.php?qq=', 'liang': 0},
    '一脚': {'url': 'http://api.caonm.net/api/zjyj/y.php?qq1=', 'liang': 2},
    '大哭': {'url': 'http://api.caonm.net/api/txmb/8.php?qq=', 'liang': 0},
    '情侣': {'url': 'http://api.caonm.net/api/mxbc/m.php?qq=', 'liang': 0},
    '名片': {'url': 'http://api.caonm.net/api/tp/m.php?qq=', 'liang': 0},
    '美女抱': {'url': 'http://api.caonm.net/api/jupai/d.php?qq=', 'liang': 0}
}


@registration_directive(matching=r'(.*)\[CQ:at,qq=(\d+)\]( |)', message_types=("group", ))
class EmoticonPlugin(BaseComponentPlugin):
    __name__ = 'EmoticonPlugin'
    plu_name = '表情包插件'
    desc = "QQ表情包生成"
    docs = '表情包名称[@群友]'
    permissions = ("all",)

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        re_obj = message_parameter.get("re_obj")
        emo_type, at_qq, _ = re_obj.groups()

        sj_info = sj.get(emo_type)
        if not sj_info:
            return

        mo_url = sj_info.get("url")
        liang = sj_info.get("liang")
        if liang == 1:
            url = mo_url+str(event.user_id)+f"&qq={str(at_qq).strip()}"
        elif liang == 2:
            url = mo_url+str(event.user_id)+f"&qq2={str(at_qq).strip()}"
        elif liang == 3:
            url = mo_url + str(event.user_id) + f"&cqq={str(at_qq).strip()}"
        else:
            url = mo_url + str(at_qq).strip()

        resp = MessageSegment.image(url)
        return await bot.send(event, resp)


@registration_directive(matching=r'#表情包列表', message_types=("group", ))
class EmoticonListPlugin(BaseComponentPlugin):
    __name__ = 'EmoticonListPlugin'
    plu_name = '表情包插件'
    desc = "表情包列表"
    docs = '#表情包列表'
    permissions = ("all",)

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        image_base61 = html_to_png("emoticon", sj)
        resp = MessageSegment.image(f"base64://{image_base61}")
        await bot.send(event, resp)
