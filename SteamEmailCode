import imaplib
import re

imap_hosts = ['imap-mail.outlook.com', 'imap.gmail.com', 'imap-ssl.mail.yahoo.com']
imap_aux = ['@hotmail.com', '@gmail.com', '@yahoo.com.br']

steam_username = ''
imap_user_email = ''
imap_pass = ''
for g in range(3):
    if len(re.findall(r'%s'%imap_aux[g], imap_user_email)) > 0:
        imap_host = imap_hosts[g]
        break
    else:
        pass

M = imaplib.IMAP4_SSL(imap_host)
M.login(imap_user_email, imap_pass)
M.select()
last_email = M.select()[1][0]
typ, data = M.search(None, 'ALL')
typ, data = M.fetch(last_email, '(RFC822)')

arq = data[0][1].decode()
arq2 = ''
for y in arq:
    if ord(y) < 33 or ord(y) > 125:
        pass
    else:
        arq2 += y

RE_email_code = re.findall(r'%s:(.*?)Thisemail'%steam_username, arq2)

print(RE_email_code[0])

M.close()
M.logout()
