import re
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["ru.wikipedia.org"]
    delimiter = ";"
    def start_requests(self):
        url = "https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Ссылки на фильмы
        for movie in response.css("div.mw-category-group ul li a"):

            is_subcategory = movie.xpath(
                "./ancestor::div[contains(@class, 'CategoryTreeItem')]").get()

            if not is_subcategory:
                film_link = movie.css("::attr(href)").get()
                absolute_url = f"https://ru.wikipedia.org{film_link}"
                yield scrapy.Request(url=absolute_url, callback=self.filmInfo)

        next_page = response.xpath("//a[contains(text(), 'Следующая страница')]/@href").get()

        if next_page:
            next_page_url = "https://ru.wikipedia.org" + next_page
            #print(f"[DEBUG] Found next page: {next_page_url}")
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            print("[DEBUG] No more pages")

    #
    def filmInfo(self, response):
        genre = None
        year = None
        directors = []
        countries = []
        IMDB_id = None
        IMDB_link = None


        name = response.css("table.infobox tr")[0].css("th::text").get()
        for tr in response.css("table.infobox tr")[1:]:
            title = tr.css("th::text").get()
            if title is None:
                title = tr.css("th a::text").get()
            if title is None:
                title = tr.css("th span::text").get()

            if title is not None:

                match title.strip():
                    case "Жанр" | "Жанры":
                        genre = text(tr)


                    case "Год":
                        year = text(tr)
                        year = [yea for yea in year if is_year(yea)]


                    case "Режиссёр" | "Режиссёры":
                        directors = text(tr)


                    case "Страна" | "Страны":
                        countries = text(tr)

                    case "IMDb":
                        IMDB_id = tr.css("td span a::text").get()
                        IMDB_link = tr.css("td span a::attr(href)").get()

        yield {
            "title": name if name else "Не указано",
            "genre": genre if genre else "Не указано",
            "director": directors if directors else "Не указано",
            "country": countries if countries else "Не указано",
            "year": year if year else "Не указано",
            "IMDB_id": IMDB_id if IMDB_id else "Не указано",
            "IMDB_link": IMDB_link if IMDB_link else "Не указано"
        }





def text(tr):
    # print("text", datetime.now())
    td_elements = tr.xpath('.//td//*[not(self::br)][text()]')

    # Извлекаем текст из каждого элемента (игнорируя <br>)
    texts = [el.xpath('normalize-space(.)').get() for el in td_elements]

    # Фильтруем пустые значения
    result = [text for text in texts if text]
    result = [text for text in result if "[" not in text]
    result = [text for text in result if "]" not in text]
    result = [text for text in result if "." not in text]
    result = [text for text in result if "\xa0" not in text]

    return result

def is_year(text):
    return bool(re.match(r"^\d{4}$", text.strip()))

