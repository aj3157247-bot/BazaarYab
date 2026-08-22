import os

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView


# ============================================================
# PATH
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FONT_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "Vazirmatn-Regular.ttf"
)


# ============================================================
# FONT
# ============================================================

if not os.path.isfile(FONT_PATH):
    raise FileNotFoundError(
        "Vazirmatn-Regular.ttf پیدا نشد:\n"
        + FONT_PATH
    )

LabelBase.register(
    name="PersianFont",
    fn_regular=FONT_PATH
)


# ============================================================
# PERSIAN SHAPING
# بدون کتابخانه اضافی
# ============================================================

JOINING = {
    "ا": ("ﺍ", "ﺎ"),
    "آ": ("ﺁ", "ﺂ"),
    "ب": ("ﺏ", "ﺐ", "ﺑ", "ﺒ"),
    "پ": ("ﭖ", "ﭗ", "ﭙ", "ﭘ"),
    "ت": ("ﺕ", "ﺖ", "ﺗ", "ﺘ"),
    "ث": ("ﺙ", "ﺚ", "ﺛ", "ﺜ"),
    "ج": ("ﺝ", "ﺞ", "ﺟ", "ﺠ"),
    "چ": ("ﭺ", "ﭻ", "ﭼ", "ﭽ"),
    "ح": ("ﺡ", "ﺢ", "ﺣ", "ﺤ"),
    "خ": ("ﺥ", "ﺦ", "ﺧ", "ﺨ"),
    "د": ("ﺩ", "ﺪ"),
    "ذ": ("ﺫ", "ﺬ"),
    "ر": ("ﺭ", "ﺮ"),
    "ز": ("ﺯ", "ﺰ"),
    "ژ": ("ﮊ", "ﮋ"),
    "س": ("ﺱ", "ﺲ", "ﺳ", "ﺴ"),
    "ش": ("ﺵ", "ﺶ", "ﺷ", "ﺸ"),
    "ص": ("ﺹ", "ﺺ", "ﺻ", "ﺼ"),
    "ض": ("ﺽ", "ﺾ", "ﺿ", "ﻀ"),
    "ط": ("ﻁ", "ﻂ", "ﻃ", "ﻄ"),
    "ظ": ("ﻅ", "ﻆ", "ﻇ", "ﻈ"),
    "ع": ("ﻉ", "ﻊ", "ﻋ", "ﻌ"),
    "غ": ("ﻍ", "ﻎ", "ﻏ", "ﻐ"),
    "ف": ("ﻑ", "ﻒ", "ﻓ", "ﻔ"),
    "ق": ("ﻕ", "ﻖ", "ﻗ", "ﻘ"),
    "ک": ("ﮎ", "ﮏ", "ﮐ", "ﮑ"),
    "گ": ("ﮒ", "ﮓ", "ﮔ", "ﮕ"),
    "ل": ("ﻝ", "ﻞ", "ﻟ", "ﻠ"),
    "م": ("ﻡ", "ﻢ", "ﻣ", "ﻤ"),
    "ن": ("ﻥ", "ﻦ", "ﻧ", "ﻨ"),
    "و": ("ﻭ", "ﻮ"),
    "ه": ("ﻩ", "ﻪ", "ﻫ", "ﻬ"),
    "ی": ("ﻯ", "ﻰ", "ﻳ", "ﻴ"),
    "ي": ("ﻯ", "ﻰ", "ﻳ", "ﻴ"),
}

NON_JOINING = set([
    "ا", "آ", "د", "ذ", "ر", "ز", "ژ", "و"
])


def is_persian_char(ch):
    return ch in JOINING


def can_join_left(ch):
    return is_persian_char(ch) and ch not in NON_JOINING


def can_join_right(ch):
    return is_persian_char(ch)


def shape_word(word):
    result = []

    chars = list(word)

    for i, ch in enumerate(chars):

        if ch not in JOINING:
            result.append(ch)
            continue

        previous = chars[i - 1] if i > 0 else ""
        next_char = chars[i + 1] if i + 1 < len(chars) else ""

        join_previous = (
            can_join_left(previous)
            and can_join_right(ch)
        )

        join_next = (
            can_join_left(ch)
            and can_join_right(next_char)
        )

        forms = JOINING[ch]

        if len(forms) == 2:

            if join_previous:
                result.append(forms[1])
            else:
                result.append(forms[0])

        else:

            if join_previous and join_next:
                result.append(forms[3])

            elif join_previous:
                result.append(forms[1])

            elif join_next:
                result.append(forms[2])

            else:
                result.append(forms[0])

    return "".join(result)


def rtl(text):
    """
    تبدیل متن فارسی به شکل قابل نمایش
    در Kivy بدون dependency اضافی.
    """

    if not text:
        return ""

    words = text.split(" ")

    shaped_words = []

    for word in words:
        shaped_words.append(
            shape_word(word)
        )

    # ترتیب راست به چپ برای نمایش Kivy
    return " ".join(
        reversed(shaped_words)
    )


# ============================================================
# PERSIAN LABEL
# ============================================================

class PersianLabel(Label):

    def __init__(self, **kwargs):

        original = kwargs.get("text", "")

        kwargs["text"] = rtl(original)

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
            size=self._update_text_size
        )

    def _update_text_size(self, *args):

        self.text_size = (
            self.width,
            None
        )

    def set_text(self, text):

        self.text = rtl(text)


# ============================================================
# PERSIAN BUTTON
# ============================================================

class PersianButton(Button):

    def __init__(self, **kwargs):

        original = kwargs.get("text", "")

        kwargs["text"] = rtl(original)

        kwargs["font_name"] = "PersianFont"

        kwargs.setdefault(
            "font_size",
            sp(16)
        )

        super().__init__(**kwargs)

        self.bind(
            size=self._update_text_size
        )

    def _update_text_size(self, *args):

        self.text_size = self.size

    def set_text(self, text):

        self.text = rtl(text)


# ============================================================
# APP
# ============================================================

class BazaarYarApp(App):

    def build(self):

        self.title = "BazaarYar"

        self.menu_open = False

        # ====================================================
        # ROOT
        # ====================================================

        self.root_layout = FloatLayout()

        # ====================================================
        # MAIN PAGE
        # ====================================================

        main = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10),
            size_hint=(1, 1)
        )

        # ====================================================
        # TOP BAR
        # ====================================================

        top = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            spacing=dp(8)
        )

        menu_button = Button(
            text="☰",
            font_name="PersianFont",
            font_size=sp(25),
            size_hint_x=None,
            width=dp(58)
        )

        menu_button.bind(
            on_release=self.toggle_menu
        )

        title = PersianLabel(
            text="بازاریار",
            font_size=sp(28),
            bold=True,
            halign="center"
        )

        top.add_widget(menu_button)
        top.add_widget(title)

        main.add_widget(top)

        # ====================================================
        # SUBTITLE
        # ====================================================

        subtitle = PersianLabel(
            text="دستیار هوشمند بازار",
            font_size=sp(17),
            halign="center",
            size_hint_y=None,
            height=dp(42)
        )

        main.add_widget(subtitle)

        # ====================================================
        # SEARCH TITLE
        # ====================================================

        search_title = PersianLabel(
            text="چه چیزی می‌خواهید پیدا کنید؟",
            font_size=sp(18),
            bold=True,
            size_hint_y=None,
            height=dp(45)
        )

        main.add_widget(search_title)

        # ====================================================
        # SEARCH
        # ====================================================

        search_box = BoxLayout(
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
            padding=[
                dp(12),
                dp(12)
            ],
            hint_text=rtl(
                "مثلاً موبایل، لباس، لپ‌تاپ..."
            )
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
        # RESULTS
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
        # BOTTOM MENU
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
        # SIDE MENU
        # ====================================================

        self.create_side_menu()

        return self.root_layout

    # ========================================================
    # SIDE MENU
    # ========================================================

    def create_side_menu(self):

        self.side_menu = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(12),
            size_hint=(None, 1),
            width=dp(280),
            pos_hint={
                "x": -1,
                "y": 0
            }
        )

        with self.side_menu.canvas.before:

            Color(
                0.10,
                0.10,
                0.14,
                1
            )

            self.side_background = RoundedRectangle(
                pos=self.side_menu.pos,
                size=self.side_menu.size,
                radius=[dp(12)]
            )

        self.side_menu.bind(
            pos=self.update_side_background,
            size=self.update_side_background
        )

        # ====================================================
        # MENU TITLE
        # ====================================================

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

        # ====================================================
        # MENU ITEMS
        # ====================================================

        buttons = [

            (
                "خانه",
                "صفحه اصلی بازاریار"
            ),

            (
                "بازار",
                "بخش بازار"
            ),

            (
                "جستجوی محصولات",
                "جستجوی محصولات"
            ),

            (
                "علاقه‌مندی‌ها",
                "علاقه‌مندی‌ها"
            ),

            (
                "حساب کاربری",
                "حساب کاربری"
            ),

            (
                "تنظیمات",
                "تنظیمات"
            ),

            (
                "درباره بازاریار",
                "بازاریار\n\n"
                "دستیار هوشمند بازار"
            )
        ]

        for title, message in buttons:

            button = PersianButton(
                text=title,
                size_hint_y=None,
                height=dp(52)
            )

            button.bind(
                on_release=lambda instance,
                msg=message:
                self.show_message_and_close(msg)
            )

            self.side_menu.add_widget(
                button
            )

        # ====================================================
        # CLOSE BUTTON
        # ====================================================

        close_button = PersianButton(
            text="بستن",
            size_hint_y=None,
            height=dp(52)
        )

        close_button.bind(
            on_release=self.close_menu
        )

        self.side_menu.add_widget(
            close_button
        )

        self.root_layout.add_widget(
            self.side_menu
        )

    # ========================================================
    # MENU CONTROL
    # ========================================================

    def toggle_menu(self, *args):

        if self.menu_open:

            self.close_menu()

        else:

            self.open_menu()

    def open_menu(self):

        self.menu_open = True

        self.side_menu.pos_hint = {
            "x": 0,
            "y": 0
        }

    def close_menu(self, *args):

        self.menu_open = False

        self.side_menu.pos_hint = {
            "x": -1,
            "y": 0
        }

    # ========================================================
    # MENU BACKGROUND
    # ========================================================

    def update_side_background(
        self,
        instance,
        *args
    ):

        self.side_background.pos = instance.pos

        self.side_background.size = instance.size

    # ========================================================
    # SEARCH
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
            "عبارت جستجو شده: "
            + query
            + "\n\n"
            "بازاریار در حال آماده‌سازی "
            "نتایج است..."
        )

    # ========================================================
    # MESSAGE
    # ========================================================

    def show_message_and_close(
        self,
        message
    ):

        self.show_message(message)

        self.close_menu()

    def show_message(self, message):

        self.result_label.set_text(
            message
        )

    # ========================================================
    # RESULT HEIGHT
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


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    BazaarYarApp().run()
