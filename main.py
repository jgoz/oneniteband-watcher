import email
import imaplib
import re
import settings

def get_inbox():
    # TODO: Error handling
    imap_server = imaplib.IMAP4_SSL(settings.IMAP_SERVER_URL, settings.IMAP_SERVER_PORT)
    imap_server.login(settings.IMAP_USERNAME, settings.IMAP_PASSWORD)
    imap_server.select('INBOX')
    return imap_server

def find_unread(inbox):
    # TODO: Error handling
    _, email_ids = inbox.search(None, '(UNSEEN)')
    return email_ids

def extract_plain_text(response_data):
    mail = email.message_from_string(response_data)

    text = []
    for part in mail.walk():
        if part.get_content_subtype() == 'plain':
            text.append(part.get_payload())
    return text

def fetch_messages(inbox, email_ids):
    data = []
    for eid in email_ids:
        if not eid:
            continue
        # TODO: Error handling
        _, response = inbox.fetch(eid, '(RFC822)')
        data.extend(extract_plain_text(response[0][1]))
    return data

def parse_gigs(messages):
    # TODO: parse gigs using regex
    gigs = []
    for message in messages:
        gigs.extend(message.split('\n'))
    return gigs

def publish_gigs(gigs):
    # TODO: publish to couchdb or something
    for gig in gigs:
        print gig

def main():
    inbox = get_inbox()
    email_ids = find_unread(inbox)
    messages = fetch_messages(inbox, email_ids)
    gigs = parse_gigs(messages)
    publish_gigs(gigs)

if __name__ == '__main__':
    main()
