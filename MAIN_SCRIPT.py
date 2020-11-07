import os ,sys
from collections import defaultdict
import pandas as pd
import datetime
import mysql.connector
import pyodbc
import os.path
import argparse
import time


def connect(server, email, username, password):
    """
    Get Exchange account cconnection with server
    """

    try:
        creds = Credentials(username=username, password=password)
        config = Configuration(server=server, credentials=creds)
        return Account(primary_smtp_address=email, autodiscover=False, config = config, access_type=DELEGATE)
    except:
        raise Exception("LOGIN FAILED")


def sqlConnect():
    """
    Database connection
    """
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER='';DATABASE='';UID='';PWD='')
    curr =  conn.cursor()
    return curr, conn


def print_tree(account):
    """
    Print folder tree
    """
    print(account.root.tree())






def mail_parsing(account):
    
    """
   mail parser to extract the all details from mail
   
    """
    cursor,cnxn=sqlConnect()
    while True:
        unread = account.inbox.filter(is_read=False)
        if unread==[]:
            print('NO NEW MAIL')
        else:
            for item in unread:
                item.is_read = True
                item.save()
                
                print('SUBJECT:',item.subject,
                      'SENDER:',item.sender,
                      'ATTACHMENTS:',item.attachments,
                      'UNIQUE ID:',item.message_id,
                      'DATE-TIME:',item.datetime_received)
                non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                print('BODY:',item.text_body.translate(non_bmp_map))
              
            
            
                for attachment in item.attachments:
                    if isinstance(attachment, FileAttachment):
                        local_path = os.path.join(r'path', attachment.name)
                        with open(local_path, 'wb') as f:  
                            f.write(attachment.content)
                            print('Saved attachment to', local_path)
                    elif isinstance(attachment, ItemAttachment):
                        if isinstance(attachment.item, Message):
                            print(attachment.item.subject, attachment.item.body)

               

                cursor.execute('INSERT INTO ******', (str(item.sender), str(item.subject), str(item.text_body.translate(non_bmp_map)),item.datetime_received, str(target_file)))
                cnxn.commit()
                # grab all the rows from the table
                cursor.execute('SELECT * TABLE NAME')
                for row in cursor:
                    print(row)
                time.sleep(5)
            

    # close the cursor and connection    
    cnxn.close()
        



def main():

    # Connection details
    server = ''
    email = ''
    username = ''
    password = ''
    
    account = connect(server, email, username, password)

    now = datetime.datetime.now()
    print ("Current date and time : ")
    Current_date_time=print (now.strftime("%Y-%m-%d %H:%M:%S"))

    print_tree(account)
    
    mail_parsing(account)
    

if __name__ == '__main__':
    main()
