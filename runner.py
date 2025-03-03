from behave.__main__ import main as behave_main
import sys
import subprocess
import time
import requests

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
        except:
            time.sleep(1)
    print("Appium sunucusu başlatılamadı!")
    return None

def determine_platform_from_tags(tags):
    """Tag'lerden platformu belirler."""
    if not tags or not tags.startswith('--tags='):
        return None
    tag_value = tags.replace('--tags=', '')
    if 'web_safari' in tag_value:
        return 'safari'
    if 'android' in tag_value:
        return 'android'
    return None

if __name__ == '__main__':
    appium_process = None

    # Tag'leri al
    if len(sys.argv) > 1 and sys.argv[1].startswith('--tags='):
        tags = sys.argv[1]
    else:
        tags_input = input("Çalıştırmak istediğiniz tag'i girin (boş bırakılırsa tüm testler çalıştırılır): ").strip()
        tags = '--tags=' + tags_input if tags_input else None

    # Tag'lerden platformu çıkar
    platform = determine_platform_from_tags(tags)

    # Platforma göre yalnızca Appium'u başlat (Safari için driver environment.py'da başlatılacak)
    if platform == 'android':
        appium_process = start_appium()
        if not appium_process:
            sys.exit("Appium başlatılamadığı için testler çalıştırılamıyor!")
    elif platform == 'safari':
        print("Safari testi seçildi, driver environment.py'da başlatılacak.")
    else:
        print("Platform belirlenemedi! Tag'lerde 'android' veya 'web_safari' kullanın.")
        sys.exit(1)

    try:
        behave_args = [tags] if tags else []
        # Platformu behave_args ile geçmek yerine, environment.py'da kullanılmak üzere bir user data ekliyoruz
        if platform:
            behave_args.append(f"--define=platform={platform}")
        print(f"🔎 Çalıştırılan Behave Komutu: behave {' '.join(behave_args)}")
        behave_main(behave_args)
    
    finally:
        if appium_process:
            appium_process.terminate()
            print("Appium sunucusu kapatıldı!")