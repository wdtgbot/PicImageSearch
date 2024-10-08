import asyncio

from loguru import logger

from src import EHentai, Network
from src.model import EHentaiResponse
from src.sync import EHentai as EHentaiSync

proxies = "http://127.0.0.1:1081"
# proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test06.jpg"
file = "../images/test06.jpg"

# 注意: EXHentai 検索にはクッキーが必要
cookies = None

# EXHentai 検索を使用するかどうか、クッキーが設定されている場合に EXHentai 検索を使用することをお勧めします
ex = False

# 空のドキュメントを返すタイムアウトを避ける
timeout = 60


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies, cookies=cookies, timeout=timeout) as client:
        ehentai = EHentai(client=client)
        # resp = await ehentai.search(url=url, ex=ex)
        resp = await ehentai.search(file=file, ex=ex)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    ehentai = EHentaiSync(proxies=proxies, cookies=cookies, timeout=timeout)
    resp = ehentai.search(url=url, ex=ex)
    # resp = ehentai.search(file=file, ex=ex)
    show_result(resp)  # type: ignore


def show_result(resp: EHentaiResponse) -> None:
    # logger.info(resp.origin)  # オリジナルデータ
    logger.info(resp.url)  # 検索結果へのリンク
    # logger.info(resp.raw[0].origin)
    logger.info(resp.raw[0].title)
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].thumbnail)
    logger.info(resp.raw[0].type)
    logger.info(resp.raw[0].date)

    # コンパクト/拡張ページレイアウトを使用することをお勧めします。そうでない場合、タグを取得できません
    logger.info(resp.raw[0].tags)
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_async())
    # test_sync()
