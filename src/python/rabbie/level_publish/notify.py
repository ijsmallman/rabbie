import smtplib
from email.mime.text import MIMEText
from typing import List
import logging


logger = logging.getLogger(__name__)


class Email:

    def __init__(self, smtp_server: str,
                 smtp_port: int,
                 username: str,
                 password: str,
                 recipients: List[str]) -> None:
        self.server = smtplib.SMTP(smtp_server, smtp_port)
        self.server.ehlo()
        self.server.starttls()

        self.username = username
        self.password = password
        self.recipients = recipients

    def notify(self, subject: str, body: str) -> None:
        """
        Send a notification email to recipients

        Parameters
        ----------
        subject: str
            email subject
        body: str
            email body
        """
        logger.debug('Sending email to {} with subject: {}, body: {}'.format(self.recipients, subject, body))
        self.server.login(self.username, self.password)
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = ','.join(self.recipients)
        self.server.send_message(msg, self.username, self.recipients)

