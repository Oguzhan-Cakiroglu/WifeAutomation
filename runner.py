from appium import webdriver
from datetime import datetime
from behave.__main__ import main as behave_main
from appium import webdriver
import socket
from appium import webdriver
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_appium():
    from appium import webdriver
    
    # 4723 portunun kullanımda olup olmadığını kontrol et
    if is_port_in_use(4723):
        print("4723 portu zaten kullanımda. Mevcut Appium sunucusunu kullanılıyor.")
        return webdriver.Remote("http://localhost:4723/wd/hub")
    else:
        desired_caps = {
            "platformName": "Android",
            "automationName": "uiautomator2",
            "deviceName": "Android",
            "appPackage": "com.tokenflexapp.test",
            "appActivity": "com.tokenflexapp.MainActivity",
            "noReset": True
            # Diğer desired capabilities'leri de ekleyebilirsiniz
        }

        try:
            appium_driver = webdriver.Remote("http://localhost:4723/wd/hub/", desired_caps)
            print("Appium başarıyla başlatıldı.")
            return appium_driver
        except Exception as e:
            print("Appium başlatılırken bir hata oluştu:", e)
            return None

def runnerDivan(tokenflex_tag):
    appium_driver = start_appium()  # Appium'u başlat

    if appium_driver is None:
        print("Appium başlatılamadı. Senaryolar çalıştırılamıyor.")
        return

    divan_features_path = "./features/"
    options = f"--tags {tokenflex_tag} --no-skipped" 
    behave_command = options + divan_features_path
    print("running divan")  
    behave_main(behave_command)
    appium_driver.quit()  # Appium'u kapat

# Örnek kullanım
if __name__ == "__main__":
    runnerDivan("@mainDivan")
