from behave.__main__ import main as behave_main
import sys
import subprocess
import time
import requests
import threading

def start_appium():
    """Appium sunucusunu başlatır."""
    print("Appium sunucusu başlatılıyor...")
    process = subprocess.Popen(['appium'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for _ in range(30):
        try:
            response = requests.get('http://localhost:4723/status', timeout=2)
            if response.status_code == 200:
                print("Appium sunucusu başarıyla başlatıldı!")
                return process
        except requests.RequestException:
            time.sleep(1)
    print("Appium sunucusu başlatılamadı!")
    return None

def determine_platforms_from_tags(tags):
    """Tag'lerden platformları belirler."""
    if not tags or not tags.startswith('--tags='):
        return []
    
    tag_value = tags.replace('--tags=', '')
    platforms = []
    
    if 'web_safari' in tag_value:
        platforms.append('safari')
    if 'android' in tag_value:
        platforms.append('android')
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
        print("Platform belirlenemedi! Tag'lerde 'android', 'ios' veya 'web_safari' kullanın.")
        sys.exit(1)

    # Appium'u başlat (Sadece Android ve iOS için, Safari'de gerek yok)
    if 'android' in platforms or 'ios' in platforms:
        appium_process = start_appium()
        if not appium_process:
            sys.exit("Appium başlatılamadığı için testler çalıştırılamıyor!")
        appium_processes.append(appium_process)

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
        print("Appium sunucusu kapatıldı!")