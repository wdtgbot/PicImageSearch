from unittest import IsolatedAsyncioTestCase

from loguru import logger
from PicImageSearch.sync import TraceMoe


class TestTraceMoe(IsolatedAsyncioTestCase):
    # proxies: str = "http://127.0.0.1:1081"
    proxies: str = ""
    requests_kwargs: dict = {"proxies": proxies} if proxies else {}
    url: str = "https://trace.moe/img/tinted-good.jpg"
    # url: str = r"C:/Users/kulujun/Pictures/1.png"  # 搜索本地图片

    async def test_tracemoe(self):
        tracemoe = TraceMoe(mute=False, size=None, **self.requests_kwargs)
        res = await tracemoe.search(self.url)
        # logger.info(res.origin)
        logger.info(res.raw)
        self.assertEqual(
            str(res.raw[0]),
            "<TraceMoeNorm(filename='Kokoro Connect - 05 (BD 1280x720 x264 AACx2).mp4', similarity=0.98)>",
        )
        self.assertEqual(res.frameCount, 9766029)
        self.assertEqual(res.raw[0].anilist, 11887)
        self.assertEqual(res.raw[0].idMal, 11887)
        self.assertEqual(
            res.raw[0].title,
            {
                "native": "ココロコネクト",
                "romaji": "Kokoro Connect",
                "english": "Kokoro Connect",
            },
        )
        self.assertEqual(res.raw[0].title_native, "ココロコネクト")
        self.assertEqual(res.raw[0].title_romaji, "Kokoro Connect")
        self.assertEqual(res.raw[0].title_english, "Kokoro Connect")
        self.assertEqual(res.raw[0].title_chinese, "心連·情結")
        self.assertEqual(res.raw[0].synonyms, ["Kokoroco"])
        self.assertFalse(res.raw[0].isAdult)
        self.assertEqual(
            res.raw[0].filename, "Kokoro Connect - 05 (BD 1280x720 x264 AACx2).mp4"
        )
        self.assertEqual(res.raw[0].episode, 5)
        self.assertEqual(res.raw[0].From, 1166)
        self.assertEqual(res.raw[0].To, 1175)
        self.assertEqual(res.raw[0].similarity, 0.98)
        logger.info(res.raw[0].video)
        logger.info(res.raw[0].image)
