from unittest import IsolatedAsyncioTestCase

from loguru import logger
from PicImageSearch.sync import SauceNAO


class TestSauceNao(IsolatedAsyncioTestCase):
    # proxies: str = "http://127.0.0.1:1081"
    proxies: str = ""
    requests_kwargs: dict = {"proxies": proxies} if proxies else {}
    api_key: str = "a4ab3f81009b003528f7e31aed187fa32a063f58"
    url: str = "https://pixiv.cat/77702503-1.jpg"
    # url: str = r"C:/kitUIN/img/tinted-good.jpg"  # 搜索本地图片

    async def test_saucenao(self):
        saucenao = SauceNAO(api_key=self.api_key, **self.requests_kwargs)
        res = await saucenao.search(self.url)
        # logger.info(res.origin)  # 原始数据
        logger.info(res.raw)
        self.assertEqual(
            str(res.raw[0]), "<SauceNAONorm(title='MDR♡', similarity=92.23)>"
        )
        self.assertIsInstance(res.long_remaining, int)
        self.assertIsInstance(res.short_remaining, int)
        logger.info(
            res.raw[0].thumbnail
        )  # https://img1.saucenao.com/res/pixiv/7770/77702503_p0_master1200.jpg?auth=pJmiu8qNI1z2fLBAlAsx7A&exp=1604748473
        self.assertEqual(res.raw[0].similarity, 92.23)
        self.assertEqual(res.raw[0].title, "MDR♡")
        self.assertEqual(res.raw[0].author, "CeNanGam")
        self.assertEqual(
            res.raw[0].url,
            "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=77702503",
        )
        self.assertEqual(res.raw[0].pixiv_id, 77702503)
        self.assertEqual(res.raw[0].member_id, 4089680)
