Feature: Chrome ve Google Testi
  Kullanıcı Testleri
  @android_google
  Scenario: Chrome'u açıp Google'a git
    Given Chrome tarayıcısı açık
    When Google.com adresine gidilir

  @android_python
  Scenario: Chrome'u açıp Python.org adresine git
    Given Chrome tarayıcısı açık
    When Python.org adresine gidilir