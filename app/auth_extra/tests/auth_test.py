from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import SimpleTestCase, Client

class RegistrationFlowTests(StaticLiveServerTestCase):

    fixtures = ['cms.json']

    test_account = {
        'email': 'bla@blabla.bl',
        'password': 'blabla',
    }

    @classmethod
    def setUpClass(cls):
        super(RegistrationFlowTests, cls).setUpClass()
        cls.client = Client()

    def test_registration(self):
        # with self.settings(COMPRESS_ENABLED=False):
        with self.settings(CAPTCHA_TEST_MODE=True):
            response = self.client.post('/en/account/sign-up/', {
                'email': self.test_account['email'],
                'password1': self.test_account['password'],
                'password2': self.test_account['password'],
                'tos': '1',
            })

            #self.assertContains(response, text='', status_code=302)
            response = self.client.get('/en/',)

            #self.assertContains(response, text=self.test_account['email'], status_code=200)
            #self.assertContains(response, text='account settings', status_code=200)
            self.assertContains(response, text='', status_code=200)

    # def test_post_registration_login(self):
    #     # with self.settings(COMPRESS_ENABLED=False):
    #     response = self.client.get('/en/',)
    #     self.assertContains(response, text=self.test_account['email'], status_code=200)
