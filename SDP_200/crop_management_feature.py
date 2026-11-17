"""Crop catalog management page."""
import sqlite3
from tkinter import ttk

import customtkinter as ctk

from crop_data import CATEGORIES, LEVELS, SEASONS, SOIL_TYPES, CropStore


def open_crop_management(parent, store=None):
    store = store or CropStore()
    win = ctk.CTkFrame(parent, fg_color='#f4f8f1')

    header = ctk.CTkFrame(win, fg_color='#1e5631', corner_radius=0)
    header.pack(fill='x')
    ctk.CTkLabel(
        header, text='Crop Management', font=('Verdana', 22, 'bold'),
        text_color='white'
    ).pack(anchor='w', padx=22, pady=(16, 4))
    ctk.CTkLabel(
        header, text='Build a reliable crop catalog for suggestions and farm records.',
        text_color='#d9f2df'
    ).pack(anchor='w', padx=22, pady=(0, 16))

    content = ctk.CTkScrollableFrame(win, fg_color='transparent')
    content.pack(fill='both', expand=True, padx=14, pady=14)

    form_card = ctk.CTkFrame(content, fg_color='white', border_width=1,
                             border_color='#c8ddca')
    form_card.pack(fill='x', padx=4, pady=(0, 12))

    mode_bar = ctk.CTkFrame(form_card, fg_color='#e8f5e9', corner_radius=8)
    mode_bar.pack(fill='x', padx=14, pady=(14, 8))
    mode_label = ctk.CTkLabel(
        mode_bar, text='Adding a crop', font=('Verdana', 15, 'bold'),
        text_color='#1b5e20'
    )
    mode_label.pack(anchor='w', padx=14, pady=(9, 2))
    mode_help = ctk.CTkLabel(
        mode_bar, text='Enter the growing details, then choose Add Crop.',
        text_color='#315b38'
    )
    mode_help.pack(anchor='w', padx=14, pady=(0, 9))

    form = ctk.CTkFrame(form_card, fg_color='transparent')
    form.pack(padx=18, pady=8)
    form.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(form, text='Crop name').grid(
        row=0, column=0, sticky='w', pady=7, padx=(0, 18))
    crop_name = ctk.CTkEntry(form, width=360, placeholder_text='Example: Rice')
    crop_name.grid(row=0, column=1, sticky='ew', pady=7)

    ctk.CTkLabel(form, text='Days to harvest').grid(
        row=1, column=0, sticky='w', pady=7, padx=(0, 18))
    days_to_harvest = ctk.CTkEntry(form, width=360, placeholder_text='Example: 120')
    days_to_harvest.grid(row=1, column=1, sticky='ew', pady=7)

    def add_combo(label, values, row):
        ctk.CTkLabel(form, text=label).grid(
            row=row, column=0, sticky='w', pady=7, padx=(0, 18))
        combo = ttk.Combobox(form, values=values, state='readonly', width=43)
        combo.grid(row=row, column=1, sticky='ew', pady=7)
        combo.current(0)
        return combo

    soil = add_combo('Soil type', SOIL_TYPES, 2)
    sunlight = add_combo('Sunlight requirement', LEVELS, 3)
    water = add_combo('Water requirement', LEVELS, 4)
    category = add_combo('Crop category', CATEGORIES, 5)
    season = add_combo('Season', SEASONS, 6)

    status = ctk.CTkLabel(form_card, text='', wraplength=680)
    status.pack(fill='x', padx=18, pady=(4, 2))

    form_actions = ctk.CTkFrame(form_card, fg_color='transparent')
    form_actions.pack(fill='x', padx=18, pady=(8, 16))
    primary_button = ctk.CTkButton(form_actions, text='Add Crop', width=145,
                                   fg_color='#2e7d32')
    primary_button.pack(side='left')
    clear_button = ctk.CTkButton(form_actions, text='Clear Form', width=120,
                                 fg_color='#607d65')
    clear_button.pack(side='left', padx=10)

    table_card = ctk.CTkFrame(content, fg_color='white', border_width=1,
                              border_color='#c8ddca')
    table_card.pack(fill='both', expand=True, padx=4, pady=(0, 8))
    table_heading = ctk.CTkFrame(table_card, fg_color='transparent')
    table_heading.pack(fill='x', padx=14, pady=(14, 6))
    ctk.CTkLabel(
        table_heading, text='Saved crops', font=('Verdana', 16, 'bold'),
        text_color='#1b5e20'
    ).pack(side='left')
    crop_count = ctk.CTkLabel(table_heading, text='')
    crop_count.pack(side='right')

    table_frame = ctk.CTkFrame(table_card, fg_color='transparent')
    table_frame.pack(fill='both', expand=True, padx=14, pady=6)
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    columns = ('ID', 'Crop', 'Days', 'Soil', 'Sunlight', 'Water', 'Category', 'Season')
    tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                        selectmode='browse', height=9)
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

    table_message = ctk.CTkLabel(table_card, text='', text_color='#526b56')
    table_message.pack(fill='x', padx=14, pady=(2, 4))
    table_actions = ctk.CTkFrame(table_card, fg_color='transparent')
    table_actions.pack(fill='x', padx=14, pady=(4, 14))
    edit_button = ctk.CTkButton(table_actions, text='Edit Selected', width=130,
                                fg_color='#8a6d1d')
    edit_button.pack(side='left')
    refresh_button = ctk.CTkButton(table_actions, text='Refresh List', width=115,
                                   fg_color='#607d65')
    refresh_button.pack(side='left', padx=10)

    editing_id = None

    def set_status(message, error=False):
        status.configure(text=message, text_color='#b71c1c' if error else '#1b5e20')

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
        primary_button.configure(text='Add Crop', fg_color='#2e7d32')
        if clear_message:
            set_status('')

    def selected_id():
        selection = tree.selection()
        if not selection:
            set_status('Select a crop from the table first.', True)
            return None
        return int(selection[0])

    def refresh_table(select=None):
        try:
            crops = store.list_crops()
        except (sqlite3.Error, OSError) as exc:
            set_status(f'Cannot load crops: {exc}', True)
            return
        for item in tree.get_children():
            tree.delete(item)
        for crop in crops:
            tree.insert('', 'end', iid=str(crop['id']), values=(
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
        primary_button.configure(text='Save Changes', fg_color='#8a6d1d')
        set_status('Editing mode is active. Clear the form to cancel.')
        crop_name.focus_set()

    primary_button.configure(command=save_crop)
    clear_button.configure(command=clear_form)
    edit_button.configure(command=edit_selected)
    refresh_button.configure(command=refresh_table)
    tree.bind('<Double-1>', edit_selected)
    refresh_table()
    return win
