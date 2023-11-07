<p align="center">
 <h1 align="center">Telegram Bot: Tracking Expenses</h1>
</p>

## Introduction
This is a Telegram bot using for *tracking expenses* and *recording data to Google Sheets*. 
Developed in Python language and using:
* Python-Telegram-Bot library
* Gspread library
  
## Get started

### 1. Requirements
Install requiremental package:
* `pip install python-telegram-bot`
* `pip install gspread`

### 2. Get Telegram Bot Token and Google API
**Telegram Bot Token:**

* <p>Opening Telegram app &#8594; Access Bot Father &#8594; Create new bot &#8594; Get Bot Token.</p>
* <p>You can also customize your bot with the command provided by Bot Father.</p>

**Google API:**
* <p>Visit <a href="https://console.cloud.google.com/">Google Cloud</a> and create new Project.</p>
* <p>Enable Google Sheets API and Google Drive API</p>
* <p>Create <b>Credentials</b>: Choose <b>Service Accounts</b> authorization and <b>ADD KEY</b> &#8594 The brower will automatically download the JSON file</p>
<p>There are <i>2 ways</i> to store the JSON file correctlly:</p>

* Store in the following path: `C:\Users\ADMIN\AppData\Roaming\gspread\service_account.json`
* Store in your project folder, following structure:
```
├── src
│   ├── main.py
│   │   ├── .config
│   │   │   ├── gspread
│   │   │   │   ├── service_account.json
```
Then, when you use `service_account()` method in your code, keep in mind to pass that path, e.g: `file = gspread.service_account("./.config/gspread/service_account.json")`




## Deploy

*updating*

## Test

*updating*
