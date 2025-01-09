from nonebot import get_plugin_config, on_message
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
import httpx
import jwt
from datetime import datetime, timedelta
import time
from .config import Config
import base64
import random
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="玉！",
    description="基于 LLM 的玉检测插件",
    usage="none",
    type="application",
    homepage="https://github.com/XTxiaoting14332/nonebot-plugin-llm-jade",
    config=Config,
    supported_adapters={"~onebot.v11"},

)

config = get_plugin_config(Config)


def generate_token(apikey: str):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("错误的apikey！", e)

    payload = {
        "api_key": id,
        "exp": datetime.utcnow() + timedelta(days=1),
        "timestamp": int(round(time.time() * 1000)),
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )


token = config.jadefoot_token

jade = on_message(priority=1, block=False)


@jade.handle()
async def handle(bot: Bot, event: GroupMessageEvent):
    for i in event.message:
        if i.type == "image":
            img_url = i.data["url"]
            logger.info(img_url)
            auth = generate_token(token)
            res = await req_glm(auth, img_url)

            # 模型拦截检查
            if is_error_response(res):
                await jade.finish("涩！", reply_message=True)
                return

            reply_map = {
                "yuzu_y": "玉！",
                "yuzu_n": "¿",
            }

            # 如果标签不在字典中，不回复，直接结束
            if res not in reply_map:
                logger.info("图片无特殊要素")
                await jade.finish()
                return

            # 判断是否符合概率条件
            if random.randint(0, 1) < config.jadefoot_probability:
                # 获取并回复对应的内容
                reply_message = reply_map.get(res)
                logger.info(f"够 {reply_message}")
                await jade.finish(reply_message, reply_message=True)
            else:
                reply_message = reply_map.get(res)
                logger.info(f"够 {reply_message}，但是概率不够")
                await jade.finish()


# 异步请求AI
async def req_glm(auth_token, img_url):
    img_base = await url_to_base64(img_url)
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    data = {
        "model": "glm-4v-flash",
        "temperature": 0.3,
        "messages": [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "需要你进行以下判断，并仅回复符合的标签(如果有多个符合只随机回复一个)："
                            "1.图片中是否出现了人类或动漫人物的脚（包括裸足，穿袜，穿鞋等），如果是请仅回复“yuzu_y”"
                            "2.图片中是否出现了非人类（包括机器人，食物，玩具等）的脚，如果是请仅回复“yuzu_n”"
                            "3.都不符合请回复“none”"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": img_base
                    }
                }
            ]
        }]
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=20, write=20, pool=30)) as client:
        res = await client.post("https://open.bigmodel.cn/api/paas/v4/chat/completions", headers=headers, json=data)
        res = res.json()
    try:
        res_raw = res['choices'][0]['message']['content']
    except Exception as e:
        res_raw = res
    return res_raw


# url转base64
async def url_to_base64(url):
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url)
        if response.status_code == 200:
            image_data = response.content
            base64_encoded = base64.b64encode(image_data).decode('utf-8')
            return base64_encoded
        else:
            raise Exception("无法下载图片，状态码：", response.status_code)


# 检查返回是否为错误
def is_error_response(res):
    if isinstance(res, dict) and 'error' in res:
        error_code = res['error'].get('code')
        if error_code == '1301':
            logger.error(f"模型敏感内容: {res['error']['message']}")
            return True
    return False
