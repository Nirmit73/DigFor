import email
import os
import re
 
def extract_email_info(eml_file):
    with open(eml_file, 'r', encoding='utf-8') as eml:
        msg = email.message_from_file(eml)
        
        sender = msg['From']
        recipient = msg['To']
        subject = msg['Subject']
        
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body += part.get_payload(decode=True).decode()
                except Exception as e:
                    pass
        else:
            body = msg.get_payload(decode=True).decode()
        
        headers = dict(msg.items())
        sender_ip = extract_sender_ip(headers)
        server_info = get_server_information(headers)
        mailer_fingerprint = extract_mailer_fingerprint(headers)
        
        return {
            'Sender': sender,
            'Recipient': recipient,
            'Subject': subject,
            'Body': body,
            'Headers': headers,
            'Sender_IP': sender_ip,
            'Server_Info': server_info,
            'Mailer_Fingerprint': mailer_fingerprint
        }
 
def extract_sender_ip(headers):
    received_headers = headers.get("Received", "")
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    match = re.search(ip_pattern, received_headers)
    if match:
        return match.group()
    return None
 
def get_server_information(headers):
    server_info = {}
    received_headers = headers.get("Received", "").split('\n')
    for header in received_headers:
        server_match = re.search(r'from\s+(\S+)', header)
        if server_match:
            server = server_match.group(1)
            if server not in server_info:
                server_info[server] = 1
            else:
                server_info[server] += 1
    return server_info
 
def extract_mailer_fingerprint(headers):
    user_agent = headers.get("User-Agent", "")
    x_mailer = headers.get("X-Mailer", "")
    return {
        "User-Agent": user_agent,
        "X-Mailer": x_mailer
    }
 
if __name__ == "__main__":
    eml_file_path = 'C:\\Users\\Vipul\\Desktop\\College\\Sem 7\\DF\\DF9\\mail.eml'
    
    if os.path.exists(eml_file_path):
        email_info = extract_email_info(eml_file_path)
        print("Email Information:")
        for key, value in email_info.items():
            print(f'{key}: {value}')
 
        print("\nSender IP:", email_info['Sender_IP'])
        
        print("\nServer Information:")
        for server, count in email_info['Server_Info'].items():
            print(f'{server}: {count} times')
        
        print("\nMailer Fingerprint:")
        for key, value in email_info['Mailer_Fingerprint'].items():
            print(f'{key}: {value}')
    else:
        print(f"File not found: {eml_file_path}")
