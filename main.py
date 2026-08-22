import os

import arabic_reshaper
from bidi.algorithm import get_display

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.metrics import dp, sp
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle


# ============================================================
# مسیر پروژه
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FONT_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "Vazirmatn-Regular.ttf"
)


# ============================================================
# بررسی فونت
# ============================================================

if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(
        "Vazirmatn-Regular.ttf پیدا نشد."
    )

LabelBase.register(
    name="PersianFont",
    fn_regular=FONT_PATH
)


# ============================================================
# تبدیل فارسی به شکل قابل نمایش در Kivy
# ============================================================

def fa(text):
    """
    تبدیل متن فارسی به شکل صحیح برای نمایش در Kivy.
    """

    if not text:
        return ""

    reshaped = arabic_reshaper.reshape(text)

    return get_display(reshaped)


# ============================================================
# Label فارسی
# ============================================================

class PersianLabel(Label):

    def __init__(self, **kwargs):

        if "text" in kwargs:
            kwargs["text"] = fa(kwargs["text"])

        kwargs.setdefault(
            "font_name",
            "PersianFont"
        )

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
            size=self.update_text_size
        )

    def update_text_size(self, *args):

        self.text_size = (
            self.width,
            None
        )

    def set_text(self, text):

        self.text = fa(text)


# ============================================================
# دکمه فارسی
# ============================================================

class PersianButton(Button):

    def __init__(self, **kwargs):

        if "text" in kwargs:
            kwargs["text"] = fa(kwargs["text"])

        kwargs.setdefault(
            "font_name",
            "PersianFont"
        )

        kwargs.setdefault(
            "font_size",
            sp(16)
        )

        super().__init__(**kwargs)

        self.bind(
            size=self.update_text_size
        )

    def update_text_size(self, *args):

        self.text_size = self.size

    def set_text(self, text):

        self.text = fa(text)


# ============================================================
# برنامه BazaarYar
# ============================================================

class BazaarYarApp(App):

    def build(self):

        self.title = "بازاریار"

        # وضعیت منوی کناری
        self.menu_open = False

        # ====================================================
        # لایه اصلی
        # ====================================================

        self.root_layout = FloatLayout()

        # ====================================================
        # صفحه اصلی
        # ====================================================

        main = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10),
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )

        # ====================================================
        # نوار بالایی
        # ====================================================

        top = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(58),
            spacing=dp(8)
        )

        menu_button = PersianButton(
            text="☰",
            size_hint_x=None,
            width=dp(55),
            font_size=sp(24)
        )

        menu_button.bind(
            on_release=self.toggle_menu
        )

        title = PersianLabel(
            text="بازاریار",
            font_size=sp(27),
            bold=True,
            halign="center"
        )

        top.add_widget(menu_button)
        top.add_widget(title)

        main.add_widget(top)

        # ====================================================
        # زیرعنوان
        # ====================================================

        subtitle = PersianLabel(
            text="دستیار هوشمند بازار",
            font_size=sp(17),
            halign="center",
            size_hint_y=None,
            height=dp(45)
        )

        main.add_widget(subtitle)

        # ====================================================
        # عنوان جستجو
        # ====================================================

        search_title = PersianLabel(
            text="چه چیزی می‌خواهید پیدا کنید؟",
            font_size=sp(18),
            bold=True,
            size_hint_y=None,
            height=dp(42)
        )

        main.add_widget(search_title)

        # ====================================================
        # جستجو
        # ====================================================

        search_box = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(55)
        )

        self.search_input = TextInput(
            hint_text=fa(
                "مثلاً موبایل، لباس، لپ‌تاپ..."
            ),
            font_name="PersianFont",
            font_size=sp(16),
            multiline=False,
            halign="right",
            padding=[
                dp(12),
                dp(12)
            ]
        )

        search_button = PersianButton(
            text="جستجو",
            size_hint_x=None,
            width=dp(100)
        )

        search_button.bind(
            on_release=self.search
        )

        search_box.add_widget(
            self.search_input
        )

        search_box.add_widget(
            search_button
        )

        main.add_widget(search_box)

        # ====================================================
        # نتایج
        # ====================================================

        self.result_label = PersianLabel(
            text=(
                "برای شروع، عبارت موردنظر "
                "خود را جستجو کنید."
            ),
            font_size=sp(17),
            valign="top",
            size_hint_y=None
        )

        self.result_label.bind(
            texture_size=self.update_result_height
        )

        scroll = ScrollView(
            do_scroll_x=False
        )

        scroll.add_widget(
            self.result_label
        )

        main.add_widget(scroll)

        # ====================================================
        # منوی پایین
        # ====================================================

        bottom = BoxLayout(
            orientation="horizontal",
            spacing=dp(6),
            size_hint_y=None,
            height=dp(60)
        )

        home = PersianButton(
            text="خانه"
        )

        market = PersianButton(
            text="بازار"
        )

        account = PersianButton(
            text="حساب"
        )

        home.bind(
            on_release=lambda x:
            self.show_message(
                "صفحه اصلی بازاریار"
            )
        )

        market.bind(
            on_release=lambda x:
            self.show_message(
                "بخش بازار"
            )
        )

        account.bind(
            on_release=lambda x:
            self.show_message(
                "حساب کاربری"
            )
        )

        bottom.add_widget(home)
        bottom.add_widget(market)
        bottom.add_widget(account)

        main.add_widget(bottom)

        self.root_layout.add_widget(main)

        # ====================================================
        # منوی کناری
        # ====================================================

        self.create_side_menu()

        return self.root_layout

    # ========================================================
    # ساخت منوی کناری
    # ========================================================

    def create_side_menu(self):

        self.side_menu = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(12),
            size_hint=(None, 1),
            width=dp(270),
            pos_hint={
                "x": -0.01,
                "y": 0
            }
        )

        with self.side_menu.canvas.before:

            Color(
                0.12,
                0.12,
                0.16,
                1
            )

            self.side_background = RoundedRectangle(
                pos=self.side_menu.pos,
                size=self.side_menu.size,
                radius=[dp(10)]
            )

        self.side_menu.bind(
            pos=self.update_side_background,
            size=self.update_side_background
        )

        # ----------------------------------------------------
        # عنوان
        # ----------------------------------------------------

        menu_title = PersianLabel(
            text="بازاریار",
            font_size=sp(25),
            bold=True,
            halign="center",
            size_hint_y=None,
            height=dp(65)
        )

        self.side_menu.add_widget(
            menu_title
        )

        # ----------------------------------------------------
        # گزینه‌ها
        # ----------------------------------------------------

        btn_home = PersianButton(
            text="خانه",
            size_hint_y=None,
            height=dp(52)
        )

        btn_market = PersianButton(
            text="بازار",
            size_hint_y=None,
            height=dp(52)
        )

        btn_search = PersianButton(
            text="جستجوی محصولات",
            size_hint_y=None,
            height=dp(52)
        )

        btn_favorites = PersianButton(
            text="علاقه‌مندی‌ها",
            size_hint_y=None,
            height=dp(52)
        )

        btn_account = PersianButton(
            text="حساب کاربری",
            size_hint_y=None,
            height=dp(52)
        )

        btn_settings = PersianButton(
            text="تنظیمات",
            size_hint_y=None,
            height=dp(52)
        )

        btn_about = PersianButton(
            text="درباره بازاریار",
            size_hint_y=None,
            height=dp(52)
        )

        btn_home.bind(
            on_release=lambda x:
            self.close_menu()
        )

        btn_market.bind(
            on_release=lambda x:
            self.show_message_and_close(
                "بخش بازار"
            )
        )

        btn_search.bind(
            on_release=lambda x:
            self.show_message_and_close(
                "جستجوی محصولات"
            )
        )

        btn_favorites.bind(
            on_release=lambda x:
            self.show_message_and_close(
                "علاقه‌مندی‌ها"
            )
        )

        btn_account.bind(
            on_release=lambda x:
            self.show_message_and_close(
                "حساب کاربری"
            )
        )

        btn_settings.bind(
            on_release=lambda x:
            self.show_message_and_close(
                "تنظیمات"
            )
        )

        btn_about.bind(
            on_release=lambda x:
            self.show_message_and_close(
                "بازاریار\n\n"
                "دستیار هوشمند بازار"
            )
        )

        for button in (
            btn_home,
            btn_market,
            btn_search,
            btn_favorites,
            btn_account,
            btn_settings,
            btn_about
        ):
            self.side_menu.add_widget(button)

        self.root_layout.add_widget(
            self.side_menu
        )

        # ابتدا منو بسته باشد
        self.side_menu.opacity = 0
        self.side_menu.disabled = True

    # ========================================================
    # باز و بسته کردن منو
    # ========================================================

    def toggle_menu(self, *args):

        if self.menu_open:
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):

        self.menu_open = True

        self.side_menu.opacity = 1
        self.side_menu.disabled = False

        self.side_menu.pos_hint = {
            "x": 0,
            "y": 0
        }

    def close_menu(self, *args):

        self.menu_open = False

        self.side_menu.opacity = 0
        self.side_menu.disabled = True

        self.side_menu.pos_hint = {
            "x": -1,
            "y": 0
        }

    # ========================================================
    # پیام + بستن منو
    # ========================================================

    def show_message_and_close(self, message):

        self.show_message(message)
        self.close_menu()

    # ========================================================
    # پس‌زمینه منو
    # ========================================================

    def update_side_background(self, instance, *args):

        self.side_background.pos = instance.pos
        self.side_background.size = instance.size

    # ========================================================
    # ارتفاع نتیجه
    # ========================================================

    def update_result_height(
        self,
        instance,
        texture_size
    ):

        instance.height = max(
            texture_size[1] + dp(25),
            dp(100)
        )

    # ========================================================
    # جستجو
    # ========================================================

    def search(self, *args):

        query = self.search_input.text.strip()

        if not query:

            self.result_label.set_text(
                "لطفاً چیزی برای جستجو وارد کنید."
            )

            return

        self.result_label.set_text(
            "نتیجه جستجو\n\n"
            f"عبارت جستجو شده: {query}\n\n"
            "بازاریار در حال آماده‌سازی "
            "نتایج است..."
        )

    # ========================================================
    # نمایش پیام
    # ========================================================

    def show_message(self, message):

        self.result_label.set_text(
            message
        )


# ============================================================
# اجرا
# ============================================================

if __name__ == "__main__":
    BazaarYarApp().run()
