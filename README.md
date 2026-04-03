# Windows 10/11 Watermark Hider / Su İzi Gizleyici

🌍 *[Read in English](#english)* | 🇹🇷 *[Türkçe okumak için aşağı kaydırın](#türkçe)*

---

## English

A standalone, bilingual (English & Turkish) Python GUI application designed to hide the persistent "Activate Windows" watermark by safely disabling the `svsvc` (Spot Verifier Service) in the Windows Registry.

### Features
- **Graphic User Interface (GUI):** A clean classic dark-theme GUI built natively with Tkinter.
- **Automatic Privilege Escalation:** Automatically triggers User Account Control (UAC) to run as an Administrator if not already elevated.
- **Bilingual Interface (TR/EN):** Automatically detects the Windows system UI language and displays the interface in either English or Turkish.
- **Console Hiding:** Uses Windows CTypes API to seamlessly suppress the background command terminal.

### How It Works
The script modifies the following Registry key:
`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\svsvc`

It changes the `Start` value to `4` (Disabled), which hides the persistent activation watermark usually found in the bottom right corner of unactivated Windows instances.

### Prerequisites
- Windows 10 or Windows 11
- Python 3.x installed (Standard libraries only; no `pip install` required)

### Usage
1. Clone the repository or download the script.
2. Run the script via command line or double click:
   ```cmd
   python windos11-10key.py
   ```
3. A Windows UAC dialog will prompt you to run as Administrator. Click **Yes**.
4. Click the **Remove Watermark** button on the GUI.
5. Once success is confirmed, click the **Restart** button to apply the changes.

### Disclaimer
This script modifies the Windows Registry. While disabling `svsvc` is a known method to hide the watermark, modify your registry at your own risk. This does **not** illegally activate Windows; it simply hides the UI watermark text.

### Author & Credits
- **Old / Main GitHub Account:** [zPeaw](https://github.com/zPeaw)
- **New Active GitHub Account:** [kmertkun](https://github.com/kmertkun) *(Currently in use due to lost credentials for the main account)*

---

## Türkçe

Windows Kayıt Defteri'ndeki `svsvc` (Spot Verifier Service) hizmetini kapatarak sağ alttaki can sıkıcı "Windows'u Etkinleştir" su izini (filigranını) kaldıran yerleşik ve açık kaynaklı bir Python aracıdır.

### Özellikler
- **Karanlık Tema Arayüz:** Modern "Dark Theme" görünümlü, kullanımı çok basit bir klasik Tkinter şablonu.
- **Otomatik Yönetici (Admin) İzni:** Betik açıldığında kendi kendine sağ tıklamaya gerek bıraktırmadan "Yönetici Olarak Çalıştır" (UAC) onay penceresini tetikler.
- **Bağımsız Çalışma:** Arkadaki siyah CMD/Terminal konsol penceresini kodu çalıştırır çalıştırmaz gizler.
- **Otomatik Dil Seçimi:** Bilgisayarın yerel işletim sistemi dilini tarar (İngilizce ise İngilizce arayüz, Türkçe ise Türkçe arayüz çıkarır).

### Kurulum ve Kullanım
*Sadece Python 3 kurulu bir Windows sisteme ihtiyacınız var, ek hiçbir eklenti kurmanıza gerek yoktur.*

1. Projeyi bilgisayarınıza indirin.
2. `windos11-10key.py` dosyasına çift tıklayın veya komut satırından çalıştırın:
   ```cmd
   python windos11-10key.py
   ```
3. Çıkan yönetici onay penceresinde "Evet" (Yes) seçeneğine tıklayın.
4. Çıkan arayüzde **Filigranı Gizle** butonuna basın.
5. İşlem bittikten sonra **Bilgisayarı Yeniden Başlat** butonuna basarak sistemi yeniden başlatın. Etkinleştirme yazısı yok olmuş olacaktır.

### Sorumluluk Reddi
Bu araç Windows kayıt defterinde (Registry) değişiklik yapar. Uygulamayı kullanmak kendi sorumluluğunuzdadır. Bu araç Windows'u yasadışı olarak etkinleştirmez, yalnızca sağ alttaki yazıyı gizler.

### Geliştirici & İletişim
- **Ana / Eski GitHub Hesabı:** [zPeaw](https://github.com/zPeaw)
- **Yeni Aktif GitHub Hesabı:** [kmertkun](https://github.com/kmertkun) *(Eski hesabın erişimi kaybedildiği için güncel olarak bu hesap kullanılmaktadır)*
