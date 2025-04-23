import asyncio
import httpx
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

API_URL = "https://api.exchangerate-api.com/v4/latest/IDR"

# Display names mapped to API currency codes
CURRENCY_MAP = {
    "USD": "USD",
    "Kuwait": "KWD",
    "Baht": "THB",
    "Yen": "JPY",
    "Euro": "EUR",
}

class CurrencyConverterApp(toga.App):

    async def fetch_rates(self):
        """Fetch real-time rates (IDR base)."""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(API_URL)
                resp.raise_for_status()
                return resp.json()["rates"]
        except Exception as e:
            self.main_window.error_dialog("Network Error", str(e))
            return None

    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.build_main()
        self.main_window.show()

    def build_main(self):
        """Screen utama dengan dua tombol navigasi."""
        box = toga.Box(style=Pack(direction=COLUMN, padding=20))

        btn_to_foreign = toga.Button(
            "Rupiah → Mata Uang Asing",
            on_press=self.show_to_foreign,
            style=Pack(flex=1, padding=10)
        )
        btn_to_idr = toga.Button(
            "Mata Uang Asing → Rupiah",
            on_press=self.show_to_idr,
            style=Pack(flex=1, padding=10)
        )

        box.add(btn_to_foreign)
        box.add(btn_to_idr)
        return box

    def show_to_foreign(self, widget):
        self.main_window.content = self.build_to_foreign()

    def show_to_idr(self, widget):
        self.main_window.content = self.build_to_idr()

    def show_main(self, widget):
        self.main_window.content = self.build_main()

    def build_to_foreign(self):
        """Layout konversi Rupiah ke asing."""
        self.input_idr = toga.TextInput(
            placeholder="Jumlah IDR",
            style=Pack(flex=1, padding_right=10)
        )
        self.currency_select = toga.Selection(
            items=list(CURRENCY_MAP.keys()),
            on_select=lambda w: None,
            style=Pack(width=100)
        )
        self.result_label = toga.Label("", style=Pack(padding_top=10))

        btn_convert = toga.Button(
            "Convert",
            on_press=self.on_convert_to_foreign,
            style=Pack(padding_top=10)
        )
        btn_back = toga.Button(
            "← Kembali",
            on_press=self.show_main,
            style=Pack(padding_top=10)
        )

        box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        row = toga.Box(style=Pack(direction=ROW))
        row.add(self.input_idr)
        row.add(self.currency_select)
        box.add(row)
        box.add(btn_convert)
        box.add(self.result_label)
        box.add(btn_back)
        return box

    def build_to_idr(self):
        """Layout konversi asing ke Rupiah."""
        self.currency_select2 = toga.Selection(
            items=list(CURRENCY_MAP.keys()),
            on_select=lambda w: None,
            style=Pack(width=100, padding_right=10)
        )
        self.input_foreign = toga.TextInput(
            placeholder="Jumlah Mata Uang",
            style=Pack(flex=1)
        )
        self.result_label2 = toga.Label("", style=Pack(padding_top=10))

        btn_convert = toga.Button(
            "Convert",
            on_press=self.on_convert_to_idr,
            style=Pack(padding_top=10)
        )
        btn_back = toga.Button(
            "← Kembali",
            on_press=self.show_main,
            style=Pack(padding_top=10)
        )

        box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        row = toga.Box(style=Pack(direction=ROW))
        row.add(self.currency_select2)
        row.add(self.input_foreign)
        box.add(row)
        box.add(btn_convert)
        box.add(self.result_label2)
        box.add(btn_back)
        return box

    def on_convert_to_foreign(self, widget):
        """Handler untuk konversi Rupiah → Asing."""
        try:
            amount = float(self.input_idr.value.replace(",", ""))
        except Exception:
            return self.main_window.info_dialog(
                "Input Error", "Masukkan angka Rupiah yang valid."
            )
        asyncio.ensure_future(self._convert_to_foreign_async(amount))

    async def _convert_to_foreign_async(self, amount):
        rates = await self.fetch_rates()
        if not rates:
            return
        selection = self.currency_select.value
        code = CURRENCY_MAP[selection]
        rate = rates.get(code)
        if rate is None:
            return self.main_window.info_dialog(
                "Error", f"Tidak tersedia kurs untuk {selection}."
            )
        converted = amount * rate
        self.result_label.text = f"{amount:,.0f} IDR = {converted:,.2f} {selection}"

    def on_convert_to_idr(self, widget):
        """Handler untuk konversi Asing → Rupiah."""
        try:
            amount = float(self.input_foreign.value.replace(",", ""))
        except Exception:
            return self.main_window.info_dialog(
                "Input Error", "Masukkan angka mata uang asing yang valid."
            )
        asyncio.ensure_future(self._convert_to_idr_async(amount))

    async def _convert_to_idr_async(self, amount):
        rates = await self.fetch_rates()
        if not rates:
            return
        selection = self.currency_select2.value
        code = CURRENCY_MAP[selection]
        rate = rates.get(code)
        if rate is None:
            return self.main_window.info_dialog(
                "Error", f"Tidak tersedia kurs untuk {selection}."
            )
        converted = amount / rate
        self.result_label2.text = f"{amount:,.2f} {selection} = {converted:,.0f} IDR"


def main():
    return CurrencyConverterApp()