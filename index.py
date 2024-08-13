try:
    import requests
    import time
    import json
    import random
    from difflib import SequenceMatcher
    from sys import exit
    import pandas as pd
    from tabulate import tabulate
    from bs4 import BeautifulSoup
    from googlesearch import search
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context
    [
        print(f"{i+1}. {option}")
        for i, option in enumerate(
            [
                "google url bulma",
                "amazon isimlerini bulma ve excel dosyasına kayıt etme",
                "akakce verilerini bulma ve excel dosyasına kayıt etme",
            ]
        )
    ]

    choice = input("Lütfen hangi işlemi yapacağınızı seçin (1, 2, veya 3): ")

    def write_errors(error):
        with open("error.json", "w", encoding="utf-8") as f:
            json.dump(error, f, ensure_ascii=False)

    def read_exel():
        try:
            print("Excel dosyası okunuyor..")
            excel_data = pd.read_excel("data.xlsx")
        except FileNotFoundError:
            print("Excel dosyası bulunamadı")
            message = "Lütfen data.xlsx dosyasını oluşturun ve verileri girin"
            print(message)
            write_errors(message)
            return
        return excel_data

    url = "https://api.akakce.com/v5/ns/"
    headers = {
        "Cookie": "APPV5DM=0; AAUSERAPPID=5063811; APPV5R=1; APPVRS=5%2E9%2E31; ASPSESSIONIDSQQTBDSR=NPEIPHHBOIJECDFJGFKBDDHG",
        "User-Agent": "okhttp/4.10.0",
    }
    max_matching_products = 1
    table = [["ID", "EAN", "AKAKÇE ADI", "AKAKÇE FiYATI", "AKAKÇE LİNKİ"]]
    amazon_pnames = [["AMAZON ADI"]]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    ]
    start_time = time.time()
    excel_data = pd.DataFrame()
    google_urls = []
    amazon_data = []

    # Fiyat bilgisini çekme
    def get_price(product):
        # "p" anahtarını kontrol et
        if "lp" in product and product["lp"]:
            return product["lp"]
        # Eğer "p" yoksa "lp" anahtarını kontrol et
        elif "p" in product and product["p"]:
            return product["p"]
        else:
            return "No data available"

    # Amazon sonuçlarını Excel dosyasına yazma
    def save_amazon_names_into_excel(amazon_names):
        print("Excel dosyasına yazılıyor..")
        for i, amazon_name in zip(excel_data.index, amazon_names):
            excel_data.at[i, "Marka_Model"] = amazon_name
            excel_data.to_excel("data.xlsx", index=False)

        print("Yazma işlemi tamamlandı.")

    # Akakçe sonuçlarını Excel dosyasına yazma
    def save_price_into__execl():
        print("Excel dosyasına yazılıyor..")
        product_names = [row[2] for row in table[1:]]
        prices = [row[3] for row in table[1:]]
        links = [row[4] for row in table[1:]]

        for i, name, link, price in zip(excel_data.index, product_names, links, prices):
            excel_data.at[i, "AKAKÇE FiYATI"] = price
            excel_data.at[i, "AKAKÇE ADI"] = name
            excel_data.at[i, "AKAKÇE LİNKİ"] = link

        excel_data.to_excel("data.xlsx", index=False)

        print("Yazma işlemi tamamlandı.")

    # Logları kaydetme
    def save_logs(urls=None, amazon_names=None):
        print("Loglar kayıt ediliyor..")
        logs = {
            "urls": {f"id_{i}": url for i, url in enumerate(urls)} if urls else {},
            "names": (
                {f"id_{i}": name for i, name in enumerate(amazon_names)}
                if amazon_names
                else {}
            ),
        }
        with open("logs.json", "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False)
        print("Loglar kayıt edildi.")

    # Google'da arama yaparak ürün linklerini bulma
    def get_google_urls():
        try:
            isbn_codes = list(excel_data["isbn"].values)
        except KeyError:
            message = "Lütfen isbn sütununun excel dosyasında var olduğundan emin olun."
            print(message)
            write_errors(message)
            return

        print("Url'ler getiriliyor..")
        for isbn_code in isbn_codes:
            query = isbn_code
            search_results = list(search(query, tld="co.in", num=1, stop=1, pause=2))
            if search_results:
                for url in search_results:
                    google_urls.append(url)
                    print(url)
            else:
                google_urls.append("No data available")
                print("No data available")

        print("Url getirme işlemi tamamlandı.")

        return google_urls

    # Amazon'dan ürün isimlerini çekme
    def get_amazon_product_names(urls):
        print("Amazon isimleri getiriliyor..")
        for url in urls:
            user_agent = random.choice(user_agents)
            headers = {
                "User-Agent": user_agent,
                "Accept-Language": "tr,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Cookie": "session-id=259-7597363-7851834; i18n-prefs=TRY; ubid-acbtr=260-7391540-1403156; session-token=z5ACu3wS7KOElFks7Dz6der3setJSvj7SbadW7rrYF2GRWHJMQCUqYli32FGT8Foif3O69yrmGFgwXTK9Z9UkDZQgd4G0OXsl3ICHtk4AmYlMYAEVZopDTuTOEsO3BAZTrqZUn6cDLSIzYWSemg02GWUAyR9D4e/RIpVY120bhuspVE34bv87pu53kiNvlqlBXuiOleTzgAHedAd7wbJm+6/2PrdVGl4K1Mb6EGAXt5M2/5SeRcc9nzEE/6u/rE1n4jdutW2i2FeavJWIMSwXpNIaeCes9RHqGqWIZIOUKAxJI+pPr4gUhqyyRjWQci6QI9K5JEAUERB0gr5ZeXEZwzZRipryWvHG+KZ0NjNHIE=; csm-hit=tb:s-BQ8ZMHT6P5NS9JKQPMWG|1715166772837&t:1715166774314&adb:adblk_yes; session-id-time=2082787201l",
            }
            if url != "No data available":
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")
                product_title = (
                    soup.find(id="centerCol")
                    .find("span", id="productTitle")
                    .text.strip()
                )
                print(product_title)
                amazon_data.append(product_title)

            else:
                print("İsim bulunamadı.")
                amazon_data.append("No data available")
            time.sleep(3)
        print("İsim getirme işlemi tamamlandı.")
        return amazon_data

    # Akakçe'de ürün arama
    def search_in_akakce():
        try:
            ean_codes = list(excel_data["EAN"].values)
            product_names = list(excel_data["Marka_Model"].values)
        except KeyError:
            message = "Lütfen EAN ve Marka_Model sütunlarının excel dosyasında var olduğundan emin olun."
            print(message)
            write_errors(message)
            return

        print("Ürünler taranıyor..")
        for i in range(len(ean_codes)):
            print(f"Product {i + 1}/{len(ean_codes)}")
            ean_code = ean_codes[i]
            if ean_code != "no data available":
                product_name = product_names[i]
                params = {
                    "a": "ds",
                    "p": "1",
                    "q": ean_code,
                    "c": "",
                    "s": "2",
                    "t": "6",
                    "f": "",
                }
                response = requests.get(url, params=params, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    # print("Response:", data)
                    if "pl" in data and "products" in data["pl"]:
                        products = data["pl"]["products"]
                        if len(products) == 1:
                            product = products[0]
                            link = f"https://www.akakce.com/arama/?q={product['n'].replace(' ', '+')}"
                            name = product["n"]
                            price = get_price(product)
                            print(f"Name: {name}, Price: {price}, Link: {link}")
                            table.append([i, ean_code, name, price, link])
                        else:
                            matching_products = []
                            for product in data["pl"]["products"]:
                                similarity = SequenceMatcher(
                                    None, product["n"], product_name
                                ).ratio()
                                if similarity > 0.4:
                                    matching_products.append((product, similarity))
                                else:
                                    print(
                                        f"Similarity: {similarity}, Name: {product['n']}"
                                    )
                            matching_products.sort(key=lambda x: x[1], reverse=True)
                            top_matching_products = matching_products[
                                :max_matching_products
                            ]
                            if top_matching_products:
                                for product, similarity in top_matching_products:
                                    link = f"https://www.akakce.com/arama/?q={product['n'].replace(' ', '+')}"
                                    name = product["n"]
                                    price = get_price(product)
                                    print(
                                        f"Similarity: {similarity}, Name: {name}, Price: {price}, Link: {link}"
                                    )
                                    table.append([i, ean_code, name, price, link])
                            else:
                                print("Herhangi bir ürün eşleşmedi.")
                                table.append(
                                    [
                                        i,
                                        ean_code,
                                        "No data available",
                                        "No data available",
                                        "No data available",
                                    ]
                                )
                    else:
                        print("Ürün bulunamadı.")
                        table.append(
                            [
                                i,
                                ean_code,
                                "No data available",
                                "No data available",
                                "No data available",
                            ]
                        )
                else:
                    print("Request failed with status code:", response.status_code)
            else:
                table.append(
                    [
                        i,
                        ean_code,
                        "No data available",
                        "No data available",
                        "No data available",
                    ]
                )
            time.sleep(3)

        print("Tarama işlemi tamamlandı.")
        print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"), "light_blue")
        save_price_into__execl()

    if choice == "1" or choice == "2" or choice == "3":
        try:
            excel_data = read_exel()
            if excel_data is not None:
                if choice == "1":
                    try:
                        get_google_urls()
                        save_logs(urls=google_urls)
                    except Exception as e:
                        print("Google url ler getirilirken bir hata oluştu", e)
                        save_logs(urls=google_urls)
                elif choice == "2":
                    try:
                        get_google_urls()
                        get_amazon_product_names(urls=google_urls)
                        save_logs(urls=google_urls, amazon_names=amazon_data)
                        save_amazon_names_into_excel(amazon_data)
                    except Exception as e:
                        print("Amazon isimleri getirilirken bir hata oluştu", e)
                        save_logs(urls=google_urls, amazon_names=amazon_data)
                elif choice == "3":
                    try:
                        search_in_akakce()
                    except Exception as e:
                        print("Ak Akçe verileri getirilirken bir hata oluştu", e)
                        save_price_into__execl()

        except Exception as e:
            message = "Lütfen data.xlsx dosyasını oluşturun ve verileri girin."
            print(message)
            write_errors(message)
            input("Programı kapatmak için enter tuşuna basın..")
            exit()
    else:
        message = "Yanlış secenek. Lütfen 1, 2, veya 3. seçenekten birini seçin."
        print(message)
        write_errors(message)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Program {round(total_time/60, 1)} dakikada tamamlandı.")
    input("Programı kapatmak için enter tuşuna basın..")
except KeyboardInterrupt:
    print("Program kapatıldı.")
