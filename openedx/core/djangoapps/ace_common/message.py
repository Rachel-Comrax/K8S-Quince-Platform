"""
Base Message types to be used to construct ace messages.
"""

import html
from edx_ace.message import MessageType

from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers


class BaseMessageType(MessageType):  # lint-amnesty, pylint: disable=missing-class-docstring
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from_address = configuration_helpers.get_value('email_from_address')
        if from_address:
            self.options.update({'from_address': from_address})  # pylint: disable=no-member


    def personalize(self, recipient, language, user_context):                
        if user_context.get('course_name'):
            user_context['course_name'] = characters_to_replace(user_context['course_name'])
        return super().personalize(recipient, language, user_context)

def characters_to_replace(val):
    characters_to_replace = (
        ('<', ''),
        ('>', ''),
        ('&', '_'),
        ('"', '``'),
        ("'", '`'),
        (")", ' '),
        ("(", ' '),
    )
    val = html.unescape(val) # convert HTML-escaped string to its original form
    for old_char, new_char in characters_to_replace:
        val  = val.replace(old_char, new_char)

    return val
    
    