from typing import List

import bs4


class Ascii2DNorm:
    # 缩略图地址
    thumbnail: str = ""
    # 原图长宽，类型，大小
    detail: str = ""
    # 标题
    title: str = ""
    # 作者
    authors: str = ""
    # url地址
    url: str = ""
    marks: str = ""

    def __init__(self, data: list):
        o_url = data[3].find("div", class_="detail-box gray-link").contents
        urls = self._get_urls([i for i in o_url if i != "\n"])
        self.detail = data[3].small.string
        self.thumbnail = "https://ascii2d.net" + data[1].find("img")["src"]
        self.url = urls["url"]
        self.title = urls["title"]
        self.authors = urls["authors"]
        self.marks = urls["mark"]

    @staticmethod
    def _get_urls(data: list) -> dict:
        all_urls = {
            "url": "",
            "title": "",
            "authors_urls": "",
            "authors": "",
            "mark": "",
        }

        for x in data:
            try:
                origin = x.find_all("a")
                all_urls["url"] = origin[0]["href"]
                all_urls["title"] = origin[0].string
                all_urls["authors_urls"] = origin[1]["href"]
                all_urls["authors"] = origin[1].string
                all_urls["mark"] = x.small.string.strip("\n")
            except IndexError:
                pass
        return all_urls

    def __repr__(self):
        return f"<Ascii2DNorm(title={repr(self.title)}, authors={repr(self.authors)}, mark={repr(self.marks)})>"


class Ascii2DResponse:
    def __init__(self, res):
        # 原始返回值
        self.origin: bs4.ResultSet = res
        # 结果返回值
        self.raw: List[Ascii2DNorm] = [Ascii2DNorm(i.contents) for i in self.origin]

    def __repr__(self):
        return f"<Ascii2DResponse(count={len(self.origin)})>"
