import os
import json
import requests
from bs4 import BeautifulSoup

product_code = input('enter code:')
page = 1
next = True
while next:
    url = f"https://www.ceneo.pl/{product_code}/opinie-{page}"
    response = requests.get(url)
    print(response.status_code)
    page_dom = BeautifulSoup(response.text, 'html.parser')
    print(type(page_dom))
    product_name = page_dom.select_one('h1').get_text()
    print(product_name)
    print(type(product_name))
    opinions = page_dom.select("div.js_product-review:not(.user-post--highlight)")
    print(type(opinions))
    print(len(opinions))
    all_opinions = []
    for opinion in opinions:
        single_opinion = {
            "opinion_id": opinion.get("data-entry-id"),
            "author": opinion.select_one("span.user-post__author-name").get_text().strip(),
            "recommendation": opinion.select_one("span.user-post__author-recomendation > em").get_text().strip() if opinion.select_one("span.user-post__author-recomendation > em") else None,
            "score": opinion.select_one("span.user-post__score-count").get_text().strip(),
            "content": opinion.select_one("div.user-post__text").get_text().strip(),
            "pros": [p.get_text().strip() for p in opinion.select("div.review-feature__item--positive")],
            "cons": [c.get_text().strip() for c in opinion.select("div.review-feature__item--negative")],
            "helpful": opinion.select_one("button.vote-yes > span").get_text().strip(),
            "unhelpful": opinion.select_one("button.vote-no > span").get_text().strip(),
            "publish_date": opinion.select_one("span.user-post__published > time:nth-child(1)").get('datetime').strip(),
            "purchase_date": opinion.select_one("span.user-post__published > time:nth-child(2)").get('datetime').strip() if opinion.select_one("span.user-post__published > time:nth-child(2)") else None,
        }
        all_opinions.append(single_opinion)
    next = True if page_dom.select_one('button.pagination__next') else False
    if next: page += 1
    if not os.path.exists("./opinions"):
        os.mkdir("./opinions")
        with open(f'./opinions/{product_code}.json', "w", encoding="UTF-8") as jf:
            json.dump(all_opinions, jf, indent=4, ensure_ascii=False)
