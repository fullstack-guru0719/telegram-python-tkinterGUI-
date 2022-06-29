import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import*
from tkinter import filedialog as fd
import os
import subprocess
import time
import csv
import tkinter as tk
from tkinter import messagebox
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
status = []
class AddContact(threading.Thread):
    def __init__(self, users, profile):
        threading.Thread.__init__(self)
        self.users = users
        self.profile = profile

    def run(self):
        global status
        options = webdriver.ChromeOptions()
        profilepath = "user-data-dir=" + os.getcwd() + "\\profiles\\" + self.profile
        options.add_argument(profilepath)
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.maximize_window()
        telegram_url = 'https://web.telegram.org/k/'
        driver.get(telegram_url)
        time.sleep(10)
        driver.implicitly_wait(20)
        # login_els = driver.find_elements(By.XPATH, '//div[@class="container center-align"]//h4[@class="i18n"]')
            # add users to contact
        session_check = driver.find_elements(By.XPATH, '//div[@class="sidebar-header__btn-container"]')
        if len(session_check) != 0:
            with open("log_session.txt", 'a') as fp:
                fp.write(self.profile + " is inactive now")
                fp.write("\n")
                driver.quit()
                for k in range(0, len(self.users)):
                    status.append([self.users[k][0], self.users[k][1], self.users[k][2], self.users[k][3], "session Error"])
                return status
        for i in range(0, len(self.users)):
            try:
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="sidebar-header__btn-container"]'))).click()
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="btn-menu-item rp-overflow tgico-user rp"]'))).click()
                time.sleep(3)
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-circle btn-corner z-depth-1 is-visible tgico-add rp"]'))).click()
                driver.implicitly_wait(20)
                time.sleep(3)
                first_names = driver.find_elements(By.CLASS_NAME, 'input-field-input')
                first_names[2].send_keys(self.users[i][0])
                first_names[3].send_keys(self.users[i][1])
                first_names[4].clear()
                first_names[4].send_keys(self.users[i][2])
                time.sleep(1)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-primary btn-color-primary rp"]'))).click()
                driver.implicitly_wait(20)
                time.sleep(3)
                contact_list = driver.find_element(By.ID, 'contacts')
                time.sleep(1)
                contact_li_array = contact_list.find_elements(By.TAG_NAME, 'li')
                
                # find user on left side and mark checkbox
                for x in range(0, len(contact_li_array)):
                    split_count = len(contact_li_array[x].text.split('\n'))
                    if split_count > 2:
                        temp_name = contact_li_array[x].text.split('\n')[1]
                    else:
                        temp_name = contact_li_array[x].text.split('\n')[0]
                    if temp_name == self.users[i][0] + " " + self.users[i][1]:
                        time.sleep(1)
                        contact_li_array[x].click()
                        break
                time.sleep(2)
                driver.implicitly_wait(20)

                # send message to added contact
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="input-message-input scrollable scrollable-y i18n no-scrollbar"]'))).send_keys("Hi")
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-icon tgico-none btn-circle z-depth-1 btn-send animated-button-icon rp send"]'))).click()
                time.sleep(3)
                status.append([self.users[i][0], self.users[i][1], self.users[i][2], self.users[i][3], "Success"])
            except:
                status.append([self.users[i][0], self.users[i][1], self.users[i][2], self.users[i][3], "Error"])
                continue
        return status

class BotManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Telegram Bot")
        self.root.geometry("900x550+0+0")
        self.root.config(bg="#2b3e50")

        self.phonenumbers = []
        self.firstnames = []
        self.lastnames = []
        self.messages = []
        self.usernames = []
        # device list
        device_label=Label(self.root,text="Device Name: ",font=("times new roman",12,"bold"),fg="white",bg="black")
        device_label.place(x=20,y=30)
        self.device_namelist = ttk.Combobox(self.root, bootstyle="primary")
        self.device_namelist.place(x= 120, y=30)
        device_name = self.fnRefreshDevices()
        device_refresh = ttk.Button(self.root,text="Refresh", command=self.fnRefreshDevices, bootstyle="success-outline")
        device_refresh.place(x=280, y=30, width=210)
        # add contact and message
        contact_label=Label(self.root,text="Add Contacts and Message ",font=("times new roman",12,"bold"),fg="white",bg="black")
        contact_label.place(x=20,y=90)
        open_re_button = ttk.Button(self.root,text="Open csv file", command=self.fnOpenContactBrowser, bootstyle="success-outline")
        open_re_button.place(x=20, y=120, width=250)

        self.threadnumber = tk.StringVar()
        threadnumber_labels=Label(self.root,text="N of Threads ",font=("times new roman",12,"bold"),fg="white",bg="black")
        threadnumber_labels.place(x=20,y=160)
        thread_number = Entry(self.root, textvariable=self.threadnumber)
        thread_number.place(x=120, y=160, height=30)

        self.add_number_list = Listbox(self.root, selectmode=EXTENDED)
        self.add_number_list.place(x=20, y=200, width=250, height=270)
        self.start_add_contact_button = ttk.Button(self.root,text="Start", command=self.fnStartContact, bootstyle="success-outline")
        self.start_add_contact_button.place(x=20, y=480, width=250, height=40)
        self.add_flag = 0
        # create group and message
        # group name is 
        self.groupname = StringVar()
        self.groupmsg = StringVar()
        group_label=Label(self.root,text="Create Group and send message",font=("times new roman",12,"bold"),fg="white",bg="black")
        group_label.place(x=320,y=90)
        group_namelabel = Label(self.root,text="Name: ",font=("times new roman",12,"bold"),fg="white",bg="black")
        group_namelabel.place(x=320, y=140)
        group_name = Entry(self.root, textvariable=self.groupname)
        group_name.place(x=435, y=140, height=30)
        group_msglabel = Label(self.root,text="Message: ",font=("times new roman",12,"bold"),fg="white",bg="black")
        group_msglabel.place(x=320, y=180)
        group_msg = Entry(self.root, textvariable=self.groupname)
        group_msg.place(x=435, y=180, height=30)
        self.start_add_group_button = ttk.Button(self.root,text="Start", command=self.fnGroupMessage, bootstyle="success-outline")
        self.start_add_group_button.place(x=320, y=270, width=250, height=40)
        # create channel and message
        # channel name is 
        self.channelname = StringVar()
        self.channeldescription = StringVar()
        self.channelmsg = StringVar()
        channel_label=Label(self.root,text="Create Channel and send message",font=("times new roman",12,"bold"),fg="white",bg="black")
        channel_label.place(x=620,y=90)
        channel_namelabel = Label(self.root,text="Name: ",font=("times new roman",12,"bold"),fg="white",bg="black")
        channel_namelabel.place(x=620, y=140)
        channel_name = Entry(self.root, textvariable=self.channelname)
        channel_name.place(x=735, y=140, height=30)
        channel_descriptlabel = Label(self.root,text="Description: ",font=("times new roman",12,"bold"),fg="white",bg="black")
        channel_descriptlabel.place(x=620, y=180)
        channel_descript = Entry(self.root, textvariable=self.channeldescription)
        channel_descript.place(x=735, y=180, height=30)
        channel_messagelabel = Label(self.root,text="Message: ",font=("times new roman",12,"bold"),fg="white",bg="black")
        channel_messagelabel.place(x=620, y=220)
        channel_message = Entry(self.root, textvariable=self.channelmsg)
        channel_message.place(x=735, y=220, height=30)
        self.start_add_channel_button = ttk.Button(self.root,text="Start", command=self.fnChannelMessage, bootstyle="success-outline")
        self.start_add_channel_button.place(x=620, y=270, width=250, height=40)
        # back
        back_button = ttk.Button(self.root,text="Back", command=self.fnBack, bootstyle="danger-outline")
        back_button.place(x=750, y=490, width=100, height=30)
    def fnStartContact(self):
        global status
        profile_list = []
        with open(os.getcwd()+"\\profile.csv", encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",", lineterminator="\n")
            for row in rows:
                profile_list.append(row[0])
        if len(self.phonenumbers) < 5:
            total_thread = 1
        else:
            total_thread = int(len(self.phonenumbers) / 5 + 0.5)
        thread_list = []
        thread_number = int(self.threadnumber.get())
        if total_thread > 1:
            for i in range(0, total_thread):
                temp_receiver = self.phonenumbers[i*5:i*5+5]
                temp_thread = AddContact(temp_receiver,profile_list[i])
                thread_list.append(temp_thread)
                if len(thread_list) == thread_number:
                    for k in range(0 ,len(thread_list)):
                        thread_list[k].start()
                    for k in range(0, len(thread_list)):
                        thread_list[k].join()
                    thread_list = []
        elif total_thread == 1:
            temp_receiver = self.phonenumbers
            temp_thread  = AddContact(temp_receiver,profile_list[0])
            temp_thread.start()
            temp_thread.join()
        textfile = open("add_contact_log.txt", "w")
        for element in status:
            textfile. write(element + "\n")
            textfile. close()
    def fnChannelMessage(self):
        channelname = self.channelname
        channeldescript = self.channeldescription
        channelmsg = self.channelmsg
        rows = [] 
        with open(os.getcwd()+"\\profile.csv", 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows.append(row)
        select_profile = rows[random.randint(1, len(rows))]
        options = webdriver.ChromeOptions()
        profilepath = "user-data-dir=" + os.getcwd() + "\\profiles\\" + select_profile[0]
        options.add_argument(profilepath)
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.maximize_window()
        telegram_url = 'https://web.telegram.org/k/'
        driver.get(telegram_url)
        time.sleep(10)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="new-menu"]'))).click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="btn-menu-item rp-overflow tgico-newchannel rp"]'))).click()
        driver.implicitly_wait(20)
        channel_names = driver.find_elements(By.CLASS_NAME, 'input-field-input')
        channel_names[1].send_keys(channelname)

        channel_descriptions = driver.find_elements(By.CLASS_NAME, 'input-field-input')
        channel_descriptions[2].send_keys(channeldescript)
        time.sleep(3)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-circle btn-corner z-depth-1 tgico-arrow_next rp is-visible"]'))).click()

        time.sleep(3)
        left_side_array = driver.find_element(By.XPATH, '//div[@class="sidebar-left-section no-shadow"]//div[@class="sidebar-left-section-content"]//ul[@class="chatlist"]')
        contact_array = left_side_array.find_elements(By.TAG_NAME, 'li')

        print(self.usernames)
        for x in range(0, len(contact_array)):
            split_count = len(contact_array[x].text.split('\n'))
            if split_count > 2:
                temp_name = contact_array[x].text.split('\n')[1]
                try:
                    self.usernames.index(temp_name)
                    check_el = contact_array[x].find_element(By.CLASS_NAME, 'checkbox-field').click()
                except:
                    pass
            else:
                temp_name = contact_array[x].text.split('\n')[0]
                try:
                    self.usernames.index(temp_name)
                    check_el = contact_array[x].find_element(By.XPATH, '//label[@class="checkbox-field checkbox-without-caption"]').click()
                except:
                    pass
        time.sleep(2)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-circle btn-corner z-depth-1 tgico-arrow_next rp is-visible"]'))).click()

        driver.implicitly_wait(10)
        time.sleep(5)
        el = driver.find_elements(By.XPATH, '//div[@class="new-message-wrapper"]')
        el_msg = el[1].find_element(By.CLASS_NAME, 'input-message-container')
        el_input = el_msg.find_elements(By.XPATH, '//div[@class="input-message-input scrollable scrollable-y i18n no-scrollbar"]')
        time.sleep(3)
        el_input[1].send_keys(channelmsg)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-icon tgico-none btn-circle z-depth-1 btn-send animated-button-icon rp send"]'))).click()
        time.sleep(3)
        return "Success"
        
    def fnGroupMessage(self):
        groupname = self.groupname.get()
        groupmsg = self.groupmsg.get()
        rows = []
        with open(os.getcwd()+"\\profile.csv", 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows.append(row)
        select_profile = rows[random.randint(1, len(rows))]
        options = webdriver.ChromeOptions()
        profilepath = "user-data-dir=" + os.getcwd() + "\\profiles\\" + select_profile[0]
        options.add_argument(profilepath)
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.maximize_window()
        telegram_url = 'https://web.telegram.org/k/'
        driver.get(telegram_url)
        time.sleep(10)
        WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="new-menu"]'))).click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="btn-menu-item rp-overflow tgico-newgroup rp"]'))).click()
        driver.implicitly_wait(20)

        left_side_array = driver.find_element(By.XPATH, '//div[@class="sidebar-left-section no-shadow"]//div[@class="sidebar-left-section-content"]//ul[@class="chatlist"]')
        contact_array = left_side_array.find_elements(By.TAG_NAME, 'li')

        for x in range(0, len(contact_array)):
            split_count = len(contact_array[x].text.split('\n'))
            if split_count > 2:
                temp_name = contact_array[x].text.split('\n')[1]
                try:
                    self.usernames.index(temp_name)
                    contact_array[x].find_element(By.CLASS_NAME, 'checkbox-field').click()
                except:
                    pass
            else:
                temp_name = contact_array[x].text.split('\n')[0]
                try:
                    self.usernames.index(temp_name)
                    contact_array[x].find_element(By.XPATH, '//label[@class="checkbox-field checkbox-without-caption"]').click()
                except:
                    pass
        time.sleep(2)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-circle btn-corner z-depth-1 tgico-arrow_next rp is-visible"]'))).click()

        driver.implicitly_wait(10)
        el_groupname = driver.find_elements(By.CLASS_NAME, 'input-field-input')
        el_groupname[1].send_keys(groupname)

        time.sleep(2)
        driver.implicitly_wait(20)
        el_btn_group = driver.find_elements(By.XPATH, '//button[@class="btn-circle btn-corner z-depth-1 tgico-arrow_next rp is-visible"]')
        el_btn_group[1].click()
        time.sleep(1)
        driver.implicitly_wait(10)

        time.sleep(10)
        el = driver.find_elements(By.XPATH, '//div[@class="new-message-wrapper"]')
        el_msg = el[1].find_element(By.CLASS_NAME, 'input-message-container')
        el_input = el_msg.find_elements(By.XPATH, '//div[@class="input-message-input scrollable scrollable-y i18n no-scrollbar"]')
        time.sleep(3)
        el_input[1].send_keys(groupmsg)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-icon tgico-none btn-circle z-depth-1 btn-send animated-button-icon rp send"]'))).click()
        print(1)
        return "Success"


    def fnOpenContactBrowser(self):
        try:
            rows = []
            filetypes = (
                ('text files', '*.csv'),
            )
            filename = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes, parent=self.root)
            with open(filename, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    if row[0] and row[0].strip():
                        self.add_number_list.insert(int(self.add_number_list.size()), row[0]+row[1]+row[2]+row[3])
                        self.phonenumbers.append(row[0])
                        self.firstnames.append(row[1])
                        self.lastnames.append(row[2])
                        self.messages.append(row[3])
                        self.usernames.append(row[1]+" "+row[2])
        except:
            pass
    def fnRefreshDevices(self):
        with open(os.devnull, 'wb') as devnull:
            subprocess.check_call(['adb', 'start-server'], stdout=devnull,
                                    stderr=devnull)
        out = subprocess.check_output(['adb', 'devices']).splitlines()
        len_list = len(out)
        if len_list < 3:
            return "No device List"
        result = []
        for i in range(1, len(out)-1):
            temp = out[i].decode('utf-8').split("\t")
            result.append(temp[0])
        self.device_namelist['value'] = tuple(result)
        return result
    def fnBack(self):
        self.root.destroy()
