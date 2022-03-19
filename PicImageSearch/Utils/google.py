import re
from typing import List

import bs4


class GoogleNorm:
    # 缩略图地址
    thumbnail: str = ""
    # 标题
    title: str = ""
    # url地址
    url: str = ""

    def __init__(self, data):
        get_data = self._get_data(data)
        self.title = get_data["title"]
        self.url = get_data["url"]
        self.thumbnail = get_data["thumbnail"]

    def _get_data(self, datas) -> dict:

        data = {
            "thumbnail": "",
            "title": "",
            "url": "",
        }

        for x in datas:
            try:
                origin = x.find_all("h3")
                data["title"] = origin[0].string
                url = x.find_all("a")
                data["url"] = url[0]["href"]
                img = self._get_thumbnail(url)
                data["thumbnail"] = img
            except IndexError:
                pass

        return data

    @staticmethod
    def _get_thumbnail(data) -> str:
        google_url = "https://www.google.com/"
        regex = re.compile(
            r"((http(s)?(://))+(www\.)?([\w\-./])*(\.[a-zA-Z]{2,3}/?))[^\s\b\n|]*[^.,;:?!@^$ -]"
        )

        thumbnail = "No detectable url"

        for a in range(5):
            try:
                if re.findall("jpg|png", regex.search(data[a]["href"]).group(1)):
                    thumbnail = regex.search(data[a]["href"]).group(1)
                elif re.findall("/imgres", data[a]["href"]):
                    thumbnail = f"{google_url}{data[a]['href']}"
            except (AttributeError, IndexError):
                continue

        return thumbnail

    def __repr__(self):
        return f"<GoogleNorm(title={repr(self.title)}, url={repr(self.url)}, thumbnail={repr(self.thumbnail)})>"


class GoogleResponse:
    def __init__(self, res, pages, index):
        # 原始返回值
        self.origin: bs4.ResultSet = res
        # 结果返回值
        self.raw: List[GoogleNorm] = [GoogleNorm(i.contents) for i in self.origin]
        # 当前页
        self.index: int = index
        # 总页数
        self.page: int = len(pages)
        # 页面源
        self.pages: list = pages

    def get_page_url(self, index) -> str:
        if self.index != index:
            url = "https://www.google.com" + self.pages[index - 1].a["href"]
            return url
        return ""

    def __repr__(self):
        return f"<GoogleResponse(count{len(self.origin)})>"
