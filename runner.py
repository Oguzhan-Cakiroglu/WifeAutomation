from behave.__main__ import main as behave_main
import sys
import subprocess
import time
import requests

def is_appium_running():
    """Appium'un çalışıp çalışmadığını kontrol eder."""
    try:
        response = requests.get('http://localhost:4723/status', timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False

def start_appium():
    """Appium sunucusunu başlatır."""
    if not is_appium_running():
        print("Appium sunucusu başlatılıyor...")
        process = subprocess.Popen(['appium'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        for _ in range(30):
            if is_appium_running():
                print("Appium sunucusu başarıyla başlatıldı!")
                return process
            time.sleep(1)
        
        print("Appium sunucusu başlatılamadı!")
        return None
    else:
        print("Appium sunucusu zaten çalışıyor.")
        return None

if __name__ == '__main__':
    appium_process = start_appium()

    try:
        if len(sys.argv) > 1:
            tags = sys.argv[1]
        else:
            tags = input("Çalıştırmak istediğiniz tag'i girin (boş bırakılırsa tüm testler çalıştırılır): ").strip()

        behave_args = []
        if tags:
            behave_args = ['--tags=' + tags]  # <-- BURADA HATA VARDI, DÜZELTİLDİ.

        print(f"🔎 Çalıştırılan Behave Komutu: behave {' '.join(behave_args)}")
        behave_main(behave_args)
    
    finally:
        if appium_process:
            appium_process.terminate()
            print("Appium sunucusu kapatıldı!")