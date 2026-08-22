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

from rtl.rtl_engine import prepare_rtl


# ============================================================
# PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

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
# PERSIAN LABEL
# ============================================================

class PersianLabel(Label):

    def __init__(self, **kwargs):

        text = kwargs.get(
            "text",
            ""
        )

        kwargs["text"] = prepare_rtl(text)

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

        self.text = prepare_rtl(text)


# ============================================================
# PERSIAN BUTTON
# ============================================================

class PersianButton(Button):

    def __init__(self, **kwargs):

        text = kwargs.get(
            "text",
            ""
        )

        kwargs["text"] = prepare_rtl(text)

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

        self.text = prepare_rtl(text)


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
            hint_text=prepare_rtl(
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
        # RESULT
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
        # BOTTOM
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


        for title, message in items:

            button = PersianButton(
                text=title,
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
# RUN
# ============================================================

if __name__ == "__main__":

    BazaarYarApp().run()
