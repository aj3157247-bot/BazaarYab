import os

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.metrics import dp, sp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle

try:
    import arabic_reshaper
    from bidi.algorithm import get_display

    def rtl(text):
        if not text:
            return ""
        return get_display(arabic_reshaper.reshape(str(text)))
except Exception:
    def rtl(text):
        return str(text)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "assets", "Vazirmatn-Regular.ttf")

if os.path.exists(FONT_PATH):
    LabelBase.register(name="PersianFont", fn_regular=FONT_PATH)
else:
    FONT_PATH = None


class PLabel(Label):
    def __init__(self, **kwargs):
        self._raw_text = kwargs.pop("raw_text", kwargs.get("text", ""))
        self.auto_height = kwargs.pop("auto_height", False)
        kwargs["font_name"] = "PersianFont" if FONT_PATH else kwargs.get("font_name", "Roboto")
        kwargs.setdefault("halign", "right")
        kwargs.setdefault("valign", "middle")
        kwargs["text"] = rtl(self._raw_text)
        super().__init__(**kwargs)
        self.bind(size=self._update_text_size)
        if self.auto_height:
            self.bind(texture_size=self._update_auto_height)

    def _update_auto_height(self, *args):
        self.height = self.texture_size[1]

    def _update_text_size(self, *args):
        self.text_size = (max(0, self.width), None)

    def set_text(self, value):
        self._raw_text = "" if value is None else str(value)
        self.text = rtl(self._raw_text)


class PButton(Button):
    def __init__(self, **kwargs):
        raw = kwargs.pop("raw_text", kwargs.get("text", ""))
        kwargs["font_name"] = "PersianFont" if FONT_PATH else kwargs.get("font_name", "Roboto")
        kwargs.setdefault("font_size", sp(16))
        kwargs.setdefault("halign", "center")
        kwargs.setdefault("valign", "middle")
        kwargs["text"] = rtl(raw)
        super().__init__(**kwargs)
        self.bind(size=self._update_text)

    def _update_text(self, *args):
        self.text_size = self.size

    def set_text(self, value):
        self.text = rtl(value)


class BazaarYarApp(App):
    def build(self):
        self.title = "BazaarYar"
        self.menu_open = False
        root = FloatLayout()

        main = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        # Header: menu is on the right for Persian RTL layout.
        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60)
        )
        title = PLabel(raw_text="بازاریار", font_size=sp(27), bold=True, halign="center")
        menu = Button(
            text="☰",
            font_name="PersianFont" if FONT_PATH else "Roboto",
            font_size=sp(25),
            size_hint_x=None,
            width=dp(60)
        )
        menu.bind(on_release=self.toggle_menu)
        header.add_widget(title)
        header.add_widget(menu)
        main.add_widget(header)

        subtitle = PLabel(
            raw_text="دستیار هوشمند بازار",
            font_size=sp(17),
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        main.add_widget(subtitle)

        search_title = PLabel(
            raw_text="چه چیزی می‌خواهید پیدا کنید؟",
            font_size=sp(18),
            size_hint_y=None,
            height=dp(45)
        )
        main.add_widget(search_title)

        # Search button is visually on the right.
        search_row = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(55)
        )
        search_button = PButton(raw_text="جستجو", size_hint_x=None, width=dp(100))
        search_button.bind(on_release=self.search)
        self.search_input = TextInput(
            font_name="PersianFont" if FONT_PATH else "Roboto",
            font_size=sp(16),
            multiline=False,
            halign="right",
            padding=(dp(10), dp(10)),
            hint_text=rtl("جستجو..."),
            cursor_width=dp(2)
        )
        search_row.add_widget(self.search_input)
        search_row.add_widget(search_button)
        main.add_widget(search_row)

        self.result = PLabel(
            raw_text="برای شروع، چیزی را جستجو کنید.",
            font_size=sp(17),
            valign="top",
            size_hint_y=None,
            auto_height=True
        )
        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(self.result)
        main.add_widget(scroll)

        # Bottom navigation: right-to-left visual order: خانه، بازار، حساب.
        bottom = BoxLayout(spacing=dp(6), size_hint_y=None, height=dp(58))
        account = PButton(raw_text="حساب")
        market = PButton(raw_text="بازار")
        home = PButton(raw_text="خانه")
        bottom.add_widget(account)
        bottom.add_widget(market)
        bottom.add_widget(home)
        main.add_widget(bottom)
        root.add_widget(main)

        self.create_menu(root)
        self.root_layout = root
        root.bind(size=lambda *_: self.update_side_position())
        self.update_side_position()
        return root

    def create_menu(self, root):
        # The Persian side menu opens from the right, not the left.
        self.side = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8),
            size_hint=(None, 1),
            width=dp(280),
            pos=(root.width, 0)
        )
        with self.side.canvas.before:
            Color(0.10, 0.10, 0.14, 1)
            self.bg = RoundedRectangle(
                pos=self.side.pos,
                size=self.side.size,
                radius=[dp(12)]
            )
        self.side.bind(pos=self.update_bg, size=self.update_bg)

        title = PLabel(
            raw_text="بازاریار",
            font_size=sp(25),
            bold=True,
            halign="center",
            size_hint_y=None,
            height=dp(65)
        )
        self.side.add_widget(title)

        items = [
            "خانه",
            "بازار",
            "جستجوی محصولات",
            "علاقه‌مندی‌ها",
            "حساب کاربری",
            "تنظیمات",
            "درباره بازاریار"
        ]
        for item in items:
            button = PButton(raw_text=item, size_hint_y=None, height=dp(52))
            button._logical_text = item
            button.bind(on_release=self.menu_click)
            self.side.add_widget(button)

        close = PButton(raw_text="بستن", size_hint_y=None, height=dp(52))
        close.bind(on_release=self.close_menu)
        self.side.add_widget(close)
        root.add_widget(self.side)

    def update_side_position(self, *args):
        if not hasattr(self, "side") or not hasattr(self, "root_layout"):
            return
        self.side.x = self.root_layout.width - self.side.width if self.menu_open else self.root_layout.width

    def toggle_menu(self, *args):
        if self.menu_open:
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        self.menu_open = True
        self.update_side_position()

    def close_menu(self, *args):
        self.menu_open = False
        self.update_side_position()

    def menu_click(self, instance):
        # Button text is visually reshaped, so use a clean mapping instead.
        self.result.set_text(getattr(instance, "_logical_text", "انتخاب شد"))
        self.close_menu()

    def update_bg(self, instance, *args):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def search(self, *args):
        text = self.search_input.text.strip()
        if not text:
            self.result.set_text("لطفاً عبارت موردنظر را وارد کنید.")
        else:
            self.result.set_text("نتیجه جستجو\n\n" + text)


if __name__ == "__main__":
    BazaarYarApp().run()
