import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from db import db_connection



def get_data():
    db = db_connection()
    bl_collection = db['backup_logs']
    dl_collection = db['delete_logs']
    backup_logs = bl_collection.find({'date': datetime.now().strftime('%d-%b-%Y')})
    delete_logs = dl_collection.find({'date': datetime.now().strftime('%d-%b-%Y')})
    
    data = {
        'total_backup_files': 0,
        'total_backup_size': 0,
        'total_delete_files': 0,
        'total_delete_size': 0,
    }

    for log in backup_logs:
        data['total_backup_files'] += 1
        data['total_backup_size'] += int(log['size'])

    for log in delete_logs:
        data['total_delete_files'] += 1
        data['total_delete_size'] += int(log['size'])

    return data


def send_email(data):
    # Replace these with your Gmail account details
    sender_email = "dhruv.modi2345@gmail.com"
    sender_password = "ptvd svgy vcen uvif"
    to_email = "dhruv.modi2345@gmail.com"
    subject = "Test Email"
    total_backup_files = data['total_backup_files']
    total_backup_size = data['total_backup_size']
    total_delete_files = data['total_delete_files']
    total_delete_size = data['total_delete_size']
    # convert to gb from bytes
    total_backup_size = f"{round(total_backup_size / 1024 / 1024 / 1024, 2)} GB"
    total_delete_size = f"{round(total_delete_size / 1024 / 1024 / 1024, 2)} GB"
    log_link = "http://216.48.190.109:8080/"
    body = f"""
        <html>
            <body style="margin: 0; padding: 0; height: 80vh; width: 80vw; display: flex; justify-content: center; align-items: center;">
                <div style="background-color: #f2f2f2; padding: 20px; display: flex; justify-content: center; align-items: center;">
                    <div style="background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); width: 500px;">
                        <h1 style="text-align: center; color: #555;">Backup Notification</h1>
                        <p style="text-align: left; color: #555; font-size: 16px;">
                            Total backup files today: {total_backup_files}<br><br>
                            Total backup size today: {total_backup_size}<br><br>
                            Total delete files today: {total_delete_files}<br><br>
                            Total delete size today: {total_delete_size}<br><br>
                            Check the logs here: <a href="{log_link}">{log_link}</a>
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """

    # Gmail SMTP settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    # Create a MIME object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # Attach body to the email
    message.attach(MIMEText(body, "html"))

    # Establish a secure connection with the SMTP server
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        # Login to your Gmail account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, to_email, message.as_string())



async def mail():
    return
    data = get_data()
    print(data)
    send_email(data)
    return True


if __name__ == '__main__':
    import asyncio
    asyncio.run(mail())
