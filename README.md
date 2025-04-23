# Currency Converter

A simple cross‑platform mobile currency converter built with BeeWare/Toga.  
Convert between Indonesian Rupiah (IDR) and major foreign currencies in real time.

![image](https://github.com/user-attachments/assets/ae2be38c-c5d0-4b49-8468-b2790fa19c2f)


## Features

- **Rupiah → Foreign**: Input IDR amount, select currency (USD, Kuwait, Baht, Yen, Euro), tap Convert.  
- **Foreign → Rupiah**: Select foreign currency, input amount, tap Convert.  
- **Real‑time rates** fetched via [exchangerate‑api.com](https://api.exchangerate-api.com/v4/latest/IDR).  
- **Error handling**: Invalid input & network errors show dialogs.

## Tech Stack

- Python 3.8+  
- BeeWare / Toga for UI  
- HTTPX for async HTTP requests  
- Briefcase for packaging to desktop/mobile platforms

## Prerequisites

- Python 3.8 or later  
- Git  
- (Optional) Xcode for iOS builds  
- Java & Android SDK for Android builds

## Project Structure
![image](https://github.com/user-attachments/assets/953db069-c441-4dec-b0d4-c1ccf165fb17)


## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/clavinorach/currency_converter.git
   cd currency_converter

2. Create & activate virtual environment
```bash
python -m venv venv
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate
```

3. Install dependencies
```bash
pip install --upgrade pip setuptools
pip install -r requirements.txt
pip install briefcase
```

4. Verify Briefcase config
```bash
[tool.briefcase.app.currency_converter]
formal_name    = "Currency Converter"
description    = "A mobile currency converter built with BeeWare/Toga."
license.file   = "LICENSE"
bundle         = "com.example.currencyconverter"
version        = "0.1.0"
sources        = ["src/currency_converter"]
requires       = ["toga", "httpx"]
icon           = "assets/app-icon"
```

## Development
Run the app on desktop to test UI & logic:
```bash
briefcase dev
```
- The window should show two buttons for navigation.

- Test “Rupiah → Foreign” and “Foreign → Rupiah” flows.

- Inspect console/logs for errors.

## Packaging & Deployment
Desktop (macOS, Windows, Linux)
```bash
briefcase create
briefcase build
briefcase run
```

Android
```bash
briefcase create android
briefcase build android
briefcase run android
```

iOS
```bash
briefcase create iOS
briefcase build iOS
# Open the generated Xcode project to sign & run on simulator/device
```

WEB
```bash
briefcase create web
briefcase build web
briefcase run web
```

## Configuration
- API URL can be changed in src/currency_converter/app.py:
```bash
API_URL = "https://api.exchangerate-api.com/v4/latest/IDR"
```
- Supported currencies defined in CURRENCY_MAP:
```bash
CURRENCY_MAP = {
    "USD": "USD",
    "Kuwait": "KWD",
    "Baht": "THB",
    "Yen": "JPY",
    "Euro": "EUR",
}
```








