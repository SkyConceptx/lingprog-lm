from django.core import mail
from django.test import TestCase
from lingprog.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """"O teste deve obter o formulário de inscrição e retornar o status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Devemos utilizar o template subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """O código HTML deverá conter marcações Django de entrada (input) de dados!"""
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """O HTML deve conter csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """O formulário deve ter uma assinatura no seu contexto"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_field(self):
        """o formulário deverá ter 4 campos"""
        form = self.response.context['form']
        self.assertSequenceEqual(['nome', 'titulo', 'email', 'resumo'], list(form.fields))

class SubscribePostTest(TestCase):
    def setUp(self):
        """Se válido, deve ser redirecionado para a /inscricao"""
        dados = dict(nome='Zezin', titulo='Quero me Inscrever', email='zezin@silva.com', resumo='Quero me inscrever no curso')
        self.response = self.client.post('/inscricao/', dados)

    def test_post(self):
        # 302 é o código de status para redirecionamento de página
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscribe_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmacao de inscricao'

        self.assertEqual(expect, email.subject)

    def test_subscribe_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@lingprog.com.br'

        self.assertEqual(expect, email.from_email)

    def test_subscribe_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@lingprog.com.br', 'zezin@silva.com']

        self.assertEqual(expect, email.to)

    def test_subscribe_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Zezin', email.body)
        self.assertIn('Quero me Inscrever', email.body)
        self.assertIn('zezin@silva.com', email.body)
        self.assertIn('Quero me inscrever no curso', email.body)

class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})
    def test_post(self):
        """Se a postagem de dados for inválida não haverá redirecionamento"""


        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')
