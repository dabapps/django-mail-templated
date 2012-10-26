import re

from django.conf import settings
if not settings.configured:
    settings.configure(DATABASES={'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db'}})
from django.core.mail.backends.base import BaseEmailBackend
from django.template.loader import get_template_from_string
from django.test import TestCase
from django.test.utils import override_settings

import mail_templated
from mail_templated import EmailMessage, send_mail


TEMPLATES = {
    'plain':'''
        {% block subject %}Plain message{% endblock %}

        {% block body %}
        This is
        plain text
        {% endblock %}
        ''',

}

def get_template(template_name):
    """
    Returns a compiled Template object for the given template name
    from TEMPLATES dict.

    This is used to patch the origin django function for testing purposes.
    """
    content = TEMPLATES[template_name]
    content = re.sub(r'^ {8}', '', content)
    return get_template_from_string(content)


class TestEmailBackend(BaseEmailBackend):

    def send_messages(self, email_messages):
        """Just returns content of messages."""
        if not email_messages:
            return
        return [message.message().as_string() for message in email_messages]


@override_settings(EMAIL_BACKEND = 'mail_templated.tests.TestEmailBackend')
class EmailTestCase(TestCase):

    def setUp(self):
        # Patch get_template() to load templates from TEMPLATES dict instead
        # of file system.
        self._origin_get_template = mail_templated.get_template
        mail_templated.get_template = get_template

    def tearDown(self):
        mail_templated.get_template = self._origin_get_template

    def test_plain(self):
        result = send_mail('plain', {}, 'from@inter.net', ['to@inter.net'])
        self.assertEqual(len(result), 1)
        self.assertNotEqual(result[0], '')