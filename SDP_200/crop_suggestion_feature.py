"""Crop suggestions based on saved catalog growing conditions."""
import sqlite3
from contextlib import closing
from tkinter import ttk

import customtkinter as ctk

from crop_data import LEVELS, SEASONS, SOIL_TYPES
from finance_data import BASE_DIR
from ui_theme import (
    BODY_BOLD, BODY_FONT, BORDER, BUTTON_FONT, COMBO_STYLE, DANGER, DEW,
    INK, LEAF, LEAF_HOVER, MUTED, PAGE_FONT, PAPER, PINE, SAGE,
    SECTION_FONT,
)


def open_crop_suggestion(parent):
    return open_suggestion_from_database(parent)


def open_suggestion_from_database(parent):
    win = ctk.CTkFrame(parent, fg_color=DEW)

    header = ctk.CTkFrame(win, fg_color=PINE, corner_radius=0)
    header.pack(fill='x')
    ctk.CTkLabel(
        header, text='Crop suggestions', font=PAGE_FONT, text_color=PAPER
    ).pack(anchor='w', padx=24, pady=(16, 2))
    ctk.CTkLabel(
        header, text='Match growing conditions with crops already in your catalog.',
        font=BODY_FONT, text_color=SAGE
    ).pack(anchor='w', padx=24, pady=(0, 14))

    card = ctk.CTkFrame(
        win, fg_color=PAPER, border_width=1, border_color=BORDER,
        corner_radius=12)
    card.pack(fill='x', padx=18, pady=(18, 10))
    ctk.CTkLabel(
        card, text='Growing conditions', font=SECTION_FONT, text_color=PINE
    ).pack(anchor='w', padx=18, pady=(14, 4))
    ctk.CTkLabel(
        card, text='Choose the conditions available on the farm.',
        font=BODY_FONT, text_color=MUTED
    ).pack(anchor='w', padx=18, pady=(0, 10))

    form = ctk.CTkFrame(card, fg_color='transparent')
    form.pack(fill='x', padx=12, pady=4)
    form.grid_columnconfigure((0, 1), weight=1, uniform='suggestion_fields')

    def create_combobox(label, values, row, column):
        box = ctk.CTkFrame(form, fg_color='transparent')
        box.grid(row=row, column=column, sticky='ew', padx=8, pady=6)
        ctk.CTkLabel(
            box, text=label, font=BODY_BOLD, text_color=INK
        ).pack(anchor='w', pady=(0, 4))
        combo = ttk.Combobox(
            box, values=values, state='readonly', style=COMBO_STYLE)
        combo.pack(fill='x')
        combo.current(0)
        return combo

    soil_cb = create_combobox('Soil type', SOIL_TYPES, 0, 0)
    season_cb = create_combobox('Season', SEASONS, 0, 1)
    sunlight_cb = create_combobox('Sunlight requirement', LEVELS, 1, 0)
    water_cb = create_combobox('Water requirement', LEVELS, 1, 1)

    result_win = ctk.CTkScrollableFrame(
        win, label_text='Suggested crops', label_font=SECTION_FONT,
        fg_color=PAPER, border_width=1, border_color=BORDER,
        label_text_color=PINE, corner_radius=12)
    result_win.pack(fill='both', expand=True, padx=18, pady=(8, 18))

    def result_message(text, error=False):
        for child in result_win.winfo_children():
            child.destroy()
        ctk.CTkLabel(
            result_win, text=text, font=BODY_FONT,
            text_color=DANGER if error else MUTED, wraplength=680
        ).pack(padx=16, pady=22)

    def search_crop():
        try:
            with closing(sqlite3.connect(BASE_DIR / 'crops.db')) as conn:
                results = conn.execute('''
                    SELECT crop_name, category, days_to_harvest
                    FROM crops
                    WHERE soil_type=? AND sunlight=? AND water_req=? AND season=?
                    ORDER BY crop_name COLLATE NOCASE
                ''', (soil_cb.get(), sunlight_cb.get(), water_cb.get(),
                      season_cb.get())).fetchall()
        except sqlite3.Error as exc:
            result_message(f'Cannot search crops: {exc}', error=True)
            return

        for child in result_win.winfo_children():
            child.destroy()
        if not results:
            result_message(
                'No matching crop found. Try a different combination of growing conditions.')
            return

        for name, category, days in results:
            item = ctk.CTkFrame(
                result_win, fg_color=DEW, border_width=1,
                border_color=BORDER, corner_radius=10)
            item.pack(fill='x', padx=10, pady=6)
            ctk.CTkLabel(
                item, text=name, font=SECTION_FONT, text_color=PINE
            ).pack(anchor='w', padx=14, pady=(10, 2))
            ctk.CTkLabel(
                item, text=f'{category}  •  About {days} days to harvest',
                font=BODY_FONT, text_color=MUTED
            ).pack(anchor='w', padx=14, pady=(0, 10))

    ctk.CTkButton(
        card, text='Search Crop', width=165, height=40,
        fg_color=LEAF, hover_color=LEAF_HOVER, font=BUTTON_FONT,
        command=search_crop
    ).pack(anchor='w', padx=20, pady=(10, 16))

    result_message('Choose growing conditions, then select Search Crop.')
    return win
