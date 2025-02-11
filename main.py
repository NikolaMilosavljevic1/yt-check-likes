'''

Requests alone doesn't work, because the number of likes is embedded via JavaScript dynamically.
That's why we need to use either YouTube API (which has limited usage) or webdriver

'''

video_link = ""
from_addr = ""
from_pass = ""
to_addr = ""
timeToSend = 0

#----------GUI----------
import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Like info update")
window.geometry("800x300")
window.configure(bg="#2c3e50") #Dark Blue
window.resizable(False, False)

linkLabel = tk.Label(window, text="Enter the link of the video: ", font=("Lucida Sans", 12), fg="white", bg="#2c3e50")
linkEntry = tk.Entry(window, font=("Lucida Sans", 12), width=50)

senderLabel = tk.Label(window, text="Enter the sender address: ", font=("Lucida Sans", 12), fg="white", bg="#2c3e50")
senderEntry = tk.Entry(window, font=("Lucida Sans", 12), width=50)

appPassLabel = tk.Label(window, text="Enter your app password : ", font=("Lucida Sans", 12), fg="white", bg="#2c3e50")
appPassEntry = tk.Entry(window, font=("Lucida Sans", 12), width=50, show='*')

recipientLabel = tk.Label(window, text="Enter the recipient address: ", font=("Lucida Sans", 12), fg="white", bg="#2c3e50")
recipientEntry = tk.Entry(window, font=("Lucida Sans", 12), width=50)

timeToSendLabel = tk.Label(window, text="Enter the time needed to pass to send mail", font=("Lucida Sans", 12), fg="white", bg="#2c3e50")
timeToSendEntry = tk.Entry(window, font=("Lucida Sans", 12), width=50)

linkLabel.grid(row=1, column=0, padx=5, pady=5, sticky='w')
linkEntry.grid(row=1, column=1, padx=2, pady=5)

senderLabel.grid(row=2, column=0, padx=5, pady=5, sticky='w')
senderEntry.grid(row=2, column=1, padx=2, pady=5)

appPassLabel.grid(row=3, column=0, padx=5, pady=5, sticky='w')
appPassEntry.grid(row=3, column=1, padx=2, pady=5)

recipientLabel.grid(row=4, column=0, padx=5, pady=5, sticky='w')
recipientEntry.grid(row=4, column=1, padx=2, pady=5)

timeToSendLabel.grid(row=5, column=0, padx=5, pady=5, sticky='w')
timeToSendEntry.grid(row=5, column=1, padx=2, pady=5)

def popup():

    def on_yes():
        global video_link
        global from_addr
        global from_pass
        global to_addr
        global timeToSend

        video_link = gui_video_link
        from_addr = gui_from_addr
        from_pass = gui_from_pass
        to_addr = gui_to_addr
        timeToSend = ord(gui_timeToSend) - ord('0')
        print(timeToSend + 5)

        popWindow.destroy()
        window.destroy()

    def on_no():
        popWindow.destroy()

    gui_video_link = linkEntry.get()
    gui_from_addr = senderEntry.get()
    gui_from_pass = appPassEntry.get()
    gui_to_addr = recipientEntry.get()
    gui_timeToSend = timeToSendEntry.get()

    if not (gui_video_link and gui_from_addr and gui_from_pass and gui_to_addr):
        messagebox.showerror("Error", "All fields must be filled out!")
        return

    popWindow = tk.Toplevel(window)

    mainx = window.winfo_x()
    mainy = window.winfo_y()
    popWindow.geometry(f"200x100+{mainx+330}+{mainy+200}")
    popWindow.configure(bg="#2c3e50")
    popWindow.resizable(False, False)

    label = tk.Label(popWindow, text="Are you sure?", font=("Lucida Sans", 12), fg="white", bg="#2c3e50")
    label.pack(pady=10)

    button_frame = tk.Frame(popWindow, bg="#2c3e50")
    button_frame.pack()

    yes_button = tk.Button(button_frame, text="Yes", command=on_yes, width=10, bg="green", fg="white", activebackground="green")
    yes_button.grid(row=0, column=0, padx=5, pady=5)

    no_button = tk.Button(button_frame, text="No", command=on_no, width=10, bg="red", fg="white", activebackground="red")
    no_button.grid(row=0, column=1, padx=5, pady=5)


submit = tk.Button(window, text="Submit", command=popup, font=("Lucida Sans", 12))
submit.grid(row=6, column=1)

window.mainloop()


#----------CODE FOR SENDING MAIL----------
import smtplib

server_addr = "smtp.gmail.com"
port = 587

def send_mail(from_addr, from_pass, to_addr, subject, body):
    try:
        with smtplib.SMTP(server_addr, port) as server: #starts connection with smtp.gmail.com on port 587
            server.starttls() #secure protocol, encrypts mail (plain text) with TLS/SSL protocol

            server.login(from_addr, from_pass)
            message = f"Subject:{subject}\n\n{body}"
            # SMTP protocol knows that something that starts with 'Subject: ' is actually subject
            # and everything after new line is body of the mail

            server.sendmail(from_addr, to_addr, message) #sends mail to recipient

        print("E-mail is successfully sent!")

    except Exception as e:
        print(f"Exception{e}")


#----------CODE FOR SCRAPING THE NUMBER OF LIKES----------
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import re
import time

#video_link = "https://youtu.be/ZJZA2B45koM?si=gq7SeOesamoqA9Hi"


#OPTIONS SET-UP:
chrome_options = Options()
chrome_options.add_argument("--headless=new")
#runs home without ui (without user seeing the new tab on google chrome being opened)

chrome_options.add_argument("--disable-gpu")
#prevents GPU rendering issues and crashing (needed for windows)

chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#prevents websites from detecting selenium, prevents flag that websites use to detect bots

def get_likes():
    driver = webdriver.Chrome(options=chrome_options) #initializes the chrome instances and starts service

    driver.get(video_link) #opens the video link on google chrome
    driver.minimize_window()

    try:
        like_cnt_flag = WebDriverWait(driver, 10).until(
            presence_of_element_located((By.CSS_SELECTOR, "button[aria-label*='like'"))
        )
    except TimeoutException as te:
        print(te.msg)
        driver.quit()

    button_like_text = driver.find_element(By.CSS_SELECTOR, "button[aria-label*='like']").get_attribute('aria-label')
    #finds css property aria-label of a button that has the word 'like' in it.
    # Then gets content of that aria-label which will be smt like: 'like this video along with xx.xx other people'
    driver.quit()

    match = re.search(r"(\d+[.,\d]*)", button_like_text) #finds the number of likes that video has
    str_num = match.group(0) #string that is represents the whole match

    arr_str_num = []
    #splitting the string by the comma or dot, its different from time to time
    if str_num.__contains__(','):
        arr_str_num = str_num.split(',')
    else:
        arr_str_num = str_num.split('.')

    #getting the string representation of the number
    string = ""
    for i in arr_str_num:
        string += i

    num = int(string)
    return num


old_likes = get_likes()
while True:
    time.sleep(timeToSend)

    new_likes = get_likes()

    if old_likes < new_likes:
        body = f"You have gained {new_likes - old_likes} like"
        if new_likes - old_likes == 1:
            body += '!'
        else:
            body += 's!'

        send_mail(from_addr, from_pass, to_addr, "Congratulations!", body)
        old_likes = new_likes
    elif old_likes > new_likes:
        body = f"You lost {old_likes - new_likes} like"
        if old_likes - new_likes == 1:
            body += '!'
        else:
            body += 's!'

        send_mail(from_addr, from_pass, to_addr, "Bad news:(", body)
        old_likes = new_likes
