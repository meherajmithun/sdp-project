"""Crop catalog management page."""
import sqlite3
from tkinter import ttk

import customtkinter as ctk

from crop_data import CATEGORIES, LEVELS, SEASONS, SOIL_TYPES, CropStore
from ui_theme import (
    BODY_BOLD, BODY_FONT, BORDER, BUTTON_FONT, COMBO_STYLE, DANGER,
    DANGER_HOVER, DEW, INK, LEAF, LEAF_HOVER, MUTED, PAGE_FONT, PAPER,
    PINE, SAGE, SECTION_FONT, SOIL, SOIL_HOVER, TREE_STYLE, WARNING,
    WARNING_INK, style_tree_rows,
)


def open_crop_management(parent, store=None):
    store = store or CropStore()
    win = ctk.CTkFrame(parent, fg_color=DEW)

    header = ctk.CTkFrame(win, fg_color=PINE, corner_radius=0)
    header.pack(fill='x')
    ctk.CTkLabel(
        header, text='Crop management', font=PAGE_FONT, text_color=PAPER
    ).pack(anchor='w', padx=22, pady=(16, 4))
    ctk.CTkLabel(
        header, text='Build a reliable crop catalog for suggestions and farm records.',
        font=BODY_FONT, text_color=SAGE
    ).pack(anchor='w', padx=22, pady=(0, 16))

    content = ctk.CTkScrollableFrame(win, fg_color='transparent')
    content.pack(fill='both', expand=True, padx=14, pady=14)

    form_card = ctk.CTkFrame(content, fg_color=PAPER, border_width=1,
                             border_color=BORDER, corner_radius=12)
    form_card.pack(fill='x', padx=4, pady=(0, 12))

    mode_bar = ctk.CTkFrame(form_card, fg_color=SAGE, corner_radius=9)
    mode_bar.pack(fill='x', padx=14, pady=(14, 8))
    mode_label = ctk.CTkLabel(
        mode_bar, text='Adding a crop', font=SECTION_FONT, text_color=PINE
    )
    mode_label.pack(anchor='w', padx=14, pady=(9, 2))
    mode_help = ctk.CTkLabel(
        mode_bar, text='Enter the growing details, then choose Add Crop.',
        font=BODY_FONT, text_color=MUTED
    )
    mode_help.pack(anchor='w', padx=14, pady=(0, 9))

    form = ctk.CTkFrame(form_card, fg_color='transparent')
    form.pack(fill='x', padx=18, pady=6)
    form.grid_columnconfigure((0, 1), weight=1, uniform='crop_fields')

    def field_box(label, row, column):
        box = ctk.CTkFrame(form, fg_color='transparent')
        box.grid(row=row, column=column, sticky='ew', padx=8, pady=5)
        ctk.CTkLabel(
            box, text=label, font=BODY_BOLD, text_color=INK
        ).pack(anchor='w', pady=(0, 4))
        return box

    crop_name_box = field_box('Crop name', 0, 0)
    crop_name = ctk.CTkEntry(
        crop_name_box, height=38, placeholder_text='Example: Rice',
        fg_color=DEW, border_color=BORDER, text_color=INK, font=BODY_FONT)
    crop_name.pack(fill='x')

    days_box = field_box('Days to harvest', 0, 1)
    days_to_harvest = ctk.CTkEntry(
        days_box, height=38, placeholder_text='Example: 120',
        fg_color=DEW, border_color=BORDER, text_color=INK, font=BODY_FONT)
    days_to_harvest.pack(fill='x')

    def add_combo(label, values, row, column):
        box = field_box(label, row, column)
        combo = ttk.Combobox(
            box, values=values, state='readonly', style=COMBO_STYLE)
        combo.pack(fill='x')
        combo.current(0)
        return combo

    soil = add_combo('Soil type', SOIL_TYPES, 1, 0)
    season = add_combo('Season', SEASONS, 1, 1)
    sunlight = add_combo('Sunlight requirement', LEVELS, 2, 0)
    water = add_combo('Water requirement', LEVELS, 2, 1)
    category = add_combo('Crop category', CATEGORIES, 3, 0)

    status = ctk.CTkLabel(
        form_card, text='', wraplength=760, font=BODY_FONT, text_color=LEAF)
    status.pack(fill='x', padx=18, pady=(4, 2))

    form_actions = ctk.CTkFrame(form_card, fg_color='transparent')
    form_actions.pack(fill='x', padx=18, pady=(8, 16))
    primary_button = ctk.CTkButton(
        form_actions, text='Add Crop', width=145, height=40,
        fg_color=LEAF, hover_color=LEAF_HOVER, font=BUTTON_FONT)
    primary_button.pack(side='left')
    clear_button = ctk.CTkButton(
        form_actions, text='Clear Form', width=120, height=40,
        fg_color=SAGE, hover_color=BORDER, text_color=PINE, font=BUTTON_FONT)
    clear_button.pack(side='left', padx=10)

    table_card = ctk.CTkFrame(content, fg_color=PAPER, border_width=1,
                              border_color=BORDER, corner_radius=12)
    table_card.pack(fill='both', expand=True, padx=4, pady=(0, 8))
    table_heading = ctk.CTkFrame(table_card, fg_color='transparent')
    table_heading.pack(fill='x', padx=14, pady=(14, 6))
    ctk.CTkLabel(
        table_heading, text='Saved crops', font=SECTION_FONT, text_color=PINE
    ).pack(side='left')
    crop_count = ctk.CTkLabel(
        table_heading, text='', font=BODY_FONT, text_color=MUTED)
    crop_count.pack(side='right')

    table_frame = ctk.CTkFrame(table_card, fg_color='transparent')
    table_frame.pack(fill='both', expand=True, padx=14, pady=6)
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    columns = ('ID', 'Crop', 'Days', 'Soil', 'Sunlight', 'Water', 'Category', 'Season')
    tree = ttk.Treeview(
        table_frame, columns=columns, show='headings', selectmode='browse',
        height=8, style=TREE_STYLE)
    widths = (55, 125, 70, 210, 85, 85, 100, 90)
    for column, width in zip(columns, widths):
        tree.heading(column, text=column)
        tree.column(column, width=width, minwidth=55)
    vertical = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
    horizontal = ttk.Scrollbar(table_frame, orient='horizontal', command=tree.xview)
    tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
    tree.grid(row=0, column=0, sticky='nsew')
    vertical.grid(row=0, column=1, sticky='ns')
    horizontal.grid(row=1, column=0, sticky='ew')
    style_tree_rows(tree)

    table_message = ctk.CTkLabel(
        table_card, text='', text_color=MUTED, font=BODY_FONT)
    table_message.pack(fill='x', padx=14, pady=(2, 4))
    table_actions = ctk.CTkFrame(table_card, fg_color='transparent')
    table_actions.pack(fill='x', padx=14, pady=(4, 14))
    edit_button = ctk.CTkButton(
        table_actions, text='Edit Selected', width=130, fg_color=SOIL,
        hover_color=SOIL_HOVER, font=BUTTON_FONT)
    edit_button.pack(side='left')
    refresh_button = ctk.CTkButton(
        table_actions, text='Refresh List', width=115, fg_color=SAGE,
        hover_color=BORDER, text_color=PINE, font=BUTTON_FONT)
    refresh_button.pack(side='left', padx=10)
    delete_button = ctk.CTkButton(
        table_actions, text='Delete Selected', width=135, fg_color=DANGER,
        hover_color=DANGER_HOVER, font=BUTTON_FONT)
    delete_button.pack(side='right')
    samples_button = ctk.CTkButton(
        table_actions, text='Load Sample Crops', width=150, fg_color=LEAF,
        hover_color=LEAF_HOVER, font=BUTTON_FONT)
    samples_button.pack(side='right', padx=10)

    confirmation = ctk.CTkFrame(table_card, fg_color=WARNING,
                                border_width=1, border_color=SOIL)
    confirmation_label = ctk.CTkLabel(
        confirmation, text='', wraplength=560, text_color=WARNING_INK,
        font=BODY_BOLD)
    confirmation_label.pack(side='left', fill='x', expand=True, padx=12, pady=10)
    confirm_button = ctk.CTkButton(confirmation, text='Confirm', width=115)
    confirm_button.pack(side='left', padx=5, pady=8)
    cancel_button = ctk.CTkButton(
        confirmation, text='Cancel', width=80, fg_color=SAGE,
        hover_color=BORDER, text_color=PINE, font=BUTTON_FONT)
    cancel_button.pack(side='left', padx=(5, 10), pady=8)

    editing_id = None

    def set_status(message, error=False):
        status.configure(text=message, text_color=DANGER if error else LEAF)

    def form_values():
        return dict(
            crop_name=crop_name.get(),
            days_to_harvest=days_to_harvest.get(),
            soil_type=soil.get(),
            sunlight=sunlight.get(),
            water_req=water.get(),
            category=category.get(),
            season=season.get(),
        )

    def clear_form(clear_message=True):
        nonlocal editing_id
        editing_id = None
        crop_name.delete(0, 'end')
        days_to_harvest.delete(0, 'end')
        for combo in (soil, sunlight, water, category, season):
            combo.current(0)
        mode_label.configure(text='Adding a crop')
        mode_help.configure(text='Enter the growing details, then choose Add Crop.')
        primary_button.configure(
            text='Add Crop', fg_color=LEAF, hover_color=LEAF_HOVER)
        if clear_message:
            set_status('')

    def selected_id():
        selection = tree.selection()
        if not selection:
            set_status('Select a crop from the table first.', True)
            return None
        return int(selection[0])

    def hide_confirmation():
        confirmation.pack_forget()

    def show_confirmation(message, button_text, command, dangerous=False):
        confirmation_label.configure(text=message)
        confirm_button.configure(
            text=button_text, command=command,
            fg_color=DANGER if dangerous else LEAF,
            hover_color=DANGER_HOVER if dangerous else LEAF_HOVER,
            font=BUTTON_FONT)
        confirmation.pack(fill='x', padx=14, pady=(0, 14))

    def refresh_table(select=None):
        try:
            crops = store.list_crops()
        except (sqlite3.Error, OSError) as exc:
            set_status(f'Cannot load crops: {exc}', True)
            return
        for item in tree.get_children():
            tree.delete(item)
        for index, crop in enumerate(crops):
            tree.insert('', 'end', iid=str(crop['id']),
                        tags=('even' if index % 2 == 0 else 'odd',), values=(
                crop['id'], crop['crop_name'], crop['days_to_harvest'],
                crop['soil_type'], crop['sunlight'], crop['water_req'],
                crop['category'], crop['season']))
        crop_count.configure(text=f'{len(crops)} saved crop' + ('' if len(crops) == 1 else 's'))
        table_message.configure(
            text='Select a crop to edit it.' if crops else
                 'No crops saved yet. Add your first crop above or load sample crops later.')
        if select is not None and tree.exists(str(select)):
            tree.selection_set(str(select))
            tree.see(str(select))

    def save_crop():
        nonlocal editing_id
        try:
            if editing_id is None:
                crop_id = store.add(**form_values())
                message = 'Crop added successfully.'
            else:
                crop_id = editing_id
                store.update(crop_id, **form_values())
                message = 'Crop changes saved.'
        except (ValueError, sqlite3.Error, OSError) as exc:
            set_status(str(exc), True)
            return
        clear_form(clear_message=False)
        refresh_table(crop_id)
        set_status(message)
        win._root().event_generate('<<FinanceChanged>>', when='tail')

    def edit_selected(event=None):
        nonlocal editing_id
        crop_id = selected_id()
        if crop_id is None:
            return
        try:
            crop = store.get(crop_id)
        except (sqlite3.Error, OSError) as exc:
            set_status(f'Cannot load the crop: {exc}', True)
            return
        if not crop:
            set_status('The selected crop no longer exists. Refresh the list.', True)
            refresh_table()
            return
        editing_id = crop_id
        hide_confirmation()
        crop_name.delete(0, 'end')
        crop_name.insert(0, crop['crop_name'] or '')
        days_to_harvest.delete(0, 'end')
        days_to_harvest.insert(0, crop['days_to_harvest'] or '')
        soil.set(crop['soil_type'] if crop['soil_type'] in SOIL_TYPES else SOIL_TYPES[0])
        sunlight.set(crop['sunlight'] if crop['sunlight'] in LEVELS else LEVELS[0])
        water.set(crop['water_req'] if crop['water_req'] in LEVELS else LEVELS[0])
        category.set(crop['category'] if crop['category'] in CATEGORIES else CATEGORIES[0])
        season.set(crop['season'] if crop['season'] in SEASONS else SEASONS[0])
        mode_label.configure(text=f"Editing {crop['crop_name']} (#{crop_id})")
        mode_help.configure(text='Update the fields, then choose Save Changes.')
        primary_button.configure(
            text='Save Changes', fg_color=SOIL, hover_color=SOIL_HOVER)
        set_status('Editing mode is active. Clear the form to cancel.')
        crop_name.focus_set()

    def delete_crop(crop_id):
        nonlocal editing_id
        try:
            crop = store.get(crop_id)
            store.delete(crop_id)
        except (ValueError, sqlite3.Error, OSError) as exc:
            hide_confirmation()
            set_status(str(exc), True)
            return
        if editing_id == crop_id:
            clear_form(clear_message=False)
        hide_confirmation()
        refresh_table()
        set_status(f"'{crop['crop_name']}' was deleted.")
        win._root().event_generate('<<FinanceChanged>>', when='tail')

    def request_delete():
        crop_id = selected_id()
        if crop_id is None:
            return
        try:
            crop = store.get(crop_id)
            references = store.reference_counts(crop_id)
        except (sqlite3.Error, OSError) as exc:
            set_status(f'Cannot check the crop: {exc}', True)
            return
        if not crop:
            set_status('The selected crop no longer exists. Refresh the list.', True)
            refresh_table()
            return
        if references['sales'] or references['expenses']:
            set_status(
                f"'{crop['crop_name']}' is used by {references['sales']} sale(s) and "
                f"{references['expenses']} expense(s). Keep the crop to protect those records.",
                True)
            return
        show_confirmation(
            f"Permanently delete '{crop['crop_name']}'? This cannot be undone.",
            'Confirm Delete', lambda: delete_crop(crop_id), dangerous=True)

    def load_samples():
        try:
            added = store.load_samples()
        except (ValueError, sqlite3.Error, OSError) as exc:
            hide_confirmation()
            set_status(f'Cannot load sample crops: {exc}', True)
            return
        hide_confirmation()
        refresh_table()
        if added:
            set_status(f'{added} sample crop' + ('' if added == 1 else 's') + ' added.')
            win._root().event_generate('<<FinanceChanged>>', when='tail')
        else:
            set_status('All sample crops are already in the catalog.')

    def request_samples():
        show_confirmation(
            'Add five starter crops? Existing crop names will be skipped.',
            'Load Samples', load_samples)

    primary_button.configure(command=save_crop)
    clear_button.configure(command=clear_form)
    edit_button.configure(command=edit_selected)
    refresh_button.configure(command=refresh_table)
    delete_button.configure(command=request_delete)
    samples_button.configure(command=request_samples)
    cancel_button.configure(command=hide_confirmation)
    tree.bind('<Double-1>', edit_selected)
    refresh_table()
    return win
