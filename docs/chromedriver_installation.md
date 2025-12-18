# Chromedriver 安装

Chromedriver 是 Google 提供的用于控制 Chrome 浏览器的驱动程序。所以你需要先安装 Chrome 浏览器，然后下载对应的 Chromedriver 版本。

## 1. 安装 Chrome 浏览器

Win和Mac都非常容易安装。我们主要介绍Ubuntu上的安装方法：

```bash
sudo apt update
sudo apt install libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb    # Might show "errors", fixed by next line
sudo apt install -f
google-chrome --version      # 查看版本
```

## 2. 安装 Chromedriver

### 自动安装

我们提供了一个自动安装脚本，你可以直接运行它来安装 Chromedriver。

> 注意：自动安装脚本需要配置代理才能正常工作。如果你的网络环境需要代理，请先配置好代理。否则采用后面手动安装的方法。

```bash
python3 scripts/auto_install_chromedriver.py --dest driver/
```

### 手动安装

通过前面的`google-chrome --version`命令查看 Chrome 浏览器的版本号，例如`126.0.6478.126`。然后根据版本号执行以下命令：

```bash
mkdir driver/
cd driver/

# 下载对应版本的 Chromedriver，注意替换版本号
wget https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip

unzip chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver ./
sudo chmod 777 chromedriver
rm -r chromedriver-linux64 chromedriver-linux64.zip
```

## 3. 测试 Chromedriver

安装完成后，你可以测试一下 Chromedriver 是否正常工作。执行以下命令：

```bash
python3 scripts/test_driver.py --driver driver/chromedriver --url https://www.baidu.com
```
