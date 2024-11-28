import os
import shutil
import logging
from datetime import datetime

def dosyalari_duzenle(klasor_yolu):
    # Günlük kaydı ayarları
    logging.basicConfig(
        filename=f'dosya_duzenleme_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Dosya türleri ve uzantıları
    dosya_turleri = {
        'Resimler': ['.jpeg', '.jpg', '.png', '.gif'],
        'Videolar': ['.mp4', '.avi', '.mov'],
        'Belgeler': ['.pdf', '.docx', '.txt'],
        'Arsivler': ['.zip', '.rar'],
        'Diger': []  # Tanınmayan dosya türleri için
    }

    try:
        # Klasörün var olup olmadığını kontrol et
        if not os.path.exists(klasor_yolu):
            raise FileNotFoundError(f"'{klasor_yolu}' klasörü bulunamadı!")

        for dosya_adi in os.listdir(klasor_yolu):
            dosya_yolu = os.path.join(klasor_yolu, dosya_adi)
            
            if os.path.isfile(dosya_yolu):
                uzanti = os.path.splitext(dosya_adi)[1].lower()
                
                # Hedef klasörü belirle
                hedef_klasor_adi = 'Diger'
                for klasor_adi, uzantilar in dosya_turleri.items():
                    if uzanti in uzantilar:
                        hedef_klasor_adi = klasor_adi
                        break

                hedef_klasor = os.path.join(klasor_yolu, hedef_klasor_adi)
                os.makedirs(hedef_klasor, exist_ok=True)

                # Aynı isimli dosya varsa yeni isim ver
                yeni_dosya_adi = dosya_adi
                sayac = 1
                while os.path.exists(os.path.join(hedef_klasor, yeni_dosya_adi)):
                    ad, uzanti = os.path.splitext(dosya_adi)
                    yeni_dosya_adi = f"{ad}_{sayac}{uzanti}"
                    sayac += 1

                # Dosyayı taşı
                try:
                    shutil.move(dosya_yolu, os.path.join(hedef_klasor, yeni_dosya_adi))
                    logging.info(f'{dosya_adi} dosyası {hedef_klasor_adi} klasörüne taşındı')
                    if yeni_dosya_adi != dosya_adi:
                        logging.info(f'Çakışmayı önlemek için {yeni_dosya_adi} olarak yeniden adlandırıldı')
                except Exception as e:
                    logging.error(f'{dosya_adi} taşınırken hata oluştu: {str(e)}')

    except Exception as e:
        logging.error(f'Klasör düzenlenirken hata oluştu: {str(e)}')
        raise

if __name__ == "__main__":
    try:
        # Burada kendi klasör yolunuzu belirtin
        dosyalari_duzenle('C:\\Users\\LENOVO\\Downloads')
        # VEYA
        # dosyalari_duzenle('/home/kullaniciadi/Downloads')  # Linux/Mac için örnek
        print("Düzenleme tamamlandı! Ayrıntılar için günlük dosyasını kontrol edin.")
    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")
