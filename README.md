# Like Tracker & Email Notifier

This project is a Python-based application that tracks the number of likes on a YouTube video and sends email notifications when the like count changes. Since YouTube dynamically loads the like count using JavaScript, the program uses Selenium to scrape the data. It features a Tkinter GUI for user input and uses SMTP for sending email notifications.

## GUI

The graphical user interface (GUI) is built using Python's built-in **Tkinter** library. It allows users to input required details such as the YouTube video link, email credentials, and time intervals for monitoring.

## Email Delivery

The script generates and sends emails using Python’s **smtplib** library, which utilizes **SMTP (Simple Mail Transfer Protocol)**.

- The email server used is **smtp.gmail.com** with port **587**.
- To enable email sending, users must generate an **App Password** for their Google account. This ensures secure authentication for SMTP.

## YouTube Scraping

Since YouTube loads the like count dynamically via JavaScript, traditional libraries like **requests** or **Scrapy** do not work. Instead, this project uses **Selenium WebDriver**.

### WebDriver Requirements:
- Install **ChromeDriver** to interact with the Chrome browser.
- Ensure the installed **ChromeDriver version matches** the version of Google Chrome installed on your system.
- Place the `chromedriver.exe` file inside the project directory.
- **Optional:** Use `chrome_options` for headless execution to improve performance and efficiency.

## Setup & Usage

### 1. Clone the repository  

### 2. Run the application  

### 3. Enter details in the GUI:  
- **YouTube video link**  
- **Sender email address**  
- **App password**  
- **Recipient email address**  
- **Time interval** (in seconds) between checks  

### 4. Click **Submit** to start monitoring  

---

## Troubleshooting  

- **Selenium WebDriver Error**: Ensure ChromeDriver is installed and that its version matches the version of Google Chrome.  
- **Login Authentication Error**: Make sure you have enabled Less Secure Apps or used an App Password.  
- **GUI Not Opening**: Check if Tkinter is installed by running:  

  ```bash
  python -m tkinter
