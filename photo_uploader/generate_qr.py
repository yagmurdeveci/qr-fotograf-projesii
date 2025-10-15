import qrcode
import socket

def get_local_ip():
    """Bilgisayarın yerel IP adresini bulur."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Bu IP'ye bağlanmaya çalışmaz, sadece en uygun arayüzü bulur
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1' # Bulunamazsa localhost döner
    finally:
        s.close()
    return IP

# !!! DİKKAT: Buradaki IP adresini kendi bilgisayarınızın IP adresi ile değiştirmelisiniz.
# Telefonunuz ve bilgisayarınız AYNI Wi-Fi ağında olmalıdır.
# get_local_ip() fonksiyonu genellikle doğru IP'yi bulur.
YOUR_COMPUTER_IP = get_local_ip() 
PORT = 5000

# QR kodun yönlendireceği tam adres
url = f" 192.168.1.101/5000"

# QR kodu oluştur
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

# QR kodunu bir dosya olarak kaydet
img.save("upload_qr_code.png")

print(f"QR Kod oluşturuldu: upload_qr_code.png")
print(f"Bu kod şu adrese yönlendiriyor: {url}")
print("Sunucuyu başlatmadan önce telefonunuzun ve bilgisayarınızın aynı Wi-Fi ağında olduğundan emin olun!")