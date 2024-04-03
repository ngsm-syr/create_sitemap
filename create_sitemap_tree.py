import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from collections import deque
from urllib.parse import urlsplit

class SitemapGenerator:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited = set()
        self.queue = deque([(base_url, 0)])  # (URL, depth)
        self.pages_info = []  # URLとタイトルのペアを保存するリスト

    def get_html(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # ステータスコードが200以外の場合はエラーを発生させる
            return response.content.decode('utf-8')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return ""

    def get_links(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all("a", href=True):
            full_link = urljoin(url, link['href'])
            if urlparse(full_link).netloc == urlparse(url).netloc and not full_link.lower().endswith(('.pdf', '.xlsx', '.docx', '.doc', '.xls', '.jpg')):
                yield full_link

    def crawl(self):
        while self.queue:
            current_url, depth = self.queue.popleft()
            if current_url not in self.visited:
                print("Visiting:", current_url, "Depth:", depth)
                self.visited.add(current_url)
                title = self.get_page_info(current_url)
                self.pages_info.append((depth, current_url, title))  # 階層レベルも保存
                for link in self.get_links(current_url):
                    self.queue.append((link, depth + 1))  # 次のレベルのリンクをキューに追加

    def get_page_info(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("title").text if soup.find("title") else "No Title"
        return title

    def sort_pages_info(self):
        # URLをパスのセグメントに基づいてソートするためのキー関数
        def sort_key(item):
            depth, url, title = item
            # URLからパスを抽出し、セグメントに分割
            path_segments = urlsplit(url).path.split('/')
            # ドメイン名とパスのセグメントを組み合わせたタプルをソートキーとして使用
            return (urlsplit(url).netloc, *path_segments, depth)

        # ソートキーに基づいてページ情報をソート
        self.pages_info.sort(key=sort_key)

if __name__ == "__main__":
    base_url = "https://sample.com"  # 対象のウェブサイトURLに変更してください
    generator = SitemapGenerator(base_url)
    generator.crawl()

    # 階層、URL、タイトルの順にファイルに保存
    with open("/Users/UserName/Desktop/sitemap_with_titles2.txt", "w", encoding='utf-8') as f:
        for depth, url, title in sorted(generator.pages_info):
            f.write(f"{depth}\t{title}\t{url}\n")  # 必要に応じて出力形式を調整
