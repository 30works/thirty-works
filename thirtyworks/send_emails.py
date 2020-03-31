import pandas as pd
import os
from django.core.mail import EmailMessage, send_mail
from django.utils.html import strip_tags


RECIPIENT_LIST_PATH = os.path.join(os.path.expanduser('~'), 'recipient_list.xlsx')
EMAIL_HTML_PATH = os.path.join(os.path.expanduser('~'), 'day1-email.html')

# # read list of recipients
# df = pd.read_excel(RECIPIENT_LIST_PATH)
# recipients = []
# for i, row in df.iterrows():
#     email_address = row['email']
#     recipients.append(email_address)

# # hardcode recipients for debugging
recipients = ['loumacnamara@gmail.com', 'xavierdcruz0@gmail.com', '9dimensionaltensor@gmail.com']

# read HTML email content
with open(EMAIL_HTML_PATH, 'r') as f:
    html_email_content = f.read()

# print(type(html_email_content))

# create a plain version for crippled email viewers
plain_message = strip_tags(html_email_content)

# print(plain_message)

# iterate over recipients
for recipient in recipients:
    
    # email = EmailMessage(
    #     subject='Hello',
    #     body='Body goes here',
    #     from_email='info@thirty.works',
    #     to=['to1@example.com', 'to2@example.com'],
    #     reply_to=['another@example.com'],
    #     headers={'Message-ID': 'foo'},
    # )

    recipient_html_email_content = "{}".format(html_email_content)
    recipient_html_email_content = recipient.format(recipient, '!!!SOME---PASSWORD!!!')

    recipient_plain_email_content = strip_tags(recipient_html_email_content)
    print('============    Plain message text (for crippled email viewers:   ==============\n)')
    print(recipient_plain_email_content)

    send_mail(
        subject='30/30 info',
        message=plain_message,
        html_message=html_email_content,
        from_email='info@thirty.works',
        recipient_list=[recipient]
    )

    print('Sent email to {}'.format(recipient))
