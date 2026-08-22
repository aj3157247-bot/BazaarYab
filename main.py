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


# ============================================================
# FONT
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FONT_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "Vazirmatn-Regular.ttf"
)

LabelBase.register(
    name="PersianFont",
    fn_regular=FONT_PATH
)


# ============================================================
# PERSIAN LABEL
# ============================================================

class PLabel(Label):

    def __init__(self, **kwargs):

        kwargs["font_name"] = "PersianFont"

        kwargs.setdefault(
            "halign",
            "right"
        )

        kwargs.setdefault(
            "valign",
            "middle"
        )

        super().__init__(**kwargs)

        self.bind(
            size=self.update_text
        )

    def update_text(self, *args):

        self.text_size = (
            self.width,
            None
        )


# ============================================================
# PERSIAN BUTTON
# ============================================================

class PButton(Button):

    def __init__(self, **kwargs):

        kwargs["font_name"] = "PersianFont"

        kwargs.setdefault(
            "font_size",
            sp(16)
        )

        super().__init__(**kwargs)

        self.bind(
            size=self.update_text
        )

    def update_text(self, *args):

        self.text_size = self.size


# ============================================================
# BAZAARYAR
# ============================================================

class BazaarYarApp(App):

    def build(self):

        self.title = "BazaarYar"

        self.menu_open = False

        root = FloatLayout()

        # ====================================================
        # MAIN
        # ====================================================

        main = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        # ====================================================
        # HEADER
        # ====================================================

        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60)
        )

        menu = Button(
            text="☰",
            font_name="PersianFont",
            font_size=sp(25),
            size_hint_x=None,
            width=dp(60)
        )

        menu.bind(
            on_release=self.toggle_menu
        )

        title = PLabel(
            text="بازاریار",
            font_size=sp(27),
            bold=True,
            halign="center"
        )

        header.add_widget(menu)
        header.add_widget(title)

        main.add_widget(header)

        # ====================================================
        # SUBTITLE
        # ====================================================

        subtitle = PLabel(
            text="دستیار هوشمند بازار",
            font_size=sp(17),
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )

        main.add_widget(subtitle)

        # ====================================================
        # SEARCH TITLE
        # ====================================================

        search_title = PLabel(
            text="چه چیزی می‌خواهید پیدا کنید؟",
            font_size=sp(18),
            size_hint_y=None,
            height=dp(45)
        )

        main.add_widget(search_title)

        # ====================================================
        # SEARCH
        # ====================================================

        search_row = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(55)
        )

        self.search_input = TextInput(
            font_name="PersianFont",
            font_size=sp(16),
            multiline=False,
            halign="right",
            padding=dp(10),
            hint_text="جستجو..."
        )

        search_button = PButton(
            text="جستجو",
            size_hint_x=None,
            width=dp(100)
        )

        search_button.bind(
            on_release=self.search
        )

        search_row.add_widget(
            self.search_input
        )

        search_row.add_widget(
            search_button
        )

        main.add_widget(
            search_row
        )

        # ====================================================
        # RESULT
        # ====================================================

        self.result = PLabel(
            text="برای شروع، چیزی را جستجو کنید.",
            font_size=sp(17),
            size_hint_y=None,
            valign="top"
        )

        scroll = ScrollView(
            do_scroll_x=False
        )

        scroll.add_widget(
            self.result
        )

        main.add_widget(
            scroll
        )

        # ====================================================
        # BOTTOM
        # ====================================================

        bottom = BoxLayout(
            spacing=dp(6),
            size_hint_y=None,
            height=dp(58)
        )

        home = PButton(text="خانه")
        market = PButton(text="بازار")
        account = PButton(text="حساب")

        bottom.add_widget(home)
        bottom.add_widget(market)
        bottom.add_widget(account)

        main.add_widget(bottom)

        root.add_widget(main)

        # ====================================================
        # SIDE MENU
        # ====================================================

        self.create_menu(root)

        return root

    # ========================================================
    # SIDE MENU
    # ========================================================

    def create_menu(self, root):

        self.side = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8),
            size_hint=(None, 1),
            width=dp(280),
            pos_hint={
                "x": -1,
                "y": 0
            }
        )

        with self.side.canvas.before:

            Color(
                0.10,
                0.10,
                0.14,
                1
            )

            self.bg = RoundedRectangle(
                pos=self.side.pos,
                size=self.side.size,
                radius=[dp(12)]
            )

        self.side.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        title = PLabel(
            text="بازاریار",
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

            button = PButton(
                text=item,
                size_hint_y=None,
                height=dp(52)
            )

            button.bind(
                on_release=self.menu_click
            )

            self.side.add_widget(button)

        close = PButton(
            text="بستن",
            size_hint_y=None,
            height=dp(52)
        )

        close.bind(
            on_release=self.close_menu
        )

        self.side.add_widget(close)

        root.add_widget(self.side)

    # ========================================================
    # MENU
    # ========================================================

    def toggle_menu(self, *args):

        if self.menu_open:
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):

        self.menu_open = True

        self.side.pos_hint = {
            "x": 0,
            "y": 0
        }

    def close_menu(self, *args):

        self.menu_open = False

        self.side.pos_hint = {
            "x": -1,
            "y": 0
        }

    def menu_click(self, instance):

        self.result.text = instance.text

        self.close_menu()

    # ========================================================
    # BACKGROUND
    # ========================================================

    def update_bg(self, instance, *args):

        self.bg.pos = instance.pos
        self.bg.size = instance.size

    # ========================================================
    # SEARCH
    # ========================================================

    def search(self, *args):

        text = self.search_input.text.strip()

        if not text:

            self.result.text = (
                "لطفاً عبارت موردنظر را وارد کنید."
            )

        else:

            self.result.text = (
                "نتیجه جستجو\n\n"
                + text
            )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    BazaarYarApp().run()
