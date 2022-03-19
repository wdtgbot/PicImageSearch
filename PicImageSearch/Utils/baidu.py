import json
import re
from typing import Dict, List, Optional


class BaiDuNorm:
    def __init__(self, data):
        # 原始返回值
        self.origin: dict = data
        # 页面标题
        self.page_title: str = data["fromPageTitle"]
        # 标题
        self.title: str = data["title"][0]
        # 说明文字
        self.abstract: str = data["abstract"]
        # 图片地址
        self.image_src: str = data["image_src"]
        # 图片所在网页地址
        self.url: str = data["url"]
        # 其他图片地址列表
        self.img: list = data.get("imgList", [])

    def __repr__(self):
        return f"<BaiDuNorm(title={repr(self.title)})>"


class BaiDuResponse:
    def __init__(self, res):
        # 百度识图原网页
        self.url: str = res.request.url  # 搜索结果地址
        # 相似结果返回值
        self.similar: Optional[List[Dict]] = []
        # 来源结果返回值
        self.raw: Optional[List[BaiDuNorm]] = []
        # 原始返回值
        self.origin: list = json.loads(
            re.search(r"cardData = (.+);window\.commonData", res.text)[1]
        )
        for i in self.origin:
            setattr(self, i["cardName"], i)
        if hasattr(self, "same"):
            self.raw = [BaiDuNorm(x) for x in self.same["tplData"]["list"]]
            info = self.same["extData"]["showInfo"]
            del info["other_info"]
            for y in info:
                for z in info[y]:
                    try:
                        self.similar[info[y].index(z)][y] = z
                    except IndexError:
                        self.similar.append({y: z})
        # 获取所有卡片名
        self.item: list[str] = [
            attr
            for attr in dir(self)
            if not callable(getattr(self, attr))
            and not attr.startswith(("__", "origin", "raw", "same", "url"))
        ]

    def __repr__(self):
        return f"<BaiDuResponse(item={self.item} , url={repr(self.url)})>"
