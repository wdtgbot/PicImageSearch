from loguru import logger
from PicImageSearch.sync import BaiDu

# proxies = "http://127.0.0.1:1081"
proxies = ""
requests_kwargs = {"proxies": proxies} if proxies else {}
baidu = BaiDu(**requests_kwargs)
res = baidu.search(
    "https://i0.hdslb.com/bfs/article/e756dd0a8375a4c30cc0ee3a51c8067157486135.jpg@1524w_856h.webp"
)
# logger.info(res.origin)
logger.info(res.item)
if hasattr(res, "same"):  # 存在来源结果
    logger.info(res.raw[0].page_title)
    logger.info(res.raw[0].abstract)
    logger.info(res.raw[0].url)
    logger.info(res.raw[0].image_src)
else:
    logger.info(res.similar)
