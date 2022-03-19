from unittest import IsolatedAsyncioTestCase

from loguru import logger
from PicImageSearch.sync import Iqdb


class TestIqdb3D(IsolatedAsyncioTestCase):
    # proxies: str = "http://127.0.0.1:1081"
    proxies: str = ""
    requests_kwargs: dict = {"proxies": proxies} if proxies else {}
    url: str = "https://3d.iqdb.org/3dbooru/2/8/6/2865ab9c1d9fe8860892945e79435219.jpg"

    async def test_iqdb_3d(self):
        iqdb = Iqdb(**self.requests_kwargs)
        res = await iqdb.search_3d(self.url)
        # logger.info(res.origin)
        logger.info(res.raw)
        self.assertEqual(res.raw[0].content, "Best match")  # 说明
        self.assertEqual(res.raw[0].url, "http://behoimi.org/post/show/649013")  # 来源地址
        self.assertEqual(
            res.raw[0].thumbnail,
            "https://iqdb.org/3dbooru/2/8/6/2865ab9c1d9fe8860892945e79435219.jpg",
        )  # 缩略图
        self.assertEqual(res.raw[0].similarity, 99.0)  # 相似度
        self.assertEqual(res.raw[0].size, "1840×1228 [Safe]")  # 图片大小
        self.assertEqual(res.raw[0].source, "3dbooru")  # 图片来源
        self.assertEqual(res.raw[0].other_source, [])  # 其他图片来源
        logger.info("相似度低的结果:    " + str(res.more))  # 相似度低的结果
