import smtplib
import imaplib
import email
import tkinter as tk
from email.mime.text import MIMEText
import tkinter.messagebox as messagebox


# Set up the email addresses and login credentials
email_address = 'wnolaby2@gmail.com'
email_password = 'qqjwcjyydgcaisce'
smtp_server = 'smtp.gmail.com'
imap_server = 'imap.gmail.com'

def show_email_body():
    # Get the currently selected email
    selected_email = emails_listbox.curselection()

    # Make sure an email is selected
    if not selected_email:
        messagebox.showwarning('Warning', 'Please select an email')
        return

    # Get the email data
    email_data = emails[selected_email[0]]

    # Get the email body
    email_body = ''
    if email_data.is_multipart():
        for part in email_data.get_payload():
            if part.get_content_type() == 'text/plain':
                email_body = part.get_payload(decode=True).decode()
                break
    else:
        email_body = email_data.get_payload(decode=True).decode()

    # Display the email body in a new window
    body_window = tk.Toplevel(root)
    body_window.title('Email Body')
    body_text = tk.Text(body_window)
    body_text.insert(tk.END, email_body)
    body_text.pack()

# Create a function to send an email
def send_email(subject, recipient, body):
    # Set up SMTP connection
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_email = 'wnolaby2@gmail.com'  # Replace with your actual email address
    password = 'qqjwcjyydgcaisce'  # Replace with your actual email password
    receiver_email = recipient_entry.get()

    # Compose email message
    message = f'Subject: {subject}\n\n{body}'

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient, message)

# Create a function to receive emails
def receive_emails(keyword=None):
    # Log in to the IMAP server and select the inbox
    try:
        with imaplib.IMAP4_SSL(imap_server) as server:
            server.login(email_address, email_password)
            server.select('inbox')

            # Search for messages that match the keyword
            if keyword:
                search_query = f'(UNSEEN KEYWORD "{keyword}")'
            else:
                search_query = 'All'
            status, messages = server.search(None, search_query)

            # Loop through the messages and add them to the list of emails
            global emails
            emails = []
            for num in messages[0].split():
                status, msg = server.fetch(num, '(RFC822)')
                email_data = email.message_from_bytes(msg[0][1])
                emails.append(email_data)

            # Clear the listbox and add each email to it
            emails_listbox.delete(0, tk.END)
            for email_data in emails:
                subject = email_data['Subject']
                sender = email.utils.parseaddr(email_data['From'])[1]
                emails_listbox.insert(tk.END, f'Subject: {subject} | From: {sender}')
    except Exception as e:
        print(e)

# Create a function to send an email when the button is clicked
def send_email_button_clicked():
    subject = subject_entry.get()
    recipient = recipient_entry.get()
    body = body_text.get('1.0', tk.END)
    send_email(subject, recipient, body)
    subject_entry.delete(0, tk.END)
    recipient_entry.delete(0, tk.END)
    body_text.delete('1.0', tk.END)

def search_emails():
    # Get the search keyword
    keyword = keyword_entry.get()

    # Make sure a keyword is entered
    if not keyword:
        messagebox.showwarning('Warning', 'Please enter a keyword')
        return

    # Search for emails containing the keyword
    global searched_emails
    searched_emails = []
    for email_data in emails:
        if keyword.lower() in str(email_data).lower():
            searched_emails.append(email_data)

    # Clear the listbox and add each email to it
    emails_listbox.delete(0, tk.END)
    for email_data in searched_emails:
        subject = email_data['Subject']
        sender = email.utils.parseaddr(email_data['From'])[1]
        emails_listbox.insert(tk.END, f'Subject: {subject} | From: {sender}')

# Create the widgets



# Create the GUI
root = tk.Tk()
root.title('Email Client')

# Create the widgets
# Create the widgets
subject_label = tk.Label(root, text='Subject')
subject_entry = tk.Entry(root)

recipient_label = tk.Label(root, text='Recipient')
recipient_entry = tk.Entry(root)

body_label = tk.Label(root, text='Body')
body_text = tk.Text(root)

send_button = tk.Button(root, text='Send', command=send_email_button_clicked)

emails_label = tk.Label(root, text='Unread Emails')
emails_listbox = tk.Listbox(root, height=10, width=50)

refresh_button = tk.Button(root, text='Refresh', command=receive_emails)

# Pack the widgets
subject_label.pack()
subject_entry.pack()

recipient_label.pack()
recipient_entry.pack()

body_label.pack()
body_text.pack()

send_button.pack()

emails_label.pack()
emails_listbox.pack()

refresh_button.pack()

read_button = tk.Button(root, text='Read Email', command=show_email_body)
read_button.pack()

keyword_label = tk.Label(root, text='Keyword')
keyword_entry = tk.Entry(root)

search_button = tk.Button(root, text='Search', command=search_emails)

# Pack the widgets
keyword_label.pack()
keyword_entry.pack()

search_button.pack()
# Receive any unread emails on start up
receive_emails()

# Start the main loop
root.mainloop()