#https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

#Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

import pandas as pd
import datetime as dt

pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x:"%.3f" % x)

df_kopya = pd.read_excel("online_retail_II.xlsx" , sheet_name="Year 2009-2010")

df = df_kopya.copy()

df.head() #veriye göz attım.

# Değişkenler

# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.

#Neler gözlemledim?
#Invoice değişkeni çoklama durumunda çünkü faturada birden fazla ürün olabilir.
#Bir ürüne toplam ne kadar ödendiğini bulmak için Price*Quantity işlemi yapılmalıdır.
#Bir faturada toplam ne kadar olduğunu bulmak için aynı olan invoice bedelleri toplanmalıdır.


df.shape
df.isnull().sum() #eksik değerlere baktım.
#eksik değerleri silmeyi tercih edeceğim çünkü eksik olan şey müşteri ID'si. Dolayısıyla ölçülebilirlik taşımıyor.
df.dropna(inplace=True)

df["Description"].nunique() #essiz ürün sayısı nedir?

df["Description"].value_counts().head() #hangi üründen kaçar tane var?

df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity", ascending=False).head() #en çok şipariş edilen ürün hangisi?

df["Invoice"].nunique() #eşsiz fatura sayısı nedir?

#Fatura başına toplam ne kadar kazanıldı?
df["TotalPrice"] = df["Quantity"] * df["Price"]
df.groupby("Invoice").agg({"TotalPrice": "sum"}).head()
df.head()
#Sayısal değişkenlere göz attım.
df.describe().T


#Veri setinde sorunlar var, fiyat eksi olamaz, iadelerden kaynaklanıyor. Çözmek için iade olan faturaları veri setinden çıkardım.
df = df[~df["Invoice"].str.contains("C", na=False)]
df.head()
#RFM METRİKLERİNİN HESAPLANMASI

#Veri seti 2022 yılına göre oldukça eski olduğu için veri seti içindeki en son tarihe iki gün ekleyip analiz yapılan tarih olarak kabul ettim.

df["InvoiceDate"].max()
today_date = dt.datetime(2010, 12, 11)
type(today_date)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                     'Invoice': lambda Invoice: Invoice.nunique(),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

rfm.head()

#Sütun isimlerini RFM tablosuna uygun hale getirmek istiyorum.
rfm.columns = ["recency", "frequency", "monetary"]
rfm.head()

#Tekrar bir betimsel istatistiğine göz attım.
rfm.describe().T

#monetery değerinin min'de 0 olmasını istemediğim için silmek istiyorum.
rfm = rfm[rfm["monetary"] > 0]

#Son durumu incelemek istiyorum.
rfm.shape #4312 tane müşteriyi ve rfm metriklerini elde ettim.

#RFM SKORLARININ HESAPLANMASI

rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm.head()

#İki ayrı değişkende olan int değerleri str çevirip toplayarak yeni bir değişken haline getirdim.
rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str)+
                    rfm["frequency_score"].astype(str))

#En değerli müşterileri gözlemledim.
rfm[rfm["RFM_SCORE"] == "55"]

#Görece biraz daha az değerli olabilecek müşterileri gözlemledim.
rfm[rfm["RFM_SCORE"] == "11"]

#RFM SEGMENTLERİNİN OLUŞTURULMASI VE ANALİZİ

#Segmentleri sektörde kabul gören sınıf isimlerine göre isimlendirdim.
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

#Genel bir gözlem yapmak istedim. Segmentleri betimledim.
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

#Yeni müşterilerin id'lerini gözlemledim.
rfm[rfm["segment"] == "new_customers"].index

#işlemin sonucunu dışarı çıkarmak istiyorum.
new_df = pd.DataFrame()
new_df["new_customer_id"] = rfm[rfm["segment"] == "new_customers"].index
new_df["new_customer_id"] = new_df["new_customer_id"].astype(int)

new_df.to_csv("new_customers.csv")


#Genelleştirmek için fonskiyon yazdım.
def create_rfm(dataframe, csv=False):

    # Öncelikle veriyi hazırladım.
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]

    # RFM metriklerini hesapladım
    today_date = dt.datetime(2011, 12, 11)
    rfm = dataframe.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
    rfm.columns = ['recency', 'frequency', "monetary"]
    rfm = rfm[(rfm['monetary'] > 0)]

    # RFM skorlarını hesapladım
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

    # cltv_df skorlarını kategorik değere dönüştürüp df'e ekledim
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                        rfm['frequency_score'].astype(str))


    # segmentleri isimlendirdim
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
    rfm = rfm[["recency", "frequency", "monetary", "segment"]]
    rfm.index = rfm.index.astype(int)

    if csv:
        rfm.to_csv("rfm.csv")

    return rfm

