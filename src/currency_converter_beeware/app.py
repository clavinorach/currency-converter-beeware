import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER

EXCHANGE_RATES = {
    "USD": 0.000066,  # US Dollar
    "KWD": 0.000020,  # Kuwaiti Dinar
    "THB": 0.0022,    # Thai Baht
    "JPY": 0.0090,    # Japanese Yen
    "EUR": 0.000060,  # Euro
    "GBP": 0.000052,  # British Pound
    "AUD": 0.000096,  # Australian Dollar
    "SGD": 0.000088,  # Singapore Dollar
    "MYR": 0.00030,   # Malaysian Ringgit
    "CNY": 0.00046,   # Chinese Yuan
}

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

class CurrencyConverterApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(
            title=self.formal_name,
            size=(400, 500)
        )
        self.main_window.content = self.build_main()
        self.main_window.show()

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
                color="white"
            )
        )

        # Footer
        footer_label = toga.Label(
            "Kurs tetap, tidak diperbarui otomatis",
            style=Pack(
                font_size=10,
                padding_top=30,
                text_align=CENTER
            )
        )

        btn_container.add(btn_to_foreign)
        btn_container.add(btn_to_idr)
        
        main_box.add(title_label)
        main_box.add(btn_container)
        main_box.add(footer_label)
        
        return main_box

    def show_to_foreign(self, widget):
        self.main_window.content = self.build_to_foreign()

    def show_to_idr(self, widget):
        self.main_window.content = self.build_to_idr()

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
        rate = EXCHANGE_RATES.get(code)
        
        if rate is None:
            self.result_label.text = f"Tidak tersedia kurs untuk {selection}!"
            return
        
        converted = amount * rate
        currency_symbol = selection.split("(")[-1].replace(")", "")
        
        self.result_label.text = (
            f"{amount:,.0f} IDR = {converted:,.2f} {currency_symbol}\n"
            f"Kurs: 1 IDR = {rate:.6f} {code}"
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
        rate = EXCHANGE_RATES.get(code)
        
        if rate is None:
            self.result_label2.text = f"Tidak tersedia kurs untuk {selection}!"
            return
        
        converted = amount / rate
        currency_symbol = selection.split("(")[-1].replace(")", "")
        
        self.result_label2.text = (
            f"{amount:,.2f} {currency_symbol} = {converted:,.0f} IDR\n"
            f"Kurs: 1 {code} = {1/rate:,.0f} IDR"
        )


def main():
    return CurrencyConverterApp(
        formal_name="Konverter Mata Uang",
        app_id="com.example.currencyconverter"
    )

if __name__ == "__main__":
    app = main()
    app.main_loop()