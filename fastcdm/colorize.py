import colorsys
import re
import sys
from typing import List, Tuple
from fastcdm.latex_processor import normalize_latex, token_add_color_RGB


def generate_high_contrast_colors(num_colors: int) -> List[Tuple[int, int, int]]:
    """
    使用 HSV 颜色空间生成一系列高对比度、视觉上易于区分的颜色。
    """
    colors_rgb = []
    golden_ratio_conjugate = 0.61803398875
    hue = 0.5
    for _ in range(num_colors):
        hue += golden_ratio_conjugate
        hue %= 1
        rgb_float = colorsys.hsv_to_rgb(hue, 0.9, 0.95)
        rgb_int = tuple(int(c * 255) for c in rgb_float)
        colors_rgb.append(rgb_int)
    return colors_rgb


def process_for_katex(pre_tokenized_latex: str) -> Tuple[str, List[str]]:

    if not pre_tokenized_latex or not isinstance(pre_tokenized_latex, str):
        return "", []

    try:
        normalized_latex = normalize_latex(pre_tokenized_latex)
        l_split = [token for token in normalized_latex.strip().split(" ") if token]

        idx = 0
        token_list = []
        temp_l_split = list(l_split)

        while idx < len(temp_l_split):
            temp_l_split, idx, token_list = token_add_color_RGB(
                temp_l_split, idx, token_list
            )

        colored_template_original = " ".join(temp_l_split)
        katex_template = re.sub(
            r"\\mathcolor\[RGB\]{<color_(\d+)>}",
            r"\\color{__COLOR__\1__}",
            colored_template_original,
        )
        return katex_template, token_list

    except Exception as e:
        print(f"\n在 KaTeX 处理过程中出错: {e}", file=sys.stderr)
        print(f"有问题的 LaTeX 字符串: {pre_tokenized_latex}", file=sys.stderr)
        return "[PROCESSING FAILED]", []
