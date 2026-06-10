import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="İzmir GES Yer Seçimi Analizi", layout="wide")

st.title("☀️ İzmir Güneş Enerjisi Santrali (GES) Dinamik Yer Seçimi Uygulaması")
st.markdown("Tez kapsamında geliştirilen Çok Kriterli Karar Analizi (MCDA) simülasyon paneli. Soldaki kriter ağırlıklarını değiştirerek bölgelerin uygunluk durumunu dinamik olarak inceleyebilirsiniz.")

# Sol Panel: Kriter Ağırlıkları (Kullanıcı Etkileşimi)
st.sidebar.header("Kriter Ağırlıklarını Belirle (%)")
st.sidebar.markdown("Toplam ağırlık 100 olmalıdır.")

w_gunes = st.sidebar.slider("Güneşlenme Süresi Ağırlığı", 0, 100, 35)
w_egim = st.sidebar.slider("Eğim Durumu Ağırlığı", 0, 100, 20)
w_trafo = st.sidebar.slider("Trafo Merkezine Uzaklık", 0, 100, 20)
w_baki = st.sidebar.slider("Bakı (Güney Yönelim) Ağırlığı", 0, 100, 15)
w_yol = st.sidebar.slider("Yollara Uzaklık Ağırlığı", 0, 100, 10)

toplam_agirlik = w_gunes + w_egim + w_trafo + w_baki + w_yol

if toplam_agirlik != 100:
    st.sidebar.error(f"⚠️ Dikkat: Toplam ağırlık %100 olmalıdır! Şu anki toplam: %{toplam_agirlik}")
else:
    st.sidebar.success("✅ Ağırlık dağılımı dengeli. Model hesaplanıyor...")

# Bölgelerin Ham CBS Analiz Puanları [Enlem, Boylam, Güneş, Eğim, Trafo, Bakı, Yol]
bolgeler = {
    "Bergama": [39.1211, 27.1774, 85, 90, 60, 80, 75],
    "Torbalı": [38.1612, 27.3636, 80, 85, 85, 75, 90],
    "Menderes": [38.2510, 27.1350, 82, 75, 70, 70, 80],
    "Aliağa": [38.7997, 26.9717, 75, 80, 95, 65, 95],
    "Çeşme": [38.3227, 26.3031, 90, 50, 50, 60, 70]
}

# Skora göre renk belirleme fonksiyonu
def renk_getir(skor):
    if skor >= 80: return "#22c55e"  # Canlı Yeşil (Çok Uygun)
    elif skor >= 70: return "#eab308"  # Sarı (Uygun)
    else: return "#ef4444"  # Kırmızı (Az Uygun / Uygun Değil)

# Sağ Panel: Harita ve Skor Listesi
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("İzmir Dinamik Uygunluk Haritası")
    # İzmir merkezli folium haritası
    m = folium.Map(location=[38.4237, 27.1428], zoom_start=9, tiles="CartoDB positron")
    
    # Her bölge için dinamik skor hesaplama ve haritaya basma
    for isim, veri in bolgeler.items():
        # Matematiksel MCDA Ağırlıklandırma Formülü
        hesaplanan_skor = (veri[2]*w_gunes + veri[3]*w_egim + veri[4]*w_trafo + veri[5]*w_baki + veri[6]*w_yol) / 100
        
        folium.CircleMarker(
            location=[veri[0], veri[1]],
            radius=18,
            popup=f"<b>{isim}</b><br>MCDA Uygunluk Skoru: {hesaplanan_skor:.1f}/100",
            color=renk_getir(hesaplanan_skor),
            fill=True,
            fill_color=renk_getir(hesaplanan_skor),
            fill_opacity=0.7
        ).add_to(m)
    
    st_folium(m, width=800, height=500)

with col2:
    st.subheader("Anlık Bölge Skorları")
    for isim, veri in bolgeler.items():
        hesaplanan_skor = (veri[2]*w_gunes + veri[3]*w_egim + veri[4]*w_trafo + veri[5]*w_baki + veri[6]*w_yol) / 100
        st.metric(label=f"{isim} Bölgesi", value=f"{hesaplanan_skor:.1f} / 100")
        st.progress(int(hesaplanan_skor))
