import os

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView


# ============================================================
# تنظیم فونت فارسی
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "assets", "Vazirmatn-Regular.ttf")

if os.path.exists(FONT_PATH):
    LabelBase.register(
        name="PersianFont",
        fn_regular=FONT_PATH
    )
    DEFAULT_FONT = "PersianFont"
else:
    DEFAULT_FONT = "Roboto"


# ============================================================
# ویجت متن راست‌چین فارسی
# ============================================================

class PersianLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault("font_name", DEFAULT_FONT)
        kwargs.setdefault("halign", "right")
        kwargs.setdefault("valign", "middle")
        super().__init__(**kwargs)

        self.bind(
            size=self._update_text_size
        )

    def _update_text_size(self, *args):
        self.text_size = (self.width, None)


# ============================================================
# برنامه اصلی
# ============================================================

class BazaarYarApp(App):

    def build(self):

        self.title = "بازاریار"

        # جلوگیری از تغییر اندازه عجیب پنجره در دسکتاپ
        Window.minimum_width = dp(320)
        Window.minimum_height = dp(600)

        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        # ----------------------------------------------------
        # سربرگ
        # ----------------------------------------------------

        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(100),
            spacing=dp(3)
        )

        title = Label(
            text="بازاریار",
            font_name=DEFAULT_FONT,
            font_size=sp(28),
            bold=True,
            halign="center",
            valign="middle"
        )

        title.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        subtitle = Label(
            text="دستیار هوشمند بازار",
            font_name=DEFAULT_FONT,
            font_size=sp(15),
            halign="center",
            valign="middle"
        )

        subtitle.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        header.add_widget(title)
        header.add_widget(subtitle)

        root.add_widget(header)

        # ----------------------------------------------------
        # جستجو
        # ----------------------------------------------------

        search_title = PersianLabel(
            text="چه چیزی می‌خواهید پیدا کنید؟",
            font_size=sp(17),
            size_hint_y=None,
            height=dp(40)
        )

        root.add_widget(search_title)

        search_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(52),
            spacing=dp(8)
        )

        self.search_input = TextInput(
            hint_text="مثلاً موبایل، لباس، لپ‌تاپ...",
            font_name=DEFAULT_FONT,
            font_size=sp(16),
            multiline=False,
            halign="right",
            padding=[dp(12), dp(10)],
            write_tab=False
        )

        search_button = Button(
            text="جستجو",
            font_name=DEFAULT_FONT,
            font_size=sp(16),
            size_hint_x=None,
            width=dp(95)
        )

        search_button.bind(
            on_release=self.search
        )

        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_button)

        root.add_widget(search_layout)

        # ----------------------------------------------------
        # ناحیه نتایج
        # ----------------------------------------------------

        self.result_label = PersianLabel(
            text="برای شروع، عبارت موردنظر خود را جستجو کنید.",
            font_size=sp(16),
            halign="right",
            valign="top",
            size_hint_y=None
        )

        self.result_label.bind(
            texture_size=lambda instance, value:
            setattr(instance, "height", max(value[1], dp(100)))
        )

        scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(4)
        )

        scroll.add_widget(self.result_label)

        root.add_widget(scroll)

        # ----------------------------------------------------
        # منوی پایین
        # ----------------------------------------------------

        bottom = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(58),
            spacing=dp(6)
        )

        home_button = Button(
            text="خانه",
            font_name=DEFAULT_FONT,
            font_size=sp(15)
        )

        market_button = Button(
            text="بازار",
            font_name=DEFAULT_FONT,
            font_size=sp(15)
        )

        profile_button = Button(
            text="حساب",
            font_name=DEFAULT_FONT,
            font_size=sp(15)
        )

        home_button.bind(
            on_release=lambda x: self.show_message(
                "صفحه اصلی بازاریار"
            )
        )

        market_button.bind(
            on_release=lambda x: self.show_message(
                "بخش بازار"
            )
        )

        profile_button.bind(
            on_release=lambda x: self.show_message(
                "حساب کاربری"
            )
        )

        bottom.add_widget(home_button)
        bottom.add_widget(market_button)
        bottom.add_widget(profile_button)

        root.add_widget(bottom)

        return root

    # ========================================================
    # جستجو
    # ========================================================

    def search(self, *args):

        query = self.search_input.text.strip()

        if not query:
            self.result_label.text = (
                "لطفاً چیزی برای جستجو وارد کنید."
            )
            return

        self.result_label.text = (
            "نتیجه جستجو\n\n"
            f"عبارت جستجو شده: {query}\n\n"
            "بازاریار در حال آماده‌سازی نتایج است..."
        )

    # ========================================================
    # نمایش پیام
    # ========================================================

    def show_message(self, message):

        self.result_label.text = message


# ============================================================
# اجرای برنامه
# ============================================================

if __name__ == "__main__":
    BazaarYarApp().run()
