# @Author: eilianxiao
# @Date: Mar 24 21:35 2021

GRAD = 256 / 6  # 256 色值 6 等份，ANSI 公式使用
COLS = 180  # 生成字符图片列数：每行字符数
SCALE = 0.43  # 字符 宽/长 的比值，用于校正生成图的长宽
TIMEOUT = 15  # seconds

# 代表灰度递减到字符
DEFAULT_GSCALES = {
    "pixel": "█",
    "dragon": "龍",
    "emoji": "　　🙂🙄😳😋😘😛😝😜😍😅😥🤣😂😨😭😎",
    "simple": " ·:-=+*#%@",
    "morelevels": r""" .'`^",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$""",
}
