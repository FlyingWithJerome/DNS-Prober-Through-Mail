'''
mail_generator.py

use to generate a full email object
'''

import random
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText


_HEADER_FORMAT = "From: %s\r\nTo: %s\r\n\r\n"
_SUBJECT = "A email for DNS resolvers' TCP-fallback (please ignore)"
_MAIN_BODY = ("This is a research project on investigating "
"DNS resolvers' TCP-fallback capability. The project is conducted by "
"Jerome Mao and Prof. Michael Rabinovich from Case Western Reserve University "
"(jxm959@case.edu)")

_ENCODED_DOMAIN_NAME = "{cpyname}-{gltd}-research.yumi.ipl.eecs.case.edu"

def _encode_domain(domain_name: str) -> str:
    domain_name_parsed = domain_name.split(".")
    company_name = domain_name_parsed[-2]
    gltd_suffix = domain_name_parsed[-1]
    return _ENCODED_DOMAIN_NAME.format(
        cpyname=company_name,
        gltd=gltd_suffix
    )

def _generate_random_string(num_char: int) -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(num_char))

def _generate_mail_content(sender: str, receiver: str) -> str:
    '''
    generate a full, string format mail (with from, to, subject) 
    '''
    mail = MIMEMultipart()
    mail["From"] = sender
    mail["To"] = receiver
    mail["Subject"] = _SUBJECT
    mail.attach(MIMEText(_MAIN_BODY))

    return mail.as_string()

def generate_mail_from_domain(domain_name: str) -> (str, str, str):
    '''
    wrapper for the mail send process
    '''
    sender_addr = "research@" + _encode_domain(domain_name)
    receiver_addr = _generate_random_string(10)+ "@" + domain_name

    return sender_addr, receiver_addr, _generate_mail_content(sender_addr, receiver_addr)
