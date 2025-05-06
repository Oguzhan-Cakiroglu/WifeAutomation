from behave.__main__ import main as behave_main
import sys
import subprocess
import time
import requests
import threading

def start_appium(port):
    """Belirtilen portta Appium sunucusunu başlatır."""
    print(f"Appium sunucusu {port} portunda başlatılıyor...")
    process = subprocess.Popen(['appium', '--port', str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Appium'un başarılı bir şekilde başlamasını bekle
    for _ in range(30):
        try:
            response = requests.get(f'http://localhost:{port}/status', timeout=2)
            if response.status_code == 200:
                print(f"✅ Appium sunucusu {port} portunda başarıyla başlatıldı!")
                return process
        except requests.RequestException:
            time.sleep(1)
    
    print(f"❌ Appium sunucusu {port} portunda başlatılamadı!")
    return None

def determine_platforms_from_tags(tags):
    """Tag'lerden platformları belirler."""
    if not tags or not tags.startswith('--tags='):
        return []
    
    tag_value = tags.replace('--tags=', '')
    platforms = []
    
    if 'web_safari' in tag_value:
        platforms.append('safari')
    if 'android2' in tag_value:  # İki Android cihazını çalıştırmak için yeni tag
        platforms.extend(['android2'])
    if 'android1' in tag_value:  # Tek Android cihazı için
        platforms.append('android1')  # Varsayılan olarak android1
    if 'ios' in tag_value:
        platforms.append('ios')

    return platforms

def run_behave(tags, platform):
    """Belirtilen platform için Behave testlerini çalıştırır."""
    behave_args = [tags] if tags else []
    behave_args.append(f"--define=platform={platform}")
    
    print(f"🔎 {platform.upper()} için Behave Komutu: behave {' '.join(behave_args)}")
    behave_main(behave_args)

if __name__ == '__main__':
    appium_processes = []

    # Tag'leri al
    if len(sys.argv) > 1 and sys.argv[1].startswith('--tags='):
        tags = sys.argv[1]
    else:
        tags_input = input("Çalıştırmak istediğiniz tag'leri girin (boş bırakılırsa tüm testler çalıştırılır): ").strip()
        tags = '--tags=' + tags_input if tags_input else None

    # Tag'lerden platformları çıkar
    platforms = determine_platforms_from_tags(tags)

    if not platforms:
        print("Platform belirlenemedi! Tag'lerde 'android', 'android_both', 'ios' veya 'web_safari' kullanın.")
        sys.exit(1)

    # Appium'u başlat
    if 'android1' in platforms:
        appium_android1 = start_appium(4723)
        if not appium_android1:
            sys.exit("❌ Android1 için Appium başlatılamadığı için testler çalıştırılamıyor!")
        appium_processes.append(appium_android1)

    if 'android2' in platforms:
        appium_android2 = start_appium(4724)
        if not appium_android2:
            sys.exit("❌ Android2 için Appium başlatılamadığı için testler çalıştırılamıyor!")
        appium_processes.append(appium_android2)

    if 'ios' in platforms:
        appium_ios = start_appium(4725)  # iOS için farklı bir port
        if not appium_ios:
            sys.exit("❌ iOS için Appium başlatılamadığı için testler çalıştırılamıyor!")
        appium_processes.append(appium_ios)

    if 'safari' in platforms:
        print("Safari testi seçildi, driver environment.py'da başlatılacak.")

    # Testleri paralel çalıştır
    threads = []
    for platform in platforms:
        thread = threading.Thread(target=run_behave, args=(tags, platform))
        threads.append(thread)
        thread.start()

    # Tüm testlerin bitmesini bekle
    for thread in threads:
        thread.join()

    # Appium'u kapat
    for process in appium_processes:
        process.terminate()
        print("🚪 Appium sunucusu kapatıldı!")