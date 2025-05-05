import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import os
from datetime import datetime, timedelta
from pony.orm import Database, Required, PrimaryKey, db_session, select, desc
import requests
import json

# Configure the database
db = Database()

class ConversionHistory(db.Entity):
    id = PrimaryKey(int, auto=True)
    from_currency = Required(str)
    to_currency = Required(str)
    amount = Required(float)
    result = Required(float)
    timestamp = Required(datetime, default=datetime.now)
    
class ExchangeRate(db.Entity):
    currency_code = PrimaryKey(str)
    rate = Required(float)
    last_updated = Required(datetime, default=datetime.now)

# API configuration
API_BASE_URL= ""
# Get API Key at https://www.exchangerate-api.com/

CURRENCY_MAP = {
    "US Dollar (USD)": "USD",
    "Kuwaiti Dinar (KWD)": "KWD",
    "Thai Baht (THB)": "THB",
    "Japanese Yen (¥)": "JPY",
    "Euro (€)": "EUR",
    "British Pound (£)": "GBP",
    "Australian Dollar (A$)": "AUD",
    "Singapore Dollar (S$)": "SGD",
    "Malaysian Ringgit (RM)": "MYR",
    "Chinese Yuan (¥)": "CNY",
}

# Reverse mapping for display purposes
REVERSE_CURRENCY_MAP = {code: name for name, code in CURRENCY_MAP.items()}

class CurrencyConverterApp(toga.App):
    def startup(self):
        # Setup database
        self.setup_database()
            
        self.update_exchange_rates_from_api()
            
        self.main_window = toga.MainWindow(
            title=self.formal_name,
            size=(400, 550)
        )
        self.main_window.content = self.build_main()
        self.main_window.show()

    def setup_database(self):
        """Set up the database connection in the project folder"""
        try:
            project_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(project_dir, 'data')
            
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                print(f"Created data directory: {data_dir}")
            
            db_path = os.path.join(data_dir, 'currency_converter.sqlite')
            print(f"Database will be stored at: {db_path}")
            
            # Bind database
            db.bind(provider='sqlite', filename=db_path, create_db=True)
            db.generate_mapping(create_tables=True)
            
            # Test connection
            with db_session:
                count = select(h for h in ConversionHistory).count()
                print(f"Database initialized with {count} records")
                
            return True
            
        except Exception as e:
            print(f"Database setup failed: {str(e)}")
            return False

    
    def update_exchange_rates_from_api(self):
        """Update exchange rates from API."""
        try:
            # Fetch new rates from API
            response = requests.get(API_BASE_URL)
            response.raise_for_status()
            data = response.json()
            
            if data.get('result') == 'success':
                rates = data['conversion_rates']
                
                with db_session:
                    # Update all supported currencies
                    for display_name, code in CURRENCY_MAP.items():
                        if code in rates and code != 'IDR':
                            rate = rates[code]
                            
                            # Update or create the rate
                            rate_obj = ExchangeRate.get(currency_code=code)
                            if rate_obj:
                                rate_obj.rate = rate
                                rate_obj.last_updated = datetime.now()
                            else:
                                ExchangeRate(currency_code=code, rate=rate)
                    
                    print("Exchange rates updated successfully from API")
                    return True
            else:
                print(f"API error: {data.get('error-type', 'Unknown error')}")
                
        except Exception as e:
            print(f"Failed to update exchange rates from API: {str(e)}")
        
        return False
    
    def get_exchange_rate(self, currency_code):
        """Get exchange rate from database."""
        with db_session:
            rate_obj = ExchangeRate.get(currency_code=currency_code)
            if rate_obj:
                return rate_obj.rate
            return None

    def build_main(self):
        """Main screen with improved UI and navigation buttons."""
        main_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=30,
                alignment=CENTER
            )
        )

        # App title
        title_label = toga.Label(
            "Konversi Mata Uang",
            style=Pack(
                font_size=24,
                padding_bottom=30,
                text_align=CENTER
            )
        )

        # Button container
        btn_container = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=10,
                width=250
            )
        )

        btn_to_foreign = toga.Button(
            "Rupiah → Mata Uang Asing",
            on_press=self.show_to_foreign,
            style=Pack(
                padding=15,
                background_color="#3498db",
                color="white",
                padding_bottom=15
            )
        )

        btn_to_idr = toga.Button(
            "Mata Uang Asing → Rupiah",
            on_press=self.show_to_idr,
            style=Pack(
                padding=15,
                background_color="#2ecc71",
                color="white",
                padding_bottom=15
            )
        )

        btn_history = toga.Button(
            "Riwayat Konversi",
            on_press=self.show_history,
            style=Pack(
                padding=15,
                background_color="#9b59b6",
                color="white"
            )
        )

        # Footer
        footer_label = toga.Label(
            "Kurs diperbarui dari API",
            style=Pack(
                font_size=10,
                padding_top=30,
                text_align=CENTER
            )
        )

        btn_container.add(btn_to_foreign)
        btn_container.add(btn_to_idr)
        btn_container.add(btn_history)
        
        main_box.add(title_label)
        main_box.add(btn_container)
        main_box.add(footer_label)
        
        return main_box

    def show_to_foreign(self, widget):
        self.main_window.content = self.build_to_foreign()

    def show_to_idr(self, widget):
        self.main_window.content = self.build_to_idr()
        
    def show_history(self, widget):
        self.main_window.content = self.build_history()

    def show_main(self, widget):
        self.main_window.content = self.build_main()

    def build_to_foreign(self):
        """Improved layout for converting Rupiah to foreign currencies."""
        container = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=30
            )
        )

        # Header
        header_label = toga.Label(
            "Konversi Rupiah ke Mata Uang Asing",
            style=Pack(
                font_size=18,
                padding_bottom=20,
                text_align=CENTER
            )
        )

        # Input box
        input_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding_bottom=15
            )
        )

        self.input_idr = toga.TextInput(
            placeholder="Masukkan jumlah IDR",
            style=Pack(
                flex=1,
                padding=12,
                font_size=14
            )
        )

        # Currency selection
        currency_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding_bottom=15
            )
        )

        self.currency_select = toga.Selection(
            items=list(CURRENCY_MAP.keys()),
            style=Pack(
                flex=1,
                padding=12,
                font_size=14
            )
        )

        # Result display
        self.result_label = toga.Label(
            "",
            style=Pack(
                padding=20,
                font_size=16,
                text_align=CENTER,
                background_color="#ecf0f1"
            )
        )

        # Buttons
        btn_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding_top=15
            )
        )

        btn_convert = toga.Button(
            "Konversi",
            on_press=self.on_convert_to_foreign,
            style=Pack(
                flex=1,
                padding=12,
                background_color="#3498db",
                color="white",
                padding_right=10
            )
        )

        btn_back = toga.Button(
            "Kembali",
            on_press=self.show_main,
            style=Pack(
                flex=1,
                padding=12,
                background_color="#e74c3c",
                color="white"
            )
        )

        input_box.add(self.input_idr)
        currency_box.add(self.currency_select)
        btn_box.add(btn_convert)
        btn_box.add(btn_back)

        container.add(header_label)
        container.add(toga.Label("Jumlah Rupiah:", style=Pack(padding_bottom=5)))
        container.add(input_box)
        container.add(toga.Label("Pilih Mata Uang:", style=Pack(padding_bottom=5)))
        container.add(currency_box)
        container.add(btn_box)
        container.add(self.result_label)

        return container

    def build_to_idr(self):
        """Improved layout for converting foreign currencies to Rupiah."""
        container = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=30
            )
        )

        # Header
        header_label = toga.Label(
            "Konversi Mata Uang Asing ke Rupiah",
            style=Pack(
                font_size=18,
                padding_bottom=20,
                text_align=CENTER
            )
        )

        # Currency selection
        currency_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding_bottom=15
            )
        )

        self.currency_select2 = toga.Selection(
            items=list(CURRENCY_MAP.keys()),
            style=Pack(
                flex=1,
                padding=12,
                font_size=14
            )
        )

        # Input box
        input_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding_bottom=15
            )
        )

        self.input_foreign = toga.TextInput(
            placeholder="Masukkan jumlah mata uang",
            style=Pack(
                flex=1,
                padding=12,
                font_size=14
            )
        )

        # Result display
        self.result_label2 = toga.Label(
            "",
            style=Pack(
                padding=20,
                font_size=16,
                text_align=CENTER,
                background_color="#ecf0f1"
            )
        )

        # Buttons
        btn_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding_top=15
            )
        )

        btn_convert = toga.Button(
            "Konversi",
            on_press=self.on_convert_to_idr,
            style=Pack(
                flex=1,
                padding=12,
                background_color="#3498db",
                color="white",
                padding_right=10
            )
        )

        btn_back = toga.Button(
            "Kembali",
            on_press=self.show_main,
            style=Pack(
                flex=1,
                padding=12,
                background_color="#e74c3c",
                color="white"
            )
        )

        currency_box.add(self.currency_select2)
        input_box.add(self.input_foreign)
        btn_box.add(btn_convert)
        btn_box.add(btn_back)

        container.add(header_label)
        container.add(toga.Label("Pilih Mata Uang:", style=Pack(padding_bottom=5)))
        container.add(currency_box)
        container.add(toga.Label("Jumlah Mata Uang:", style=Pack(padding_bottom=5)))
        container.add(input_box)
        container.add(btn_box)
        container.add(self.result_label2)

        return container
        
    def build_history(self):
        """Build the conversion history screen."""
        container = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=30
            )
        )

        # Header
        header_label = toga.Label(
            "Riwayat Konversi",
            style=Pack(
                font_size=18,
                padding_bottom=20,
                text_align=CENTER
            )
        )

        # History list
        self.history_table = toga.Table(
            headings=['Dari', 'Ke', 'Jumlah', 'Hasil', 'Waktu'],
            style=Pack(
                flex=1,
                padding_bottom=15
            )
        )
        
        # Button to return to main menu
        btn_back = toga.Button(
            "Kembali",
            on_press=self.show_main,
            style=Pack(
                padding=12,
                background_color="#e74c3c",
                color="white"
            )
        )
        
        # Load history data
        self.load_history_data()
        
        container.add(header_label)
        container.add(self.history_table)
        container.add(btn_back)
        
        return container
        
    def load_history_data(self):
        """Load conversion history data from database into table."""
        with db_session:
            # Get the last 20 conversion records ordered by timestamp
            history_data = list(select(h for h in ConversionHistory).order_by(desc(ConversionHistory.timestamp))[:20])
            
            # Format the data for display in the table
            table_data = []
            for record in history_data:
                from_currency = "IDR" if record.from_currency == "IDR" else record.from_currency
                to_currency = "IDR" if record.to_currency == "IDR" else record.to_currency
                
                # Format amount and result
                if from_currency == "IDR":
                    amount_str = f"{record.amount:,.0f} IDR"
                else:
                    amount_str = f"{record.amount:.2f} {from_currency}"
                    
                if to_currency == "IDR":
                    result_str = f"{record.result:,.0f} IDR"
                else:
                    result_str = f"{record.result:.2f} {to_currency}"
                
                # Format timestamp
                time_str = record.timestamp.strftime("%d/%m/%Y %H:%M")
                
                table_data.append(
                    [from_currency, to_currency, amount_str, result_str, time_str]
                )
            
            # Update table data
            self.history_table.data = table_data

    def on_convert_to_foreign(self, widget):
        """Handler for converting Rupiah to foreign currencies."""
        try:
            amount = float(self.input_idr.value.replace(",", "").replace(".", ""))
            if amount <= 0:
                raise ValueError
        except Exception:
            self.result_label.text = "Masukkan jumlah Rupiah yang valid!"
            return
        
        self._convert_to_foreign(amount)

    def _convert_to_foreign(self, amount):
        selection = self.currency_select.value
        code = CURRENCY_MAP[selection]
        rate = self.get_exchange_rate(code) 
        
        if rate is None:
            self.result_label.text = f"Tidak tersedia kurs untuk {selection}!\nSilakan periksa koneksi internet Anda."
            return
        
        # Convert IDR to foreign: amount (IDR) * rate (foreign/IDR) = foreign amount
        converted = amount * rate
        currency_symbol = selection.split("(")[-1].replace(")", "")
        
        # Calculate the inverse rate for display (how much IDR per 1 foreign)
        inverse_rate = 1 / rate if rate != 0 else 0
        
        self.result_label.text = (
            f"{amount:,.0f} IDR = {converted:,.2f} {currency_symbol}\n"
            f"Kurs: 1 {code} = {inverse_rate:,.0f} IDR"
        )
        
        # Save the conversion to history
        with db_session:
            ConversionHistory(
                from_currency="IDR",
                to_currency=code,
                amount=amount,
                result=converted
            )


    def on_convert_to_idr(self, widget):
        try:
            amount = float(self.input_foreign.value.replace(",", "").replace(".", ""))
            if amount <= 0:
                raise ValueError
        except Exception:
            self.result_label2.text = "Masukkan jumlah mata uang yang valid!"
            return
        
        self._convert_to_idr(amount)

    def _convert_to_idr(self, amount):
        selection = self.currency_select2.value
        code = CURRENCY_MAP[selection]
        rate = self.get_exchange_rate(code)  
        
        if rate is None:
            self.result_label2.text = f"Tidak tersedia kurs untuk {selection}!\nSilakan periksa koneksi internet Anda."
            return
        
        # Convert foreign to IDR: amount (foreign) / rate (foreign/IDR) = IDR amount
        converted = amount / rate
        currency_symbol = selection.split("(")[-1].replace(")", "")
        
        # Calculate the inverse rate for display (how much IDR per 1 foreign)
        inverse_rate = 1 / rate if rate != 0 else 0
        
        self.result_label2.text = (
            f"{amount:,.2f} {currency_symbol} = {converted:,.0f} IDR\n"
            f"Kurs: 1 {code} = {inverse_rate:,.0f} IDR"
        )
        
        # Save to history
        with db_session:
            ConversionHistory(
                from_currency=code,
                to_currency="IDR",
                amount=amount,
                result=converted
            )

def main():
    return CurrencyConverterApp(
        formal_name="Konverter Mata Uang",
        app_id="com.example.currencyconverter"
    )

if __name__ == "__main__":
    app = main()
    app.main_loop()