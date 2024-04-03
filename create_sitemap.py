import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class SitemapGenerator:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited = set()
        self.pages_info = []  # URLとタイトルのペアを保存するリスト

    def get_html(self, url):
        try:
            response = requests.get(url)
            # レスポンスを'utf-8'で明示的にデコードする
            return response.content.decode('utf-8')
        except requests.RequestException:
            return ""

    def get_page_info(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("title").text if soup.find("title") else "No Title"
        return title

    def get_links(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        links = set()
        excluded_extensions = ['.pdf', '.xlsx', '.docx', '.jpg', '.doc', '.xls']  # 除外する拡張子のリスト
        for link in soup.find_all("a", href=True):
            full_link = urljoin(url, link['href'])
            # 除外する拡張子で終わるリンクを無視
            if not any(full_link.lower().endswith(ext) for ext in excluded_extensions):
                if urlparse(full_link).netloc == urlparse(url).netloc:
                    links.add(full_link)
        return links

    def crawl(self, url):
        if url in self.visited:
            return
        print("Visiting:", url)
        self.visited.add(url)
        title = self.get_page_info(url)
        self.pages_info.append((url, title))
        for link in self.get_links(url):
            self.crawl(link)  # この再帰呼び出しでサイト内のリンクを辿る

if __name__ == "__main__":
    base_url = "https://sample.com"  # 対象のウェブサイトURLに変更してください
    generator = SitemapGenerator(base_url)
    generator.crawl(base_url)

    # URLとタイトルのペアをファイルに保存
    with open("/Users/UserName/Desktop/sitemap_with_titles.txt", "w", encoding='utf-8') as f:
        for url, title in generator.pages_info:
            f.write(f"{url}\t{title}\n")
