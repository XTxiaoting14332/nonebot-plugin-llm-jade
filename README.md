<div align="center">
  <a href="https://nonebot.dev/store/plugins/"><img src="image/logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
<div align="center">

# nonebot-plugin-llm-jade
</div>
_✨ 基于 LLM 的玉检测插件 ✨_<br>


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/XTxiaoting14332/nonebot-plugin-llm-jade.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-llm-jade">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-llm-jade.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>



## 📖 介绍

基于 LLM 的玉检测插件，使用智谱API<br>
使用智谱的 `GLM-4V-Flash` 进行检测，不消耗api余额


## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令安装

    nb plugin install nonebot-plugin-llm-jade

</details>

<details>
<summary>pip安装</summary>

    pip install nonebot-plugin-llm-jade

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_llm_jade"]
</details>
<details>
<summary>Github下载</summary>

手动克隆本仓库或直接下载压缩包，将里面的 `nonebot_plugin_llm_jade` 文件夹复制到 `src/plugins` 中,并安装以下依赖

    httpx  PyJWT

</details>


</details><br>


## 🔧配置项
### 必填项

```
#智谱清言的API Key
jadefoot_token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

启用的群聊
jadefoot_group = ["123456789","987654321"]
```

### 非必填项

```
#触发的概率（默认为0.5）
jadefoot_probability = 0.5

```

## 🖼️ 使用效果图

![image](./img/img.webp)