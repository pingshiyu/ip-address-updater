import smtplib, socket, requests
import logging

'''
    This script will detect the current dynamic IP address and send an update
    email if it finds a change.

    This is to connect my university laptop with my home machine via remote
    desktop connection.
'''

def config_logger():
    logging.basicConfig(
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler("./logs/execution_history.log"),
            logging.StreamHandler()
        ])
    return logging.getLogger()

def get_current_ip():
    '''
        Get current public IPv4 address.
        Output:
            ip : string, current public IPv4 address.
    '''
    ip = None
    try:
        ip = requests.get('https://api.ipify.org').text
        logging.info(f"Current IP address is {ip}")
    except:
        logger.error('Cannot get current IP address.')
    return ip

def get_cached_ip():
    '''
        Get the cached IP from last running. Cached IP stored in
        ./data/ip_cache.txt
        Output:
            ip : string, stored IP address from previous run
    '''
    cached_ip = ''
    with open('./data/ip_cache.txt', 'r') as f:
        cached_ip = f.readline()
        logger.info(f"Cached IP is {cached_ip}")
    return cached_ip

def update_cached_ip(current_ip):
    '''
        Update the cached IP address
    '''
    with open('./data/ip_cache.txt', 'w+') as f:
        f.write(current_ip)
        logger.info(f"Updated cached IP to {current_ip}")

def send_update_email(current_ip):
    # prepare login details & from / to addresses
    username = 'xxxxxx@gmail.com'
    password = '******'
    recipient = 'xxxxxx@gmail.com'
    message = '\n'.join([
                    f'From: {username}',
                    f'To: {recipient}',
                    'Subject: <IP ADDRESS UPDATE>',
                    '',
                    f'Updated IP address is: {current_ip}'
                ])
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.ehlo_or_helo_if_needed()
    smtp.login(username, password)
    smtp.sendmail(username, recipient, message)
    logger.info(f"Email successfully sent!")

if __name__ == '__main__':
    # prepare logger
    logger = config_logger()

    # send email if IP address has changed
    current_ip = get_current_ip()
    cached_ip = get_cached_ip()
    # if the addresses are different then update & send update email
    if current_ip and (current_ip != cached_ip):
        logger.info("IP address has changed, updating & sending update mail...")
        update_cached_ip(current_ip)
        send_update_email(current_ip)
