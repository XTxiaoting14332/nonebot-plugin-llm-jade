from pydantic import BaseModel

class Config(BaseModel):

    # 用户token
    jadefoot_token: str = ""

    # 触发概率
    jadefoot_probability: float = 0.3