'''
mail_sender.py

implements MailSender, which sends mails to the smtp servers
'''
import concurrent.futures
import csv
import logging
import os
import smtplib
import sys

import mx_query
import mail_generator

_LOGGER = logging.getLogger()
_LOGGER.setLevel(logging.INFO)

def _init_logger(log_path: str) -> None:
    '''
    initialize the global formatter
    '''
    log_format = "[%(asctime)s] %(message)s"
    formatter = logging.Formatter(log_format)
    log_file = logging.FileHandler(log_path)
    _LOGGER.setFormatter(formatter)
    _LOGGER.addHandler(log_file)

class MailSender(object):
    '''
    represents a group of labors that send mail in a parallel manner
    '''

    def __init__(self, num_worker: int):
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_worker)

    @staticmethod
    def mail_send(
            remote_endpoint: str,
            sender: str,
            receiver: str,
            message: str
    ) -> bool:
        '''
        the labor that really sends out the email
        '''
        smtp_success = False
        ssl_smtp_success = False
        print("remote_endpoint", remote_endpoint)
        print("sender", sender)
        print("receiver", receiver)
        
        try:
            with smtplib.SMTP(host=remote_endpoint) as receiving_server:
                receiving_server.sendmail(sender, receiver, message)
                smtp_success = True
        except Exception as e:
            print(e)
            pass
        if smtp_success:
            return True

        # retry with smtp ssl
        try:
            with smtplib.SMTP_SSL(host=remote_endpoint) as receiving_server:
                receiving_server.sendmail(sender, receiver, message)
                ssl_smtp_success = True
        except Exception as e:
            print(e)
            return False
        return smtp_success or ssl_smtp_success

    def do_send(self, target: str):
        '''
        the main loop in sending emails
        '''
        # self._executor.submit(MailSender.mail_send_workflow, target)
        MailSender.mail_send_workflow(target)

    @staticmethod
    def mail_send_workflow(domain_name: str) -> bool:
        '''
        a whole workflow for sending emails
        '''
        smtp_names = mx_query.query_mx_record(domain_name)
        # no smtp server available in this domain ??
        if not smtp_names:
            _LOGGER.critical("No valid MX records for the domain [%s]", domain_name)
            return False

        mail_send_success = False
        while not mail_send_success and smtp_names:
            _, mail_server_address = smtp_names.pop()
            mail_tuple = mail_generator.generate_mail_from_domain(domain_name)
            mail_send_success = MailSender.mail_send(mail_server_address, *mail_tuple)

        if not mail_send_success:
            _LOGGER.critical("Mail delivery failed for all MX records [%s]", domain_name)
        return mail_send_success

    def __del__(self):
        self._executor.shutdown()

def driver(website_list_dir: str, max_threads_num=20) -> None:
    '''
    the driver for the whole mail sender
    '''
    mail_sender = MailSender(max_threads_num)
    with open(website_list_dir, "r") as source_file:
        file_reader = csv.reader(source_file)
        for _, website in file_reader:
            mail_sender.do_send(website)

if __name__ == "__main__":
    # assert len(sys.argv) == 3, "Need a path to the website lists and a path to log"
    # workers = os.cpu_count()
    # full_path = os.path.expanduser(sys.argv[1])
    # path_to_log = os.path.expanduser(sys.argv[2])

    # _init_logger(path_to_log)
    # driver(full_path, max_threads_num=workers)

    mail_sender = MailSender(1)
    mail_sender.do_send("cnn.com")