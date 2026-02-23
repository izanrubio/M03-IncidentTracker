from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class SecurityTest(TestCase):
    def setUp(self):
        # 1. Creem un usuari normal que NO és superusuari
        self.user = User.objects.create_user(username='victim_izaan', password='password123')
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()

    def test_privilege_escalation_vulnerability(self):
        # 2. Loguegem l'usuari per poder accedir a la vista @login_required
        self.client.login(username='victim_izaan', password='password123')

        # 3. Payload maliciós (el mateix que has fet servir tu)
        # Tanca la cometa i injecta el canvi de permisos
        payload = "hacker@izaan.com', is_superuser = true, is_staff = true --"

        # 4. Simulem la petició GET a la vista vulnerable d'actualitzar correu
        response = self.client.get(reverse('actualitzar_correu'), {'email': payload})

        # 5. Refresquem l'usuari de la base de dades
        self.user.refresh_from_db()

        # 6. L'ASSERT: Verifiquem que l'usuari NO hauria de ser superusuari.
        # Com que el codi encara és vulnerable, aquest assert FALLARÀ.
        self.assertFalse(self.user.is_superuser, "SEGURETAT CRÍTICA: L'usuari ha aconseguit escalada de privilegis!")
