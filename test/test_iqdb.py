from unittest import IsolatedAsyncioTestCase

from loguru import logger
from PicImageSearch.sync import Iqdb


class TestIqdb(IsolatedAsyncioTestCase):
    # proxies: str = "http://127.0.0.1:1081"
    proxies: str = ""
    requests_kwargs: dict = {"proxies": proxies} if proxies else {}
    url: str = "https://pixiv.cat/77702503-1.jpg"
    # url: str = r"C:/kitUIN/img/tinted-good.jpg"  # 搜索本地图片

    async def test_iqdb(self):
        iqdb = Iqdb(**self.requests_kwargs)
        res = await iqdb.search(self.url)
        # logger.info(res.origin)
        logger.info(res.raw)
        self.assertEqual(res.raw[0].content, "Best match")  # 说明
        self.assertEqual(
            res.raw[0].url,
            "https://anime-pictures.net/pictures/view_post/621762?lang=en",
        )  # 来源地址
        self.assertEqual(
            res.raw[0].thumbnail,
            "https://iqdb.org/anime-pictures/5/0/4/50430189318ee7163a0ee8219cbaf01e.jpg",
        )  # 缩略图
        self.assertEqual(res.raw[0].similarity, 96.0)  # 相似度
        self.assertEqual(res.raw[0].size, "919×1300 [Ero]")  # 图片大小
        self.assertEqual(res.raw[0].source, "Anime-Pictures")  # 图片来源
        logger.info("其他图片来源:      " + str(res.raw[0].other_source))
        logger.info("SauceNAO搜图链接:  " + res.saucenao_url)
        logger.info("Ascii2d搜图链接:   " + res.ascii2d_url)
        logger.info("TinEye搜图链接:    " + res.tineye_url)
        logger.info("Google搜图链接:    " + res.google_url)
        logger.info("相似度低的结果:    " + str(res.more))
