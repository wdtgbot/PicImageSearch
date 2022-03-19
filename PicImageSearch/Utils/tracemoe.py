from typing import List, Optional

import httpx
from pathlib2 import Path

from ..network import HandOver


class TraceMoeAnilist:
    def __init__(self, data):
        # 匹配的 Anilist ID 见 https://anilist.co/
        self.id: int = data["id"]
        # 匹配的 MyAnimelist ID 见 https://myanimelist.net/
        self.idMal: int = data["idMal"]
        # 番剧名字
        self.title: dict = data["title"]
        # 番剧国际命名
        self.title_native: str = data["title"]["native"]
        # 番剧英文命名
        self.title_english: str = data["title"]["english"]
        # 番剧罗马命名
        self.title_romaji: str = data["title"]["romaji"]
        # 番剧中文命名
        self.title_chinese: str = data["title"].get("chinese", "")
        # 备用英文标题
        self.synonyms: list = data["synonyms"]
        # 是否R18
        self.isAdult: bool = data["isAdult"]

    def __repr__(self):
        return (
            f"(<id={self.id}, idMal={self.idMal}, title={self.title},"
            f" synonyms={self.synonyms}, isAdult={self.isAdult})> "
        )


class TraceMoeMe:
    def __init__(self, data):
        # IP 地址（访客）或电子邮件地址（用户）
        self.id: str = data["id"]
        # 优先级
        self.priority: int = data["priority"]
        # 搜索请求数量
        self.concurrency: int = data["concurrency"]
        # 本月的搜索配额
        self.quota: int = data["quota"]
        # 本月已经使用的搜索配额
        self.quotaUsed: int = data["quotaUsed"]

    def __repr__(self):
        return f"<TraceMoeMe(id={repr(self.id)}, quota={self.quota})>"


class TraceMoeNorm(HandOver):
    def __init__(
        self, data, chinese_title=True, mute=False, size=None, **requests_kwargs
    ):
        """

        :param data: 数据
        :param chinese_title: 中文番剧名称显示
        :param mute: 预览视频静音
        :param size: 视频与图片大小(s/m/l)
        """
        super().__init__(**requests_kwargs)
        # 原始数据
        self.origin: dict = data
        # 匹配的 MyAnimelist ID 见 https://myanimelist.net/
        self.idMal: int = 0
        # 剧名字
        self.title: dict = {}
        # 番剧国际命名
        self.title_native: str = ""
        # 剧英文命名
        self.title_english: str = ""
        # 番剧罗马命名
        self.title_romaji: str = ""
        # 番剧中文命名
        self.title_chinese: str = ""
        # 匹配的 Anilist ID 见 https://anilist.co/
        self.anilist: Optional[int] = None
        # 备用英文标题
        self.synonyms: list = []
        # 是否R18
        self.isAdult: bool = False
        if type(data["anilist"]) == dict:
            self.anilist = data["anilist"]["id"]  # 匹配的 Anilist ID 见 https://anilist.co/
            self.idMal: int = data["anilist"][
                "idMal"
            ]  # 匹配的 MyAnimelist ID 见 https://myanimelist.net/
            self.title: dict = data["anilist"]["title"]  # 番剧名字
            self.title_native: str = data["anilist"]["title"]["native"]  # 番剧国际命名
            self.title_english: str = data["anilist"]["title"]["english"]  # 番剧英文命名
            self.title_romaji: str = data["anilist"]["title"]["romaji"]  # 番剧罗马命名
            self.synonyms: list = data["anilist"]["synonyms"]  # 备用英文标题
            self.isAdult: bool = data["anilist"]["isAdult"]  # 是否R18
            if chinese_title:
                self.title_chinese: str = self._get_chinese_title()  # 番剧中文命名
        else:
            self.anilist: int = data["anilist"]  # 匹配的Anilist ID见https://anilist.co/
        # 找到匹配项的文件名
        self.filename: str = data["filename"]
        # 估计的匹配的番剧的集数
        self.episode: int = data["episode"]
        # 匹配场景的开始时间
        self.From: int = data["from"]
        # 匹配场景的结束时间
        self.To: int = data["to"]
        # 相似度，相似性低于 87% 的搜索结果可能是不正确的结果
        self.similarity: float = float(data["similarity"])
        # 预览视频
        self.video: str = data["video"]
        # 预览图像
        self.image: str = data["image"]
        if size in ["l", "s", "m"]:  # 大小设置
            self.video += "&size=" + size
            self.image += "&size=" + size
        if mute:  # 视频静音设置
            self.video += "&mute"

    async def download_image(
        self, filename="image.png", path: Path = Path.cwd()
    ) -> Path:
        """
        下载缩略图

        :param filename: 重命名文件
        :param path: 本地地址(默认当前目录)
        :return: 文件路径
        """
        endpoint = await self.downloader(self.image, path, filename)
        return endpoint

    async def download_video(
        self, filename="video.mp4", path: Path = Path.cwd()
    ) -> Path:
        """

        下载预览视频

        :param filename: 重命名文件
        :param path: 本地地址(默认当前目录)
        :return: 文件路径
        """
        endpoint = await self.downloader(self.video, path, filename)
        return endpoint

    def _get_chinese_title(self) -> str:
        return self.get_anime_title(self.origin["anilist"]["id"])["data"]["Media"][
            "title"
        ]["chinese"]

    @staticmethod
    def get_anime_title(anilist_id: int) -> dict:
        """获取中文标题

        :param anilist_id: id
        :return: dict
        """
        query = """
        query ($id: Int) { # Define which variables will be used in the query (id)
          Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
            id
            title {
              romaji
              english
              native
            }
          }
        }
        """

        # Define our query variables and values that will be used in the query request
        variables = {"id": anilist_id}

        url = "https://trace.moe/anilist/"

        response = httpx.post(url, json={"query": query, "variables": variables})
        return response.json()

    def __repr__(self):
        return f"<TraceMoeNorm(filename={repr(self.filename)}, similarity={self.similarity:.2f})>"


class TraceMoeResponse:
    def __init__(self, res, chinese_title, mute, size, **requests_kwargs):
        self.requests_kwargs = requests_kwargs
        # 原始数据
        self.origin: dict = res
        # 结果返回值
        self.raw: List[TraceMoeNorm] = list()
        res_docs = res["result"]
        for i in res_docs:
            self.raw.append(
                TraceMoeNorm(
                    i,
                    chinese_title=chinese_title,
                    mute=mute,
                    size=size,
                    **self.requests_kwargs,
                )
            )
        # 搜索结果数量
        self.count: int = len(self.raw)
        # 搜索的帧总数
        self.frameCount: int = res["frameCount"]
        # 错误报告
        self.error: str = res["error"]

    def __repr__(self):
        return f"<TraceMoeResponse(count={len(self.raw)}, frameCount={self.frameCount}"
