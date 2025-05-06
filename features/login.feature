Feature: Chrome ve Google Testi
  Kullanıcı Testleri
  @android1
  Scenario: Chrome'u açıp Google'a git
    Given Chrome tarayıcısı açık
    When Google.com adresine gidilir

  @android2
  Scenario: Chrome'u açıp Python.org adresine git
    Given Chrome tarayıcısı açık
    When Python.org adresine gidilir