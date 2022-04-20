#https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

#Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

#Veri setine göz attım.
![1](https://user-images.githubusercontent.com/101973346/164128665-417315fb-bab3-4ab4-97fb-7d700b74ea06.png)

# Değişkenler
#InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
#StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
#Description: Ürün ismi
#Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
#InvoiceDate: Fatura tarihi ve zamanı.
#UnitPrice: Ürün fiyatı (Sterlin cinsinden)
#CustomerID: Eşsiz müşteri numarası
#Country: Ülke ismi. Müşterinin yaşadığı ülke.

# Neler gözlemledim?
#Invoice değişkeni çoklama durumunda çünkü faturada birden fazla ürün olabilir.
#Bir ürüne toplam ne kadar ödendiğini bulmak için Price*Quantity işlemi yapılmalıdır.
#Bir faturada toplam ne kadar olduğunu bulmak için aynı olan invoice bedelleri toplanmalıdır.

# eksik değerlere baktım.
![5](https://user-images.githubusercontent.com/101973346/164128801-b77bbea6-892b-4751-a4a2-8895bce85792.png)

#eksik değerleri silmeyi tercih edeceğim çünkü eksik olan şey müşteri ID'si. Dolayısıyla ölçülebilirlik taşımıyor.
![9](https://user-images.githubusercontent.com/101973346/164128887-f31bd0a5-178e-445d-9241-6af5bdc543e5.png)

#essiz ürün sayısı nedir?
![51](https://user-images.githubusercontent.com/101973346/164128954-a7e68676-a27d-4922-a532-ba7e5e7a5d99.png)

#hangi üründen kaçar tane var?
![3](https://user-images.githubusercontent.com/101973346/164129119-5f879085-9c68-49da-941d-d03969980c42.png)

#en çok şipariş edilen ürün hangisi?
![8](https://user-images.githubusercontent.com/101973346/164129085-384759e9-594e-4b80-a86b-d667805a23d2.png)

#Fatura başına toplam ne kadar kazanıldı?
![c](https://user-images.githubusercontent.com/101973346/164129187-d7828409-21f2-410f-aee7-314ef3808055.png)

#Sayısal değişkenlere göz attım.
![vv](https://user-images.githubusercontent.com/101973346/164129273-c39d86ab-369e-47d1-8d5d-0ace35f89ec2.png)

#Veri setinde sorunlar var, fiyat eksi olamaz, iadelerden kaynaklanıyor. Çözmek için iade olan faturaları veri setinden çıkardım.
![vvv](https://user-images.githubusercontent.com/101973346/164129355-e5b2ce03-68c8-473b-adf4-192d10683e31.png)

# RFM METRİKLERİNİN HESAPLANMASI

#Veri seti 2022 yılına göre oldukça eski olduğu için veri seti içindeki en son tarihe iki gün ekleyip analiz yapılan tarih olarak kabul ettim.
![bv](https://user-images.githubusercontent.com/101973346/164129440-aa6444a6-69f0-4432-8262-3360cc889d5e.png)

#İşlemleri yaptım.
![gf](https://user-images.githubusercontent.com/101973346/164129507-2ca5b22c-bee0-4930-ba00-d4ae2ec6e311.png)

#Sütun isimlerini RFM tablosuna uygun hale getirmek istiyorum.
![ffff](https://user-images.githubusercontent.com/101973346/164129609-d4e5c849-b8f0-41ec-af59-8732b9a29866.png)

#Tekrar bir betimsel istatistiğine göz attım.
![dddd](https://user-images.githubusercontent.com/101973346/164129679-59d2ab82-facc-477e-b137-d2ded8063021.png)

#monetery değerinin min'de 0 olmasını istemediğim için silmek istiyorum.
![ds](https://user-images.githubusercontent.com/101973346/164129798-2df88e9e-f27c-4816-801f-64ecb6d7661c.png)

#Son durumu incelemek istiyorum. 
![dsa](https://user-images.githubusercontent.com/101973346/164129853-f54b0946-6398-44ef-933f-47745ffeff23.png)
#4312 tane müşteriyi ve rfm metriklerini elde ettim.


# RFM SKORLARININ HESAPLANMASI

![ll](https://user-images.githubusercontent.com/101973346/164129952-0555e130-1bdd-469c-85ea-651467d343c6.png)

#İki ayrı değişkende olan int değerleri str çevirip toplayarak yeni bir değişken haline getirdim.
![ddw](https://user-images.githubusercontent.com/101973346/164130066-1c0cd361-d7b6-4aac-8964-b167a70895e9.png)

#En değerli müşterileri gözlemledim.
![g](https://user-images.githubusercontent.com/101973346/164130193-ce887f3b-1a7b-44e7-b12f-1b4627300385.png)
![gg](https://user-images.githubusercontent.com/101973346/164130205-f2db11e5-01b5-4156-986f-98fc327c8d50.png)

#Görece biraz daha az değerli olabilecek müşterileri gözlemledim.
![m](https://user-images.githubusercontent.com/101973346/164130301-3597bbff-c53a-4fb6-ad3c-c65c91c0a15f.png)
![mm](https://user-images.githubusercontent.com/101973346/164130311-ff8bd5e2-bb9e-47e2-b991-364611226fe0.png)

# RFM SEGMENTLERİNİN OLUŞTURULMASI VE ANALİZİ

#Segmentleri sektörde kabul gören sınıf isimlerine göre isimlendirdim.
![j](https://user-images.githubusercontent.com/101973346/164130531-ef0bf7ae-4b5a-4da0-9b9b-d1ca1e9994c4.png)
![jj](https://user-images.githubusercontent.com/101973346/164130545-ca716821-ec6a-4b3a-9fa5-d02648ac7094.png)

#Genel bir gözlem yapmak istedim. Segmentleri betimledim.
![k](https://user-images.githubusercontent.com/101973346/164130729-d71559ee-0fd7-43e3-8647-f0ccd755f555.png)

#Yeni müşterilerin id'lerini gözlemledim.
![ş](https://user-images.githubusercontent.com/101973346/164130804-cbba522b-13e2-45da-8447-d600a1659ef4.png)

#işlemin sonucunu dışarı çıkarmak istiyorum.
![fgfgfgf](https://user-images.githubusercontent.com/101973346/164130866-fd152896-3d80-4589-9b46-7ec4a7c78831.png)


## Genelleştirmek için fonskiyon yazdım. ##
