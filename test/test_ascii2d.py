from unittest import IsolatedAsyncioTestCase

from loguru import logger
from PicImageSearch.sync import Ascii2D


class TestAscii2D(IsolatedAsyncioTestCase):
    # proxies: str = "http://127.0.0.1:1081"
    proxies: str = ""
    requests_kwargs: dict = {"proxies": proxies} if proxies else {}
    url: str = "https://pixiv.cat/77702503-1.jpg"
    # url: str = r"C:/kitUIN/img/tinted-good.jpg"  # 搜索本地图片

    async def test_ascii2d(self):
        ascii2d = Ascii2D(bovw=True, **self.requests_kwargs)
        res = await ascii2d.search(self.url)
        # logger.info(res.origin)  # 原始数据
        logger.info(res.raw)
        self.assertEqual(
            str(res.raw[1]),
            "<Ascii2DNorm(title='MDR♡', authors='CeNanGam', mark='pixiv')>",
        )
        self.assertEqual(
            res.raw[1].thumbnail,
            "https://ascii2d.net/thumbnail/5/0/4/3/50430189318ee7163a0ee8219cbaf01e.jpg",
        )
        self.assertEqual(res.raw[1].title, "MDR♡")
        self.assertEqual(res.raw[1].authors, "CeNanGam")
        self.assertEqual(res.raw[1].url, "https://www.pixiv.net/artworks/77702503")
        self.assertEqual(res.raw[1].detail, "919x1300 JPEG 1002.6KB")
