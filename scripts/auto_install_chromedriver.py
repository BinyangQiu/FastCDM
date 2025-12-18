#!/usr/bin/env python3
import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Optional

from webdriver_manager.chrome import ChromeDriverManager


def resolve_target_path(dest: str) -> Path:
    p = Path(dest)
    if p.exists() and p.is_dir():
        name = "chromedriver.exe" if sys.platform.startswith("win") else "chromedriver"
        return p / name
    if dest.endswith(os.sep):
        name = "chromedriver.exe" if sys.platform.startswith("win") else "chromedriver"
        return Path(dest) / name
    return p


def install(dest: Optional[str]) -> Path:
    print(
        "[提示] ChromeDriverManager 下载可能需要代理。如果失败，请查看 docs/chromedriver_installation.md 以手动安装。"
    )
    src_path = ChromeDriverManager().install()
    print(f"[完成] 已下载: {src_path}")
    if dest:
        target = resolve_target_path(dest)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(src_path, target)
        try:
            mode = os.stat(target).st_mode
            os.chmod(target, mode | 0o111)
        except Exception as e:
            print(f"[警告] 设置可执行权限失败: {e}")
        print(f"[完成] 已移动到: {target}")
        return target
    else:
        print(f"[信息] 使用默认安装位置: {src_path}")
        return Path(src_path)


def main():
    parser = argparse.ArgumentParser(
        prog="auto_install_chromedriver",
        description=(
            "自动下载 ChromeDriver。可选指定目标路径，若未指定则保留在默认位置。"
        ),
    )
    parser.add_argument(
        "-d",
        "--dest",
        type=str,
        default=None,
        help="目标 chromedriver 路径或目录。可传目录或完整文件路径。",
    )
    args = parser.parse_args()
    target = install(args.dest)
    print(f"[结果] chromedriver 位置: {target}")


if __name__ == "__main__":
    main()
