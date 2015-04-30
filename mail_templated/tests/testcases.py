# -- coding: utf-8 --
from django.test import TestCase
from mail_templated import send_mail
from django.core import mail


class TestSendEmail(TestCase):

    def test_send_email(self):
        """ test we can send an email """
        send_mail('test_message.email', {'context_var': "1"}, "from_email", ["to_email"])
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        # now check the details are correct
        self.assertEqual(email.to[0], "to_email")
        self.assertEqual(email.from_email, "from_email")
        self.assertEqual(email.subject, "Test Message")
        self.assertEqual(email.template_name, "test_message.email")
        self.assertEqual(email.body, "Test Message Body")
        self.assertEqual(email.message().get_content_type(), "multipart/alternative")
        self.assertIn("<p>Test Message HTML</p>", email.message().as_string())

    def test_send_extended_email(self):
        """ test we can send an email """
        send_mail('test_message_extended.email', {'context_var': "1"}, "from_email", ["to_email"])
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        # now check the details are correct
        self.assertEqual(email.to[0], "to_email")
        self.assertEqual(email.from_email, "from_email")
        self.assertEqual(email.subject, "Test Message")
        self.assertEqual(email.template_name, "test_message_extended.email")
        self.assertEqual(email.body, "Test Message Body")
        self.assertEqual(email.message().get_content_type(), "multipart/alternative")
        self.assertIn("<p>Test Message HTML</p>", email.message().as_string())
