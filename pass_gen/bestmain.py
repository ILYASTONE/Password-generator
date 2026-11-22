import flet as ft
from flet import Colors
import string
from random import choice
import asyncio


class PasswordGeneratorApp:
    def __init__(self):
        # Настройки по умолчанию
        self.password_settings = {
            "length": 12,
            "use_specials": True,
            "exclude_similar": True,
            "save_to_file": False
        }

        # Поля для пользовательского ввода при сохранении
        self.login_input_value = ""
        self.service_input_value = ""

        # Словари с переводами
        self.translations = {
            "ru": {
                "title": "🛡️ ГЕНЕРАТОР ПАРОЛЕЙ",
                "generate_section": "ГЕНЕРАЦИЯ ПАРОЛЯ",
                "generate_btn": "✨ Сгенерировать пароль",
                "copy_tooltip": "Копировать пароль",
                "save_disabled": "⏸️ Сохранение в файл отключено",
                "save_success": "💾 Пароль сохранен в passwords.txt",
                "save_error": "❌ Ошибка сохранения: ",
                "settings_section": "НАСТРОЙКИ",
                "length_text": "Длина: ",
                "specials_label": "Спецсимволы (!@#$%^&*)",
                "similar_label": "Исключить похожие (l,1,O,0)",
                "save_label": "Сохранять в файл",
                "check_section": "ПРОВЕРИТЬ СВОЙ ПАРОЛЬ",
                "check_input_label": "Введите пароль для проверки",
                "check_empty": "❌ Введите пароль для проверки!",
                "strong": "🟢 НАДЕЖНЫЙ",
                "medium": "🟡 СРЕДНИЙ",
                "weak": "🔴 СЛАБЫЙ",
                "length_info": "Длина: ",
                "copied": "✅ Пароль скопирован в буфер обмена!",
                "about": "ℹ️ Автор: Ilyastone\nTelegram: @Ilyastone\nTikTok: @ilyastone10\nEmail: Ilyastone10@gmail.com\nВерсия: 2.2 (Логин)",
                "language_label": "Язык:",
                "check_btn": "🔍 Проверить надежность",
                "crack_time": "⏱️ Время взлома: ",
                "service_label": "Сервис / Аккаунт:",
                "login_label": "Логин / Email:",
                "dialog_generate": "🔑 Сгенерировать и сохранить",
                "dialog_cancel": "❌ Отмена",
                "fill_service_login": "⚠️ Заполните Сервис и Логин!",
                "file_data_header": "📝 Данные для записи в файл",
                "dialog_hint_text": "Пароль появится здесь после нажатия зеленой кнопки."
            },
            "en": {
                "title": "🛡️ PASSWORD GENERATOR",
                "generate_section": "PASSWORD GENERATION",
                "generate_btn": "✨ Generate Password",
                "copy_tooltip": "Copy password",
                "save_disabled": "⏸️ Save to file disabled",
                "save_success": "💾 Password saved to passwords.txt",
                "save_error": "❌ Save error: ",
                "settings_section": "SETTINGS",
                "length_text": "Length: ",
                "specials_label": "Special chars (!@#$%^&*)",
                "similar_label": "Exclude similar (l,1,O,0)",
                "save_label": "Save to file",
                "check_section": "CHECK YOUR PASSWORD",
                "check_input_label": "Enter password to check",
                "check_empty": "❌ Enter password to check!",
                "strong": "🟢 STRONG",
                "medium": "🟡 MEDIUM",
                "weak": "🔴 WEAK",
                "length_info": "Length: ",
                "copied": "✅ Password copied to clipboard!",
                "about": "ℹ️ Author: Ilyastone\nTelegram: @Ilyastone\nTikTok: @ilyastone10\nEmail: Ilyastone10@gmail.com\nVersion: 2.2 (Login)",
                "language_label": "Language:",
                "check_btn": "🔍 check reliability",
                "crack_time": "⏱️ Crack time: ",
                "service_label": "Service / Account:",
                "login_label": "Login / Email:",
                "dialog_generate": "🔑 Generate & Save",
                "dialog_cancel": "❌ Cancel",
                "fill_service_login": "⚠️ Fill in Service and Login!",
                "file_data_header": "📝 Data to be saved to file",
                "dialog_hint_text": "The password will appear here after clicking the green button."
            }
        }

        # Текущий язык
        self.current_lang = "ru"

    def t(self, key):
        """Получение перевода по ключу"""
        return self.translations[self.current_lang][key]

    def main(self, page: ft.Page):
        # Настройка страницы
        self.page = page
        page.title = "Генератор паролей"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 20
        page.scroll = ft.ScrollMode.AUTO
        page.window_width = 400
        page.window_height = 750

        # --- ЗАГОЛОВКИ И ТЕКСТЫ ДЛЯ ОБНОВЛЕНИЯ ЯЗЫКА ---
        self.generate_section_title = ft.Text(
            self.t("generate_section"), size=18, weight=ft.FontWeight.BOLD
        )
        self.settings_section_title = ft.Text(
            self.t("settings_section"), size=18, weight=ft.FontWeight.BOLD
        )
        self.check_section_title = ft.Text(
            self.t("check_section"), size=18, weight=ft.FontWeight.BOLD
        )
        self.specials_label_text = ft.Text(self.t("specials_label"))
        self.similar_label_text = ft.Text(self.t("similar_label"))
        self.save_label_text = ft.Text(self.t("save_label"))
        self.about_text = ft.Text(
            self.t("about"),
            size=14,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.GREY_400
        )

        # НОВЫЙ АТРИБУТ: ссылка на текст заголовка данных файла
        self.file_data_header = ft.Text(
            self.t("file_data_header"),
            size=16,
            weight=ft.FontWeight.BOLD
        )

        # Переключатель языка
        self.lang_toggle = ft.Row([
            ft.Text(self.t("language_label"), size=16),
            ft.Text("RU", size=20),
            ft.Switch(
                value=False,
                on_change=self.toggle_language,
                active_color=ft.Colors.BLUE_400
            ),
            ft.Text("EN", size=20),
        ], alignment=ft.MainAxisAlignment.CENTER)

        # Заголовок приложения
        self.title = ft.Text(
            self.t("title"),
            size=28,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        # Поле для вывода пароля
        self.password_output = ft.TextField(
            value="",
            read_only=True,
            text_align=ft.TextAlign.CENTER,
            text_size=18,
            border_color=ft.Colors.BLUE_400,
            bgcolor=ft.Colors.BLACK12,
        )

        # Статус сохранения
        self.status_text = ft.Text(
            self.t("save_disabled"),
            size=14,
            color=ft.Colors.GREY_400,
            text_align=ft.TextAlign.CENTER
        )

        # Кнопка генерации теперь открывает диалог
        self.generate_btn = ft.ElevatedButton(
            self.t("generate_btn"),
            on_click=self.show_save_dialog,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20
            ),
            width=300
        )

        copy_btn = ft.IconButton(
            icon=ft.Icons.COPY,
            tooltip=self.t("copy_tooltip"),
            on_click=self.copy_password,
            icon_color=ft.Colors.BLUE_400
        )

        # Настройки
        length_slider = ft.Slider(
            min=6,
            max=50,
            divisions=44,
            value=self.password_settings["length"],
            label="{value} символов",
            on_change=self.change_length
        )

        self.length_text = ft.Text(f"{self.t('length_text')}{self.password_settings['length']}")

        self.specials_switch = ft.Switch(
            value=self.password_settings["use_specials"],
            on_change=self.toggle_specials,
            active_color=ft.Colors.BLUE_400
        )

        self.similar_switch = ft.Switch(
            value=self.password_settings["exclude_similar"],
            on_change=self.toggle_similar,
            active_color=ft.Colors.BLUE_400
        )

        self.save_switch = ft.Switch(
            value=self.password_settings["save_to_file"],
            on_change=self.toggle_save,
            active_color=ft.Colors.BLUE_400
        )

        # НОВЫЕ ПОЛЯ ВВОДА
        self.service_input = ft.TextField(
            label=self.t("service_label"),
            hint_text="Например: Google аккаунт",
            width=300
        )

        self.login_input = ft.TextField(
            label=self.t("login_label"),
            hint_text="example@gmail.com",
            width=300
        )

        # Поле для проверки пароля
        self.check_input = ft.TextField(
            label=self.t("check_input_label"),
            password=True,
            can_reveal_password=True,
            border_color=ft.Colors.BLUE_400,
            width=300
        )

        self.check_result = ft.Text(
            "",
            size=16,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        self.check_btn = ft.ElevatedButton(
            self.t("check_btn"),
            on_click=self.check_password,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            width=300
        )

        # Собираем интерфейс
        page.add(
            ft.Column([
                self.lang_toggle,
                self.title,
                ft.Divider(height=20, color=ft.Colors.BLUE_400),

                # Секция генерации
                self.generate_section_title,
                self.password_output,
                ft.Row([
                    self.generate_btn,
                    copy_btn
                ], alignment=ft.MainAxisAlignment.CENTER),
                self.status_text,

                ft.Divider(height=20, color=ft.Colors.BLUE_400),

                # Секция настроек
                self.settings_section_title,
                self.length_text,
                length_slider,

                ft.Row([
                    self.specials_label_text,
                    self.specials_switch
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Row([
                    self.similar_label_text,
                    self.similar_switch
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Row([
                    self.save_label_text,
                    self.save_switch
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Divider(height=20, color=ft.Colors.BLUE_400),

                # НОВЫЕ ПОЛЯ ДЛЯ СОХРАНЕНИЯ (используем ссылку self.file_data_header)
                self.file_data_header,
                self.service_input,
                self.login_input,

                ft.Divider(height=20, color=ft.Colors.BLUE_400),

                # Секция проверки
                self.check_section_title,
                self.check_input,
                self.check_btn,
                self.check_result,

                ft.Divider(height=20, color=ft.Colors.BLUE_400),
                self.about_text
            ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            )
        )

        page.update()

    async def show_save_dialog(self, e):
        dialog_service = ft.TextField(
            label=self.t("service_label"),
            value=self.service_input.value,
            width=300
        )
        dialog_login = ft.TextField(
            label=self.t("login_label"),
            value=self.login_input.value,
            width=300
        )

        def close_dialog(e):
            setattr(dialog_service.page.dialog, 'open', False)
            self.page.update()

        generate_action = ft.TextButton(
            self.t("dialog_generate"),
            on_click=lambda _: self.save_with_data(dialog_service, dialog_login)
        )

        cancel_action = ft.TextButton(
            self.t("dialog_cancel"),
            on_click=close_dialog
        )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(self.t("generate_section")),
            content=ft.Column([
                dialog_service,
                dialog_login,
                ft.Text(size=12, color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER,
                        value=self.t("dialog_hint_text"))
            ], spacing=10),
            actions=[generate_action, cancel_action],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.dialog = dialog
        self.page.show_dialog(dialog)

    def save_with_data(self, service_field, login_field):
        """Генерирует пароль и сохраняет его вместе с данными из диалога"""
        service = service_field.value.strip()
        login = login_field.value.strip()

        if not service or not login:
            self.page.snack_bar = ft.SnackBar(content=ft.Text(self.t("fill_service_login")), open=True)
            return

        letters = string.ascii_letters
        digits = string.digits
        specials = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        pool = letters + digits

        if self.password_settings["use_specials"]:
            pool += specials

        if self.password_settings["exclude_similar"]:
            similar_chars = "l1I0O"
            for char in similar_chars:
                pool = pool.replace(char, "")

        length = self.password_settings["length"]
        password = "".join(choice(pool) for _ in range(length))

        # Обновляем UI
        self.password_output.value = password
        self.service_input.value = service
        self.login_input.value = login
        self.page.update()

        # --- БЛОК ДЛЯ СОХРАНЕНИЯ В ФАЙЛ ---
        labels = {
            "ru": {"service": "Сервис:", "login": "Логин:", "password": "Пароль:"},
            "en": {"service": "Service:", "login": "Login:", "password": "Password:"}
        }

        current_labels = labels[self.current_lang]

        if self.password_settings["save_to_file"]:
            try:
                with open("passwords.txt", "a", encoding="utf-8") as file:
                    file.write(f"{current_labels['service']} {service}\n")
                    file.write(f"{current_labels['login']} {login}\n")
                    file.write(f"{current_labels['password']} {password}\n")
                    file.write("\n")
                self.status_text.value = self.t("save_success")
                self.status_text.color = ft.Colors.GREEN_400
            except Exception as ex:
                self.status_text.value = f"{self.t('save_error')}{ex}"
                self.status_text.color = ft.Colors.RED_400
        else:
            self.status_text.value = self.t("save_disabled")
            self.status_text.color = ft.Colors.GREY_400

        self.status_text.update()
        self.page.close_drawer()

    def copy_password(self, e):
        """Копирование пароля в буфер обмена"""
        if self.password_output.value:
            self.page.set_clipboard(self.password_output.value)
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(self.t("copied")),
                    open=True
                )
            )

    def change_length(self, e):
        self.password_settings["length"] = int(e.control.value)
        self.length_text.value = f"{self.t('length_text')}{self.password_settings['length']}"
        self.length_text.update()

    def toggle_specials(self, e):
        """Переключение спецсимволов"""
        self.password_settings["use_specials"] = e.control.value

    def toggle_similar(self, e):
        """Переключение исключения похожих символов"""
        self.password_settings["exclude_similar"] = e.control.value

    def toggle_save(self, e):
        """Переключение сохранения в файл"""
        self.password_settings["save_to_file"] = e.control.value

    def toggle_language(self, e):
        """Переключение языка"""
        self.current_lang = "ru" if not e.control.value else "en"
        self.update_ui_language()
        self.page.update()

    def update_ui_language(self):
        """Обновление интерфейса при смене языка"""
        self.lang_toggle.controls[0].value = self.t("language_label")
        self.title.value = self.t("title")
        self.generate_section_title.value = self.t("generate_section")
        self.settings_section_title.value = self.t("settings_section")
        self.check_section_title.value = self.t("check_section")
        self.about_text.value = self.t("about")
        self.length_text.value = f"{self.t('length_text')}{self.password_settings['length']}"
        self.status_text.value = self.t("save_disabled")
        self.specials_label_text.value = self.t("specials_label")
        self.similar_label_text.value = self.t("similar_label")
        self.save_label_text.value = self.t("save_label")
        self.check_input.label = self.t("check_input_label")
        self.generate_btn.content = ft.Text(self.t("generate_btn"))
        self.check_btn.content = ft.Text(self.t("check_btn"))

        # Обновляем лейблы статичных полей ввода
        self.service_input.label = self.t("service_label")
        self.login_input.label = self.t("login_label")

        # КРИТИЧЕСКОЕ ДОБАВЛЕНИЕ: обновляем значение нашего нового атрибута
        self.file_data_header.value = self.t("file_data_header")

        # Подсказки тоже можно перевести при желании
        if not self.service_input.value:
            self.service_input.hint_text = ("Например: Google аккаунт" if self.current_lang == "ru"
                                            else "e.g.: Google account")
        if not self.login_input.value:
            self.login_input.hint_text = "example@gmail.com"

        if not self.password_output.value:
            self.password_output.hint_text = self.t("copy_tooltip")

        self.page.update()

    def check_password(self, e):
        """Проверка надежности пароля"""
        user_password = self.check_input.value.strip()

        if not user_password:
            self.check_result.value = self.t("check_empty")
            self.check_result.color = ft.Colors.RED_400
            self.check_result.update()
            return

        length = len(user_password)
        has_upper = any(c.isupper() for c in user_password)
        has_lower = any(c.islower() for c in user_password)
        has_digit = any(c.isdigit() for c in user_password)
        specials = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        has_special = any(c in specials for c in user_password)

        crack_time_value = self.calculate_crack_time(user_password)

        time_line = ""
        if crack_time_value:
            time_line = f"\n{self.t('crack_time')}{crack_time_value}"

        if length > 8 and has_special and has_digit and has_upper and has_lower:
            self.check_result.value = f"{self.t('strong')} ({self.t('length_info')}{length}){time_line}"
            self.check_result.color = ft.Colors.GREEN_400
        elif length >= 8 and (has_upper or has_lower) and has_digit and has_special:
            self.check_result.value = f"{self.t('medium')} ({self.t('length_info')}{length}){time_line}"
            self.check_result.color = ft.Colors.ORANGE_400
        else:
            self.check_result.value = f"{self.t('weak')} ({self.t('length_info')}{length}){time_line}"
            self.check_result.color = ft.Colors.RED_400

        self.check_result.update()

    def calculate_crack_time(self, password):
        """Расчет примерного времени взлома пароля"""
        length = len(password)
        pool_size = 0

        if any(c.islower() for c in password):
            pool_size += 26
        if any(c.isupper() for c in password):
            pool_size += 26
        if any(c.isdigit() for c in password):
            pool_size += 10

        specials = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if any(c in specials for c in password):
            pool_size += len(specials)

        if pool_size == 0:
            return ""

        combinations = pool_size ** length
        attempts_per_second = 10_000_000_000
        seconds = combinations / attempts_per_second

        if seconds < 1 and self.current_lang == "ru":
            return "мгновенно"
        elif seconds < 1 and self.current_lang == "en":
            return "instantly"
        elif seconds < 60 and self.current_lang == "ru":
            return f"{seconds:.0f} сек."
        elif seconds < 60 and self.current_lang == "en":
            return f"{seconds:.0f} sec."
        elif seconds < 3600 and self.current_lang == "ru":
            return f"{seconds / 60:.0f} мин."
        elif seconds < 3600 and self.current_lang == "en":
            return f"{seconds / 60:.0f} min."
        elif seconds < 86400 and self.current_lang == "ru":
            return f"{seconds / 3600:.0f} час."
        elif seconds < 86400 and self.current_lang == "en":
            return f"{seconds / 3600:.0f} h."
        elif seconds < 31536000 and self.current_lang == "ru":
            return f"{seconds / 86400:.0f} дн."
        elif seconds < 31536000 and self.current_lang == "en":
            return f"{seconds / 86400:.0f} d."
        elif seconds < 31536000 * 100 and self.current_lang == "ru":
            return f"{seconds / 31536000:.0f} лет"
        elif seconds < 31536000 * 100 and self.current_lang == "en":
            return f"{seconds / 31536000:.0f} y."
        elif seconds < 31536000 * 1000000 and self.current_lang == "ru":
            return f"{seconds / 31536000:.0f} лет 🔥"
        elif seconds < 31536000 * 1000000 and self.current_lang == "en":
            return f"{seconds / 31536000:.0f} y."
        elif seconds > 31536000 * 1000000 and self.current_lang == "ru":
            return f"{seconds / 31536000:.1e} лет 💀"
        else:
            return f"{seconds / 31536000:.1e} y. 💀"


def main():
    app = PasswordGeneratorApp()
    asyncio.run(ft.app_async(target=app.main))


if __name__ == "__main__":
    main()