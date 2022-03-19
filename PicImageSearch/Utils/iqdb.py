import re
from typing import List

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


class IqdbNorm:
    no_more: bool = True
    # 备注
    content: str = ""
    # url地址
    url: str = ""
    # 来源平台名称
    source: str = ""
    # 其他来源
    other_source: list = []
    # 缩略图地址
    thumbnail: str = ""
    # 原图长宽大小
    size: str = ""
    # 相似值
    similarity: float = 0

    def __init__(self, data: Tag, no_more: bool = True):
        self.no_more = no_more
        self._arrange(data.table)

    def _arrange(self, data: Tag):
        regex_iq = re.compile("[0-9]+")
        if self.no_more:
            self.content = data.tr.th.string
            if self.content == "No relevant matches":
                return
            tbody = data.tr.next_sibling
        else:
            tbody = data.tr
        self.url = self._get_url(tbody.td.a["href"])
        self.thumbnail = "https://iqdb.org" + tbody.td.a.img["src"]
        tbody = tbody.next_sibling
        source = [stt for stt in tbody.td.strings]
        if len(source) > 1:
            self.other_source.append(
                {"source": source[1], "url": self._get_url(tbody.td.a["href"])}
            )
        tbody = tbody.next_sibling
        self.size = tbody.td.string
        similarity_raw = regex_iq.search(tbody.next_sibling.td.string)
        if similarity_raw:
            self.similarity = float(similarity_raw.group(0))
        self.source = source[0]

    @staticmethod
    def _get_url(url: str):
        if url[:4] == "http":
            return url
        return f"https:{url}"

    def __repr__(self):
        return f"<IqdbNorm(content={repr(self.content)}, source={repr(self.source)}, similarity={self.similarity})>"


class IqdbResponse:
    def __init__(self, res: bytes):
        # 原始返回值
        self.origin: bytes = res
        # 结果返回值
        self.raw: List[IqdbNorm] = []
        # 更多结果返回值(低相似度)
        self.more: List[IqdbNorm] = []
        # SauceNao搜索链接
        self.saucenao_url: str = ""
        # Ascii2d搜索链接
        self.ascii2d_url: str = ""
        # Google搜索链接
        self.google_url: str = ""
        # TinEye搜索链接
        self.tineye_url: str = ""
        self._slice(res)

    def _slice(self, data: bytes) -> None:
        soup = BeautifulSoup(data, "html.parser")

        pages = soup.find(attrs={"class": "pages"})
        for i in pages:
            if i == "\n" or str(i) == "<br/>" or "Your image" in str(i):
                continue
            # logger.info(i)
            self.raw.append(IqdbNorm(i))
        self._get_show(soup.find(attrs={"id": "show1"}))
        self._get_more(soup.find(attrs={"id": "more1"}))

    def _get_more(self, data: Tag) -> None:
        for i in data.contents[2]:
            if str(i)[:2] == "<d":
                self.more.append(IqdbNorm(i, False))
            # logger.info(i)

    def _get_show(self, data: Tag) -> None:
        for j in data.contents:
            if type(j) != NavigableString:
                if j["href"] == "#":
                    continue
                if j.string == "SauceNao":
                    self.saucenao_url = "https:" + j["href"]
                elif j.string == "ascii2d.net":
                    self.ascii2d_url = j["href"]
                elif j.string == "Google Images":
                    self.google_url = "https:" + j["href"]
                elif j.string == "TinEye":
                    self.tineye_url = "https:" + j["href"]

    def __repr__(self):
        return f"<IqdbResponse(count={len(self.raw)})>"
