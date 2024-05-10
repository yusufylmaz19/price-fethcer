# Akakçe Ürün Karşılaştırma Scripti

Bu Python scripti, belirli `EAN` kodlarına sahip ürünleri Akakçe'de arar ve benzer ürünleri bulmaya çalışır. Bulunan ürünlerin isimlerini, fiyatlarını ve Akakçe linklerini sağlar. Sonuçları bir Excel dosyasına kaydeder. Ayrıca `isbn` kodalarına göre googlda arama yaparak amazon ürün isimlerini de bulup Excel dosyasına kaydeder.

## Çalıştırma Senaryoları

### Eğer script olarak çalıştırmak isterseniz aşağıdaki [Kurulum](#kurulum)  ve [Kullanım](#kullanım) adımlarını takip edin.

- Not: Size verilen script dosyası ile sizin excel dosyası aynı dizinde olmak zorundadır. Aksi durumda program çalışmayacaktır.

### Eğer exe olarak çalıştırmak isterseniz size verilen dosyaları bir klasöre atman ve [Kullanım](#kullanım) adımlarını takip edin.

- Not: Size verilen exe dosyası ile sizin excel dosyası aynı dizinde olmak zorundadır. Aksi durumda program çalışmayacaktır.

## Kurulum

1. Python'un sisteminizde yüklü olduğundan emin olun. Python'un resmi web sitesinden [buradan](https://www.python.org/downloads/) indirebilirsiniz.

2. Pip'in sisteminizde yüklü olduğundan emin olun. Pip, Python paketlerini yönetmek için kullanılan bir paket yöneticisidir. Python'un yüklü olduğu durumlarda genellikle otomatik olarak yüklenir.

3. Aşağıdaki paketleri pip kullanarak yükleyin:

   ```shell
   pip install openpyxl
   pip install pandas
   pip install tabulate
   pip install google
   pip install beautifulsoup4
   pip install requests
   ```

4. Aynı dizine `data.xlsx` adında bir Excel dosyası ekleyin. Bu dosya, aramak istediğiniz ürünlerin EAN kodlarını ve isimlerini içermelidir. Sutun başlıkları `EAN` ve `Marka_Model` olmalıdır.Dilerseniz kod içinde bulunan sutun başlıklarını excel dosyasına göre değiştirebilirsiniz.

## Kullanım

#### Script Olarak Çalıştırma

1. Komut istemcisinde, scriptin bulunduğu dizine gidin.

2. Aşağıdaki komutu çalıştırarak scripti başlatın:

   ```shell
   python3 index.py veya python index.py
   ```

3. Size 3 adet secenek sunulacaktır.

- İlk seçenek google'da arama yaparak url'leri bulur ve log dosyasına yazar.
- İkinci seçenek ise url'leri kullanarak amazon'da arama yapar ve buluduğu isimleri log dosyasına yazar ve excel dosyasına `Marka_Model` olarak kayıt eder.
- Üçüncü seçenek ise Akakçe'de arama yapar ve bulduğu ürünleri ve excel dosyasına `AKAKÇE FiYATI`, `AKAKÇE ADI` ve `AKAKÇE LİNKİ` olarak kayıt eder.

#### Exe Olarak Çalıştırma

1. Size verilen exe dosyasını çalıştırın.
   ```shell
   start index.exe veya index.exe üzerine çift tıklayın.
   ```

## Notlar

- Kod içinde karşılaştırma yapılırken Akakçe'nin bize sağladığı JSON verileri kullanılmıştır. Bu verilerin yapısı değişirse, kodun çalışmama ihtimali vardır. Bu durumda kodun güncellenmesi gerekecektir.

- Mevcut yanıtta Akakçe'nin `EAN` koduna göre birebir eşleşme yapılmamaktadır. Bu nedenle, Excel dosyasındaki ürün isimlerine göre karşılaştırma yapılarak en yakın ürünler bulunmaktadır. Bu durumda, ürün isimlerinin doğru ve eksiksiz olması gerekmektedir.
