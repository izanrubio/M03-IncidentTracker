import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


class SecurityRegressionTests(StaticLiveServerTestCase):
    fixtures = ['testdb.json']  # Càrrega de dades (Punt 2.2.2)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.add_argument("--headless")  # mode Headless (Punt 2.2.1)

        # Detectem si estem en local (Firefox snap) o al runner de CI (APT/system Firefox)
        SNAP_FIREFOX = "/snap/firefox/current/usr/lib/firefox/firefox"
        if os.path.exists(SNAP_FIREFOX):
            # Màquina local amb Firefox instal·lat com a snap
            opts.binary_location = SNAP_FIREFOX

        # Si el binary_location NO s'estableix, Selenium el cerca al PATH del sistema
        # (comportament correcte a GitHub Actions runner d'Ubuntu)
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_role_restriction(self):
        """AUDITORIA: L'analista no ha d'entrar a /admin/"""
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))

        # PUNT 2.2.3: Implementa el login amb 'analista1'
        self.selenium.find_element(By.NAME, "username").send_keys("analista1")
        self.selenium.find_element(By.NAME, "password").send_keys("analista1")
        self.selenium.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Intentar forçar URL d'admin
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))

        # ASSERT de Seguretat (Punt 2.2.3)
        # Si l'analista té is_staff=True, Django el deixarà entrar i el títol serà
        # "Site administration | Django site admin" → el test FALLARÀ (Fase RED).
        # Si l'analista NO té is_staff ni is_superuser, Django el redirigirà al login
        # i el títol serà diferent → el test PASSARÀ (Fase GREEN).
        self.assertNotEqual(
            self.selenium.title,
            "Site administration | Django site admin",
            "SEGURETAT: L'analista1 ha accedit al panell d'administració!"
        )
