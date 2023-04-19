import imaplib
import email
import re
import time
from email.header import decode_header
import tkinter as tk
import pygame

pygame.init()
pygame.mixer.init()
EMAIL = "YOUR_MAIL_HERE"
PASSWORD = "YOUR_PASSWORD_HERE"
SERVER = "imap-mail.outlook.com" # For hotmail, you can replace it if needed
REFRESH = 60000 # refresh mail checking time in milliseconds

def get_message_content(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()

def update_listbox(listbox, mail):
    mail.select("inbox")

    # Rechercher tous les e-mails non lus
    status, messages = mail.search(None, 'UNSEEN')
    messages = messages[0].split(b' ')

    # Limiter la recherche aux 100 derniers messages reçus
    messages = messages[-100:]

    for msg_num in messages[::-1]:
        if not msg_num:
            continue

        msg_num_str = msg_num.decode('utf-8')

        status, message_data = mail.fetch(msg_num, '(BODY.PEEK[])')
        if message_data[0] is None or message_data[0][1] is None:
            continue

        msg = email.message_from_bytes(message_data[0][1])

        if msg["Subject"] is not None:
            decoded_subject = decode_header(msg["Subject"])[0]
            try:
                subject = decoded_subject[0].decode() if isinstance(decoded_subject[0], bytes) else decoded_subject[0]
            except UnicodeDecodeError:
                subject = decoded_subject[0].decode('iso-8859-1')
        else:
            subject = ""

        if subject == "You have a new booking":
            message_content = get_message_content(msg)

            pattern = r"from\s+([a-zA-Z]+\s+\d{1,2},\s+\d{4})\s+(\d{1,2}:\d{2})"
            match = re.search(pattern, message_content)

            if match:
                datetime_str = match.group(1) + "|" + match.group(2)
                date_str, time_str = datetime_str.split("|", 1)
                listbox.insert(tk.END, f"{date_str} - {time_str}")
                mail.store(msg_num, '+FLAGS', '\\Seen')
                sound = pygame.mixer.Sound("new.wav")
                sound.play()
                window.lift()
                window.attributes('-topmost', True)
                window.after_idle(window.attributes, '-topmost', False)

        elif subject == "Evaluation imminent":
            sound2 = pygame.mixer.Sound("imminent.wav")
            sound2.play()
            window.lift()
            window.attributes('-topmost', True)
            window.after_idle(window.attributes, '-topmost', False)
            mail.store(msg_num, '+FLAGS', '\\Seen')

    listbox.after(REFRESH, update_listbox, listbox, mail)

def delete_selected_item(listbox):
    selected_index = listbox.curselection()
    if selected_index:
        listbox.delete(selected_index)

def main():
    global window
    window = tk.Tk()
    window.title("Evaluation Information")

    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(window, width=40, yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)

    update_listbox(listbox, mail)

    delete_button = tk.Button(window, text="Supprimer", command=lambda: delete_selected_item(listbox))
    delete_button.pack(side=tk.BOTTOM)

    window.mainloop()

if __name__ == "__main__":
    main()
