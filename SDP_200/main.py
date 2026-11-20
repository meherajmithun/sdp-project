"""Single-window Smart Agricultural System."""
import sqlite3
from contextlib import closing
import customtkinter as ctk

from crop_management_feature import open_crop_management
from crop_suggestion_feature import open_crop_suggestion
from sales_tracker_feature import open_sales_tracker
from expense_tracker_feature import open_expense_tracker
from finance_ui import FinanceDashboard
from finance_data import BASE_DIR
from ui_theme import (
    BODY_BOLD, BODY_FONT, BORDER, BUTTON_FONT, DANGER, DANGER_HOVER,
    DEW, DISPLAY_FONT, INK, LEAF, LEAF_HOVER, MUTED, PAPER, PINE,
    PINE_DARK, SAGE, configure_ttk,
)


class Login_Window:
    def __init__(self, root):
        self.root = root
        root.title('Smart Agricultural System')
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        configure_ttk(root)
        screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
        width = min(1280, max(1000, screen_width - 100))
        height = min(820, max(700, screen_height - 100))
        root.geometry(f'{width}x{height}+{max(20, (screen_width-width)//2)}+{max(20, (screen_height-height)//2)}')
        root.minsize(1000, 700)
        self.fullscreen = False
        root.attributes('-fullscreen', False)
        root.bind('<Escape>', lambda event: self.set_fullscreen(False))
        root.bind('<F11>', lambda event: self.set_fullscreen(not self.fullscreen))
        toolbar = ctk.CTkFrame(root, fg_color=PINE, corner_radius=0, height=64)
        toolbar.pack(fill='x')
        ctk.CTkLabel(
            toolbar, text='SMART AGRICULTURAL SYSTEM', text_color=PAPER,
            font=DISPLAY_FONT
        ).pack(side='left', padx=24, pady=14)
        ctk.CTkButton(
            toolbar, text='Exit app', width=92, height=36, command=root.destroy,
            fg_color=DANGER, hover_color=DANGER_HOVER, font=BUTTON_FONT
        ).pack(side='right', padx=(8, 18), pady=12)
        self.fullscreen_button = ctk.CTkButton(
            toolbar, text='Full screen', width=122, height=36,
            command=lambda: self.set_fullscreen(not self.fullscreen),
            fg_color='transparent', hover_color=PINE_DARK, border_width=1,
            border_color=SAGE, text_color=PAPER, font=BUTTON_FONT)
        self.fullscreen_button.pack(side='right', padx=4, pady=12)
        self.body = ctk.CTkFrame(root, fg_color=DEW, corner_radius=0)
        self.body.pack(fill='both', expand=True)
        self.setup_database()
        self.show_cover()

    def set_fullscreen(self, enabled):
        self.fullscreen = enabled
        self.root.attributes('-fullscreen', enabled)
        self.fullscreen_button.configure(text='Exit full screen' if enabled else 'Full screen')
        return 'break'

    def clear_body(self):
        for child in self.body.winfo_children():
            child.destroy()
        self.pages = {}

    def setup_database(self):
        with closing(sqlite3.connect(BASE_DIR / 'admininfo.db')) as conn, conn:
            conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL)')

    def account_form(self, title):
        self.clear_body()
        panel = ctk.CTkFrame(
            self.body, fg_color=PAPER, width=440, border_width=1,
            border_color=BORDER, corner_radius=16)
        panel.place(relx=0.5, rely=0.5, anchor='center')
        ctk.CTkLabel(panel, text='FIELD ACCESS', font=BODY_BOLD,
                     text_color=LEAF).pack(padx=45, pady=(28, 4))
        ctk.CTkLabel(panel, text=title, font=DISPLAY_FONT,
                     text_color=PINE).pack(padx=45, pady=(0, 22))
        ctk.CTkLabel(panel, text='Username', text_color=INK,
                     font=BODY_BOLD).pack(anchor='w', padx=34)
        self.txtuser = ctk.CTkEntry(
            panel, width=340, height=42, fg_color=DEW, border_color=BORDER,
            text_color=INK, font=BODY_FONT)
        self.txtuser.pack(padx=30, pady=(5, 15))
        ctk.CTkLabel(panel, text='Password', text_color=INK,
                     font=BODY_BOLD).pack(anchor='w', padx=34)
        self.txtpass = ctk.CTkEntry(
            panel, width=340, height=42, show='*', fg_color=DEW,
            border_color=BORDER, text_color=INK, font=BODY_FONT)
        self.txtpass.pack(padx=30, pady=(5, 15))
        self.account_status = ctk.CTkLabel(
            panel, text='', text_color=DANGER, wraplength=340, font=BODY_FONT)
        self.account_status.pack(padx=30, pady=5)
        return panel

    def show_cover(self):
        """Show the product welcome screen before authentication."""
        self.clear_body()
        cover = ctk.CTkFrame(self.body, fg_color=DEW, corner_radius=0)
        cover.pack(fill='both', expand=True)

        # A quiet field-line motif gives the welcome screen an agricultural
        # signature without requiring external image assets.
        field = ctk.CTkFrame(cover, fg_color=PINE, corner_radius=0, width=430)
        field.pack(side='left', fill='y')
        field.pack_propagate(False)
        ctk.CTkLabel(
            field, text='SMART AGRICULTURAL SYSTEM', font=BODY_BOLD,
            text_color=SAGE
        ).pack(anchor='w', padx=42, pady=(54, 10))
        ctk.CTkLabel(
            field, text='A clearer season\nstarts here.', font=DISPLAY_FONT,
            text_color=PAPER, justify='left'
        ).pack(anchor='w', padx=42)
        ctk.CTkLabel(
            field,
            text='Plan crops, understand your growing conditions,\nand keep every taka in view.',
            font=BODY_FONT, text_color=SAGE, justify='left'
        ).pack(anchor='w', padx=42, pady=(18, 0))

        motif = ctk.CTkFrame(field, fg_color='transparent', height=230)
        motif.pack(fill='x', padx=42, pady=(46, 0))
        motif.pack_propagate(False)
        for index, width in enumerate((260, 220, 180, 140)):
            row = ctk.CTkFrame(
                motif, fg_color=LEAF if index % 2 == 0 else SAGE,
                height=2, width=width
            )
            row.place(x=index * 18, y=30 + index * 42)
        ctk.CTkLabel(
            field, text='CROPS  /  RECORDS  /  DECISIONS',
            font=BODY_BOLD, text_color='#A9CDB2'
        ).pack(anchor='w', padx=42, side='bottom', pady=38)

        content = ctk.CTkFrame(cover, fg_color=DEW, corner_radius=0)
        content.pack(side='right', fill='both', expand=True)
        ctk.CTkLabel(
            content, text='Welcome to your farm workspace',
            font=DISPLAY_FONT, text_color=PINE
        ).pack(anchor='w', padx=58, pady=(110, 8))
        ctk.CTkLabel(
            content,
            text='Everything you need to make the next growing decision\nwith more confidence.',
            font=BODY_FONT, text_color=MUTED, justify='left'
        ).pack(anchor='w', padx=58)

        actions = ctk.CTkFrame(content, fg_color='transparent')
        actions.pack(anchor='w', padx=58, pady=(38, 0))
        ctk.CTkButton(
            actions, text='Sign in', width=180, height=46,
            command=self.show_login, fg_color=LEAF, hover_color=LEAF_HOVER,
            font=BUTTON_FONT
        ).pack(side='left')
        ctk.CTkButton(
            actions, text='Create an account', width=180, height=46,
            command=self.register, fg_color=SAGE, hover_color=BORDER,
            text_color=PINE, font=BUTTON_FONT
        ).pack(side='left', padx=12)

        ctk.CTkLabel(
            content,
            text='Your data stays on this computer. Start with a crop catalog,\nthen add sales and expenses as your season grows.',
            font=BODY_FONT, text_color=MUTED, justify='left'
        ).pack(anchor='w', padx=58, pady=(62, 0))

    def show_login(self, message=''):
        panel = self.account_form('Welcome back')
        self.account_status.configure(text=message)
        ctk.CTkButton(panel, text='Login', command=self.login, width=340, height=42,
                      fg_color=LEAF, hover_color=LEAF_HOVER, font=BUTTON_FONT).pack(padx=30, pady=8)
        ctk.CTkButton(panel, text='Create an account', command=self.register, width=340, height=40,
                      fg_color=SAGE, hover_color=BORDER, text_color=PINE,
                      font=BUTTON_FONT).pack(padx=30, pady=8)
        ctk.CTkButton(panel, text='Forgot Password?', command=self.forgot_password, width=340,
                      fg_color='transparent', hover_color=DEW, text_color=MUTED,
                      font=BODY_FONT).pack(padx=30, pady=(6, 24))
        ctk.CTkButton(panel, text='Back to welcome', command=self.show_cover, width=340,
                      fg_color='transparent', hover_color=DEW, text_color=MUTED,
                      font=BODY_FONT).pack(padx=30, pady=(0, 20))
        self.txtpass.bind('<Return>', lambda event: self.login())
        self.txtuser.focus_set()

    def login(self):
        username, password = self.txtuser.get().strip(), self.txtpass.get()
        if not username or not password:
            self.account_status.configure(text='Enter your username and password.')
            return
        try:
            with closing(sqlite3.connect(BASE_DIR / 'admininfo.db')) as conn:
                found = conn.execute('SELECT 1 FROM users WHERE username=? AND password=?', (username, password)).fetchone()
        except sqlite3.Error as exc:
            self.account_status.configure(text=f'Cannot sign in: {exc}')
            return
        if found:
            self.username = username
            self.open_dashboard()
        else:
            self.account_status.configure(text='Invalid username or password.')

    def register(self):
        panel = self.account_form('Create account')
        def save_user():
            username, password = self.txtuser.get().strip(), self.txtpass.get()
            if not username or not password:
                self.account_status.configure(text='Enter a username and password.')
                return
            try:
                with closing(sqlite3.connect(BASE_DIR / 'admininfo.db')) as conn, conn:
                    conn.execute('INSERT INTO users VALUES (?, ?)', (username, password))
            except sqlite3.IntegrityError:
                self.account_status.configure(text='Username already exists.')
                return
            except sqlite3.Error as exc:
                self.account_status.configure(text=f'Cannot register: {exc}')
                return
            self.show_login('Account created. You can now sign in.')
        ctk.CTkButton(panel, text='Register', command=save_user, width=340, height=42,
                      fg_color=LEAF, hover_color=LEAF_HOVER, font=BUTTON_FONT).pack(padx=30, pady=8)
        ctk.CTkButton(panel, text='Back to login', command=self.show_login, width=340,
                      fg_color=SAGE, hover_color=BORDER, text_color=PINE,
                      font=BUTTON_FONT).pack(padx=30, pady=(8, 24))

    def forgot_password(self):
        self.account_status.configure(text='Password recovery is not available yet.')

    def open_dashboard(self):
        self.clear_body()
        sidebar = ctk.CTkFrame(self.body, width=224, fg_color=PINE, corner_radius=0)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        ctk.CTkLabel(sidebar, text='YOUR FARM', font=BODY_BOLD,
                     text_color='#A9CDB2').pack(anchor='w', padx=20, pady=(24, 3))
        ctk.CTkLabel(sidebar, text=self.username, wraplength=180, font=BODY_FONT,
                     text_color=PAPER).pack(anchor='w', padx=20, pady=(0, 20))
        self.content = ctk.CTkFrame(self.body, fg_color=DEW, corner_radius=0)
        self.content.pack(side='right', fill='both', expand=True)
        self.builders = {'Dashboard': FinanceDashboard, 'Crop Management': open_crop_management,
                         'Crop Suggestion': open_crop_suggestion, 'Sales Tracker': open_sales_tracker,
                         'Expense Tracker': open_expense_tracker}
        self.nav_buttons = {}
        for name in self.builders:
            button = ctk.CTkButton(
                sidebar, text=name, width=192, height=44, anchor='w',
                command=lambda page=name: self.show_page(page),
                fg_color='transparent', hover_color=LEAF_HOVER,
                text_color=PAPER, font=BUTTON_FONT)
            button.pack(padx=16, pady=5)
            self.nav_buttons[name] = button
        ctk.CTkButton(
            sidebar, text='Logout', width=192, height=42, command=self.logout,
            fg_color=DANGER, hover_color=DANGER_HOVER, font=BUTTON_FONT
        ).pack(side='bottom', padx=16, pady=18)
        self.show_page('Dashboard')

    def show_page(self, name):
        if name not in self.pages:
            try:
                self.pages[name] = self.builders[name](self.content)
            except (sqlite3.Error, OSError) as exc:
                page = ctk.CTkFrame(self.content, fg_color=DEW)
                ctk.CTkLabel(page, text=f'Cannot load {name}: {exc}', wraplength=600,
                             text_color=DANGER, font=BODY_FONT).pack(pady=30)
                self.pages[name] = page
        for page in self.pages.values():
            page.pack_forget()
        self.pages[name].pack(fill='both', expand=True)
        self.current_page = self.pages[name]
        for label, button in self.nav_buttons.items():
            button.configure(
                fg_color=LEAF if label == name else 'transparent',
                text_color=PAPER)
        self.root.event_generate('<<FinanceChanged>>', when='tail')

    def logout(self):
        self.username = ''
        self.show_login()


if __name__ == '__main__':
    ctk.set_appearance_mode('light')
    ctk.set_default_color_theme('green')
    root = ctk.CTk()
    app = Login_Window(root)
    root.mainloop()
