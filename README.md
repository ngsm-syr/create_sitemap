* 指定したウェブサイトをクロールして、各ページのURLとタイトルを収集し、UTF-8エンコーディングでテキストファイルに保存するPythonコードです。
* requests と beautifulsoup4のインストールが必要
* pip install requests beautifulsoup4
* 保存場所を指定したい場合は、UserNameの部分をユーザー名に書き換えます（Mac）  
/Users/UserName/Desktop/sitemap_with_titles.txt
* 内部リンクのみクロールします（外部リンクは除外）
* excluded_extensions = [ ] の部分で除外したい拡張子を指定します
