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
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FONT_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "Vazirmatn-Regular.ttf"
)


# ============================================================
# PERSIAN FONT
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
# PERSIAN LETTER SHAPING
# ============================================================

FORMS = {

    "ا": ("ﺍ", "ﺎ", "ﺍ", "ﺎ"),
    "آ": ("ﺁ", "ﺂ", "ﺁ", "ﺂ"),

    "ب": ("ﺏ", "ﺐ", "ﺑ", "ﺒ"),
    "پ": ("ﭖ", "ﭗ", "ﭙ", "ﭘ"),
    "ت": ("ﺕ", "ﺖ", "ﺗ", "ﺘ"),
    "ث": ("ﺙ", "ﺚ", "ﺛ", "ﺜ"),

    "ج": ("ﺝ", "ﺞ", "ﺟ", "ﺠ"),
    "چ": ("ﭺ", "ﭻ", "ﭼ", "ﭽ"),

    "ح": ("ﺡ", "ﺢ", "ﺣ", "ﺤ"),
    "خ": ("ﺥ", "ﺦ", "ﺧ", "ﺨ"),

    "د": ("ﺩ", "ﺪ", "ﺩ", "ﺪ"),
    "ذ": ("ﺫ", "ﺬ", "ﺫ", "ﺬ"),

    "ر": ("ﺭ", "ﺮ", "ﺭ", "ﺮ"),
    "ز": ("ﺯ", "ﺰ", "ﺯ", "ﺰ"),
    "ژ": ("ﮊ", "ﮋ", "ﮊ", "ﮋ"),

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

    "و": ("ﻭ", "ﻮ", "ﻭ", "ﻮ"),

    "ه": ("ﻩ", "ﻪ", "ﻫ", "ﻬ"),

    "ی": ("ﻯ", "ﻰ", "ﻳ", "ﻴ"),
    "ي": ("ﻯ", "ﻰ", "ﻳ", "ﻴ"),
}


NON_CONNECTING = {
    "ا",
    "آ",
    "د",
    "ذ",
    "ر",
    "ز",
    "ژ",
    "و",
}


def is_persian_letter(char):

    return char in FORMS


def connects_to_previous(char):

    return (
        is_persian_letter(char)
        and char not in NON_CONNECTING
    )


def connects_to_next(char):

    return is_persian_letter(char)


def shape_persian_word(word):

    chars = list(word)

    result = []

    for i, char in enumerate(chars):

        if char not in FORMS:

            result.append(char)
            continue

        previous = ""

        next_char = ""

        if i > 0:
            previous = chars[i - 1]

        if i < len(chars) - 1:
            next_char = chars[i + 1]

        join_previous = (
            connects_to_previous(previous)
            and connects_to_next(char)
        )

        join_next = (
            connects_to_previous(char)
            and connects_to_next(next_char)
        )

        forms = FORMS[char]

        if join_previous and join_next:

            result.append(forms[3])

        elif join_previous:

            result.append(forms[1])

        elif join_next:

            result.append(forms[2])

        else:

            result.append(forms[0])

    return "".join(result)


# ============================================================
# RTL TEXT ENGINE
# ============================================================

def prepare_persian_text(text):

    if not text:
        return ""

    # --------------------------------------------------------
    # متن را خط به خط پردازش می‌کنیم
    # --------------------------------------------------------

    lines = text.split("\n")

    final_lines = []

    for line in lines:

        # اگر خط خالی است
        if not line:

            final_lines.append("")
            continue

        # ----------------------------------------------------
        # فاصله‌ها را حفظ می‌کنیم
        # ----------------------------------------------------

        words = line.split(" ")

        shaped_words = []

        for word in words:

            if word:

                shaped_words.append(
                    shape_persian_word(word)
                )

            else:

                shaped_words.append("")

        # ----------------------------------------------------
        # نکته مهم:
        #
        # کلمات فارسی نباید با reversed(words)
        # برگردانده شوند.
        #
        # ترتیب منطقی جمله حفظ می‌شود.
        # ----------------------------------------------------

        final_lines.append(
            " ".join(shaped_words)
        )

    return "\n".join(final_lines)


# ============================================================
# PERSIAN LABEL
# ============================================================

class PersianLabel(Label):

    def __init__(self, **kwargs):

        original_text = kwargs.get(
            "text",
            ""
        )

        kwargs["text"] = prepare_persian_text(
            original_text
        )

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

    def _update_text_size(
        self,
        *args
    ):

        self.text_size = (
            self.width,
            None
        )

    def set_text(
        self,
        text
    ):

        self.text = prepare_persian_text(
            text
        )


# ============================================================
# PERSIAN BUTTON
# ============================================================

class PersianButton(Button):

    def __init__(self, **kwargs):

        original_text = kwargs.get(
            "text",
            ""
        )

        kwargs["text"] = prepare_persian_text(
            original_text
        )

        kwargs["font_name"] = "PersianFont"

        kwargs.setdefault(
            "font_size",
            sp(16)
        )

        super().__init__(**kwargs)

        self.bind(
            size=self._update_text_size
        )

    def _update_text_size(
        self,
        *args
    ):

        self.text_size = self.size

    def set_text(
        self,
        text
    ):

        self.text = prepare_persian_text(
            text
        )


# ============================================================
# MAIN APP
# ============================================================

class BazaarYarApp(App):

    def build(self):

        self.title = "BazaarYar"

        self.menu_open = False

        self.root_layout = FloatLayout()

        # ====================================================
        # MAIN CONTENT
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

        top.add_widget(
            menu_button
        )

        top.add_widget(
            title
        )

        main.add_widget(
            top
        )

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

        main.add_widget(
            subtitle
        )

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

        main.add_widget(
            search_title
        )

        # ====================================================
        # SEARCH BOX
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
            hint_text=prepare_persian_text(
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

        main.add_widget(
            search_box
        )

        # ====================================================
        # RESULT AREA
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

        main.add_widget(
            scroll
        )

        # ====================================================
        # BOTTOM NAVIGATION
        # ====================================================

        bottom = BoxLayout(
            orientation="horizontal",
            spacing=dp(6),
            size_hint_y=None,
            height=dp(60)
        )

        home_button = PersianButton(
            text="خانه"
        )

        market_button = PersianButton(
            text="بازار"
        )

        account_button = PersianButton(
            text="حساب"
        )

        home_button.bind(
            on_release=lambda x:
            self.show_message(
                "صفحه اصلی بازاریار"
            )
        )

        market_button.bind(
            on_release=lambda x:
            self.show_message(
                "بخش بازار"
            )
        )

        account_button.bind(
            on_release=lambda x:
            self.show_message(
                "حساب کاربری"
            )
        )

        bottom.add_widget(
            home_button
        )

        bottom.add_widget(
            market_button
        )

        bottom.add_widget(
            account_button
        )

        main.add_widget(
            bottom
        )

        self.root_layout.add_widget(
            main
        )

        # ====================================================
        # SIDE MENU
        # ====================================================

        self.create_side_menu()

        return self.root_layout

    # ========================================================
    # CREATE SIDE MENU
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

        # ----------------------------------------------------
        # TITLE
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
        # ITEMS
        # ----------------------------------------------------

        items = [

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
                "درباره بازاریار\n\n"
                "دستیار هوشمند بازار"
            )
        ]

        for title_text, message in items:

            button = PersianButton(
                text=title_text,
                size_hint_y=None,
                height=dp(52)
            )

            button.bind(
                on_release=lambda instance,
                msg=message:
                self.show_message_and_close(
                    msg
                )
            )

            self.side_menu.add_widget(
                button
            )

        # ----------------------------------------------------
        # CLOSE
        # ----------------------------------------------------

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
    # MENU
    # ========================================================

    def toggle_menu(
        self,
        *args
    ):

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

    def close_menu(
        self,
        *args
    ):

        self.menu_open = False

        self.side_menu.pos_hint = {
            "x": -1,
            "y": 0
        }

    # ========================================================
    # SIDE MENU BACKGROUND
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

    def search(
        self,
        *args
    ):

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

        self.show_message(
            message
        )

        self.close_menu()

    def show_message(
        self,
        message
    ):

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
# START
# ============================================================

if __name__ == "__main__":
    BazaarYarApp().run()
