# @Author: lonsty
# @Date: Mar 24 21:22 2021
from typing import List

from pathlib import Path

import numpy as np
import requests
from PIL import Image
from rich.console import Console
from urwid.util import str_util

from . import __version__
from . import settings as conf

console = Console()


def half2full(string: str) -> str:
    full_width_chars = []
    for char in string:
        num = ord(char)
        if num == 32:  # 空格
            num = 0x3000
        elif 33 <= num <= 113:
            num += 0xFEE0
        num = chr(num)
        full_width_chars.append(num)
    return "".join(full_width_chars)


def check_character_width(text: str) -> (str, int):
    new_text = text
    char_width = 1

    half_width_char, full_width_char = 0, 0
    for char in text:
        char_wid = str_util.get_width(ord(char))
        if char_wid == 1:
            half_width_char += 1
        elif char_wid == 2:
            full_width_char += 1
    if full_width_char > 0:
        new_text = half2full(text)
        char_width = 2
    return new_text, char_width


def six_level_gray(v: int) -> int:
    if v < 48:
        six_level_value = 0
    elif v < 115:
        six_level_value = 1
    elif v < 155:
        six_level_value = 2
    elif v < 195:
        six_level_value = 3
    elif v < 235:
        six_level_value = 4
    else:
        six_level_value = 5
    return six_level_value


def load_image(file: str) -> Image:
    filepath = Path(file)
    if not filepath.is_file():
        return None
    return Image.open(filepath)


def load_image_from_url(url: str) -> Image:
    try:
        resp = requests.get(url, stream=True, timeout=conf.TIMEOUT)
        resp.raise_for_status()
    except Exception:
        return None
    return Image.open(resp.raw)


def print_ansi_art(art: List[List]) -> None:
    for row in art:
        print("".join(row))
    print()


def save_ansi_art(filepath: Path, art: List[List]) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        for row in art:
            f.write("".join(row) + "\n")
    return None


def ansi_art(
    src: str,
    columns: int,
    output: Path,
    scale: float,
    grayscale: str,
    diy_grayscale: str,
    no_color: bool,
    reverse_grayscale: bool,
    reverse_color: bool,
    quiet: bool,
):
    image = load_image(src) or load_image_from_url(src)
    if not image:
        raise ValueError(f"{src} is not a file, or URL cannot be accessed")

    gscale = conf.DEFAULT_GSCALES.get(grayscale)
    if diy_grayscale:
        gscale = diy_grayscale
    if reverse_grayscale:
        gscale = gscale[::-1]
    gscale, char_width = check_character_width(gscale)
    cols = int(columns / char_width)
    gscale_len = len(gscale)

    arr = np.asarray(image, "int32")
    height, width, _ = arr.shape

    if cols > width:
        raise ValueError("the output columns cannot be greater than the width of the image")

    w = width / cols
    h = w / (scale * char_width)
    rows = int(height / h)

    if not quiet:
        console.print(f"[no]ansify {__version__} © lonsty[/]")
        console.print(f"Image Size : {width} px x {height} px")
        console.print(f"Output Size: {cols} cols x {rows} rows")
        console.print(f"Grayscale  : [[yellow]{gscale}[/]]\n")

    ansi_img = []
    for r in range(rows):
        y1 = int(h * r)
        y2 = int(h * (r + 1))
        if r == rows - 1:
            y2 = height

        ansi_img.append([])
        for c in range(cols):
            x1 = int(w * c)
            x2 = int(w * (c + 1))
            if c == cols - 1:
                x2 = width

            # 截取小块图片
            crop = np.asarray(arr[y1:y2, x1:x2], dtype="uint8")
            # 取 RGB 三通道的颜色
            rarr, garr, barr = crop[..., 0], crop[..., 1], crop[..., 2]
            # 计算小块图片的 RGB 平均值
            ravg, gavg, bavg = np.average(rarr), np.average(garr), np.average(barr)
            # 由公式计算灰度
            yavg = 0.2989 * ravg + 0.5870 * gavg + 0.1140 * bavg
            # 由灰度值取字符
            asval = gscale[int((yavg * gscale_len) / 255)]

            if no_color:
                ansi_img[r].append(asval)
            else:
                # 由公式计算 ANSI 颜色码
                if reverse_color:
                    ravg, gavg, bavg = 255 - ravg, 255 - gavg, 255 - bavg
                # color = 16 + 36 * int(ravg / conf.GRAD) + 6 * int(gavg / conf.GRAD) + int(bavg / conf.GRAD)
                color = 16 + 36 * six_level_gray(ravg) + 6 * six_level_gray(gavg) + six_level_gray(bavg)
                ansi_img[r].append(f"\033[38;5;{color}m{asval}\033[0m")

    # 输出 ANSI art
    print_ansi_art(ansi_img)

    # 保存到文件
    if output:
        save_ansi_art(output, ansi_img)
