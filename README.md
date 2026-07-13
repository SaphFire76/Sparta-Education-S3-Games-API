# Project Setup Guide

Follow these instructions to set up your local development environment, install the required dependencies, and configure your API keys.

## Prerequisites
Make sure you have [Python](https://www.python.org/downloads/) installed on your machine. 

---

## 1. Create a Virtual Environment
It is best practice to run this project inside a virtual environment to keep dependencies isolated. 

Open your terminal, navigate to the project's root directory, and run:
```bash
python -m venv .venv
```
*(Note: If you are on macOS/Linux, you might need to use `python3` instead of `python`).*

## 2. Activate the Virtual Environment
You must activate the environment every time you work on this project. 

**For Windows:**
```bash
.venv\Scripts\activate
```

**For macOS and Linux:**
```bash
source .venv/bin/activate
```
*You will know it is activated when you see `(.venv)` appear at the beginning of your terminal prompt.*

## 3. Install Dependencies
With your virtual environment active, install all the required libraries from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## 4. Set Up Environment Variables
This project requires environment variables to safely store sensitive information like API keys. 

1. In the root directory of this project, create a new file and name it exactly **`.env`**
2. Open the `.env` file and add your API key. Do not use quotes around the key:
```text
API_KEY=your_actual_api_key_here
```

**Security Note:** The `.env` and `.venv` files are already included in the `.gitignore` file. Never commit your `.env` file to version control!

---
**You are now ready to run the project!**