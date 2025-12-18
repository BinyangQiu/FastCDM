import argparse
import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def parse_args():
    parser = argparse.ArgumentParser(
        prog="test_driver",
        description="测试指定 ChromeDriver 是否可用，并检查页面访问是否正常。",
    )
    parser.add_argument(
        "--driver",
        type=str,
        required=True,
        help="ChromeDriver 可执行文件路径。",
    )
    parser.add_argument(
        "--url",
        type=str,
        default="https://www.baidu.com",
        help="用于测试的目标 URL，默认 https://www.baidu.com。",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    driver_path = Path(args.driver)

    if not driver_path.exists():
        print(f"不通过：ChromeDriver 路径不存在：{driver_path}")
        sys.exit(1)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    try:
        client = webdriver.Chrome(
            options=chrome_options, service=Service(str(driver_path))
        )
    except Exception as e:
        print(f"不通过：初始化 WebDriver 失败：{e}")
        sys.exit(1)

    try:
        client.get(args.url)
        print("通过：成功访问页面，视为返回 200。")
        sys.exit(0)
    except Exception as e:
        print(f"不通过：页面请求失败：{e}")
        sys.exit(1)
    finally:
        try:
            client.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
