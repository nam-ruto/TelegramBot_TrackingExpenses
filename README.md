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

<p><i>Refferences: <a href="https://docs.gspread.org/en/latest/api/auth.html#gspread.auth.authorize">Authentication docs - gspread</a></i></p>


## Deploy

<p>This project will be deployed via Github and PythonAnywhere.</p>

<p>Firstly, you have to push the source code to Github as usual. It is recommended that setting your repository privately as this project contains sensitive information like <code>token</code> and <code>JSON file</code>.</p>

### 1. Get PAT
If your repository is in the private mode, you need to get the `Personal Access Token` for the next step.

Why do we need a `PAT`? This is required when you deploy your bot in `PythonAnywhere`, you need to *clone* your Github Repo and a `PAT` is needed for private repo.

Remind to save it securely and you will need it when set up environment when using `PythonAnyWhere`.

### 2. Using PythonAnyWhere
* Create a new account.
* <p>Start a new <code>console</code> &#8594; <code>bash</code></p>
* Clone your project repo: `git clone https://<pat>@github.com/user_name/repo_name.git`
* <p>Set up virtual environment: <code>mkvirtualenv venv</code></p>
* Change direction to your root folder: you can use `pwd` and `ls` command to check the current position.
* <p>Install all required package: <code>pip install -r requirements.text</code></p>
* <p>Run main file: <code>python main.py</code></p>

<p>&#9989; <b>Successfully, your bot is now live on sever!</b></p>


## Result

<p>Here is my released result: <a href="https://t.me/mkkeyBot">@mkkeyBot</a></p>

![mkkeyBot](./assets/result.gif "Tracking Expenses Bot")

Thank you for visiting!

*Author: Hoang Duc Nam*
