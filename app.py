import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np

st.set_page_config(page_title="İzmir GES Yer Seçimi Analizi", layout="wide")

st.title("☀️ İzmir Güneş Enerjisi Santrali (GES) Dinamik Yer Seçimi Uygulaması")
st.markdown("Bitirme tezi kapsamında geliştirilen Çok Kriterli Karar Analizi (MCDA) aracı.")

# Sol Panel: Kriter Ağırlıkları (Kullanıcı Etkileşimi)
st.sidebar.header("Kriter Ağırlıklarını Belirle (%)")
st.sidebar.markdown("Toplam ağırlık 100 olmalıdır.")

w_gunes = st.sidebar.slider("Güneşlenme Süresi Ağırlığı", 0, 100, 35)
w_egim = st.sidebar.slider("Eğim Ağırlığı", 0, 100, 20)
w_trafo = st.sidebar.slider("Trafo Merkezine Uzaklık", 0, 100, 20)
w_yol = st.sidebar.slider("Yola Uzaklık", 0, 100, 10)
w_baki = st.sidebar.slider("Bakı (Güney Yönelim)", 0, 100, 15)

toplam_agirlik = w_gunes + w_egim + w_trafo + w_yol + w_baki

if toplam_agirlik != 100:
    st.sidebar.error(f"Hata: Toplam ağırlık 100 olmalı! Şu anki toplam: {toplam_agirlik}")
else:
    st.sidebar.success("Ağırlıklar geçerli. Harita güncelleniyor...")

# Sağ Panel: Harita Gösterimi
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Veri Yükleme")
    st.file_uploader("Eğim Haritası (TIFF) Yükle", type=["tif", "tiff"])
    st.file_uploader("Güneşlenme Haritası (TIFF) Yükle", type=["tif", "tiff"])
    st.button("Analizi Çalıştır")
    st.info("Not: Bu bir prototiptir. 'Analizi Çalıştır' butonu ile yüklenen raster dosyalar (örneğin numpy dizileri olarak) ağırlıklarla çarpılıp (Örn: Piksel_Degeri * w_egim) yeni bir uygunluk rasterı üretir.")

with col2:
    st.subheader("Sonuç Haritası: İzmir Uzamsal Dağılım")
    # İzmir merkezli interaktif Folium haritası oluşturma
    m = folium.Map(location=[38.4237, 27.1428], zoom_start=9, tiles="CartoDB positron")
    
    # Tezinde gösterebileceğin örnek bir uygunluk alanı (Örnek Poligon)
    folium.Polygon(
        locations=[[38.5, 27.1], [38.5, 27.3], [38.3, 27.2]],
        color="orange",
        fill=True,
        fill_color="orange",
        fill_opacity=0.5,
        tooltip="Örnek Yüksek Uygunluk Alanı"
    ).add_to(m)

    # Haritayı Streamlit içinde göster
    st_data = st_folium(m, width=900, height=500)