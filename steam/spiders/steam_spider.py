import pandas as pd
import scrapy


class SteamSpider(scrapy.Spider):
    name = "steam"

    def start_requests(self):
        df = pd.read_csv("data.csv")
        urls = df["url"].to_list()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        url = response.url

        user = url.split("/")[-3]
        game = url.split("/")[-1]

        # Get tag html "img".
        html_img_review = response.xpath(
            "/html/body/div[1]/div[7]/div[5]/div/div[2]/div/div/div[2]/div[3]/div[1]/img[2]"
        )

        # Not exists xpath
        if len(html_img_review) == 0:
            return dict(game=game, user=user, like=None)

        # recommended = 1 -> "icon_thumbsUp.png"
        # recommended = 0 -> "icon_thumbsDown.png"
        src_img = html_img_review.attrib["src"].split("/")[-1].lower()
        recommended = 1 if "up" in src_img else 0

        return dict(game=game, user=user, recommended=recommended)
