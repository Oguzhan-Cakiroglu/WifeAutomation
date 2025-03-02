Feature: Chrome ve Google Testi
  Kullanıcı olarak Chrome'u açıp farklı sayfalara gidebilmek istiyorum

  @android_google
  Scenario: Chrome'u açıp Google'a git
    Given Chrome tarayıcısı açık
    When Google.com adresine gidilir

  @android_python
  Scenario: Chrome'u açıp Python.org adresine git
    Given Chrome tarayıcısı açık
    When Python.org adresine gidilir