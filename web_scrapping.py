
import re
from urllib.request import urlopen, Request
import os
from datetime import datetime
from openpyxl import Workbook
from bs4 import BeautifulSoup
from inscriptis import get_text
import requests
save_excel = False #Change to "True" to save email into Excel

book = Workbook()
sheet = book.active


def start_scrape(page, name_the_file=None):

    print("\n\nWebpage is currently being scrapped... please wait...")

    # scrape = BeautifulSoup(page, 'html.parser')
    # scrape = scrape.extract()

    #print(page)
    text = get_text(page)
    #print(text)
    #phone_numbers = set(re.findall(r"((?:\d{3}|\(\d{3}\))?(?:\s|-|\.)?\d{3}(?:\s|-|\.)\d{4})", scrape))
    phone_numbers = set(re.findall(r"(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{4}", text))#"set" removes duplicates
    emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", text))
    social_profile = set(re.findall('/([\w+]+\:\/\/)?([\w\d-]+\.)*[\w-]+[\.\:]\w+([\/\?\=\&\#\.]?[\w-]+)*\/?/gm', text))
    
    # nodupnumber = len(list(phone_numbers))
    # nodupemail = len(list(emails))

    # dupnumber = len(list(re.findall(r"((?:\d{3}|\(\d{3}\))?(?:\s|-|\.)?\d{3}(?:\s|-|\.)\d{4})", text))) 
    # dupemail = len(list(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", text)))

    # number_of_dup_number = int(dupnumber) - int(nodupnumber) 
    # number_of_dup_email = int(dupemail) - int(nodupemail)

    email_list = list(emails)

    if len(phone_numbers) == 0:
        print("No phone number(s) found.")

        print("-----------------------------\n")
    else:
        count = 1
        for item in phone_numbers:
            print("Phone number #" + str(count) + ': ' + item)
            count += 1

    print("-----------------------------\n")

    if len(emails) == 0:
        print("No email address(es) found.")
        print("-----------------------------\n")
    else:
        count = 1
        for item in emails:
            print('Email address #' + str(count) + ': ' + item)
            count += 1
    print("-----------------------------\n")
           
    if len(social_profile) == 0:
        print("No social_profile(s) found.")
        print("-----------------------------\n")
    else:
        count = 1
        for item in social_profile:
            print('social_profile(s)' + str(count) + ': ' + item)
            count += 1

    if save_excel:
        for row in zip(email_list):
            sheet.append(row)
        excel_file = (name_the_file + ".xlsx")
        book.save(excel_file) 
       
    # print("\nDuplicates have been removed from list.")
    # print("Total phone numbers: ", nodupnumber)
    # print("Total email addresses: ", nodupemail)
    # print("There were " + str(number_of_dup_number) + " duplicate phone numbers.")
    # print("There were " + str(number_of_dup_email) + " duplicate email addresses.")

    if save_excel:
        print("\n\nData has been stored inside of an Excel spreadsheet named: "
              + excel_file + " in this directory: " + os.getcwd())
        mod_time = os.stat(excel_file).st_mtime
        print("\nCompleted at: " + str(datetime.fromtimestamp(mod_time)))
        print("\nSize of file: " + str(os.stat(excel_file).st_size) + " KB")

def main():

    webpage = input("Paste the webpage you would like to scrape (include http/https): ")

    if save_excel:
        name_the_file = input("Name the file you would like to save the data in (don't include .xlsx): ")

    try:
        page = urlopen(webpage) 
        start_scrape(page)
    except:
        hdr = head = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding': 'none',
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Connection': 'keep-alive',
                    'refere': 'https://example.com',
                    'cookie': """your cookie value ( you can get that from your web page) """
                    }
        req = Request(webpage, headers=hdr)
        page = urlopen(req).read().decode('utf-8')
        start_scrape(page)

if __name__ == "__main__":
    main()