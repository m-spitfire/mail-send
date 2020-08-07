#! python3
# mail-send.py - A small automating e mailsending file

import smtplib
from email.message import EmailMessage
import sys
import filetype
import os

EMAIL_NAME = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_DARSH = os.environ.get("EMAIL_DARSH")

# If no argument passed
if len(sys.argv) < 2:
    print("Usage: python mail-send.py [keyphrase] - send e mail according to keyphrase")
    sys.exit()
keyphrase = sys.argv[1]

# Creating a EmailMessage() object
msg = EmailMessage()
msg["From"] = EMAIL_NAME


def send_darshana_files():
    """
    Function for sending e mails 
    to my teacher from a certain directory
    """
    global keyphrase, msg

    files = []
    while True:
        fileInput = input('Enter file name  or "send" for sending e-mail: ')
        if fileInput != "send":
            files.append(fileInput)
        else:
            break

    for file_name in files:
        with open("C:\\Users\\Ilqar\\Desktop\\ielts_essay\\" + file_name, "rb") as f:
            file_data = f.read()

        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=file_name,
        )


def send_custom_files():
    """
    Function for sending custom files
    You must input first directory then file name
    """
    files = []
    file_names = []
    while True:
        file_path = input('Please type directory of file e.g C:\\path\\to\\file (note that you must not put file name in the file path) or "send" for sending: ')

        if file_path != "send":
            file_name = input("Input only file name again:")
            full_path = os.path.join(file_path, file_name)
            files.append(full_path)
            file_names.append(file_name)
        else:
            break

    for path in files:
        with open(path, "rb") as f:
            file_data = f.read()

        kind = filetype.guess(path)

        if kind.extension == "pdf" or kind.extension == "zip":
            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="octet-stream",
                filename=file_name,
            )
        elif kind.extension == "jpg" or kind.extension == "png":
            msg.add_attachment(
                file_data, maintype="image", subtype=kind.extension, filename=file_name
            )
        else:
            print("Only pdf, docx, and image files are supported")


def main():
    if keyphrase == "darshana":
        msg["Subject"] = "IELTS essay roof"
        msg["To"] = EMAIL_DARSH
        msg.set_content("Murad Bashirov Mon/Thu 19:00")
        send_darshana_files()
    elif keyphrase == "custom":
        msg["subject"] = input("Set an e mail subject: ")
        msg["To"] = input("Who to send? ")
        content = input("What is message content? ")
        msg.set_content(content)
        confirmation = input("Want to add attachment(y for confirm, n for deny): ")
        if confirmation == "y":
            send_custom_files()
        elif confirmation == "n":
            pass
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_NAME, EMAIL_PASS)
        smtp.send_message(msg)


if __name__ == "__main__":
    main()
