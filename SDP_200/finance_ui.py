"""Shared field-ledger widgets for finance dashboards and trackers."""
from datetime import date
import sqlite3
from tkinter import Misc, filedialog, ttk

import customtkinter as ctk

from finance_data import CATEGORIES, FinanceStore, export_csv, money
from ui_theme import (
    BODY_BOLD, BODY_FONT, BORDER, BUTTON_FONT, COMBO_STYLE, DANGER,
    DANGER_HOVER, DEW, INK, LEAF, LEAF_HOVER, MUTED, PAGE_FONT, PAPER,
    PINE, SAGE, SECTION_FONT, SOIL, SOIL_HOVER, TREE_STYLE, VALUE_FONT,
    WARNING, WARNING_INK, style_tree_rows,
)


def table(parent, columns, height=9, expand=True, fixed_height=None):
    frame = ctk.CTkFrame(
        parent, fg_color=PAPER, border_width=1, border_color=BORDER,
        corner_radius=10)
    frame.pack(fill='both' if expand else 'x', expand=expand, padx=16, pady=8)
    if fixed_height:
        frame.configure(height=fixed_height)
        frame.pack_propagate(False)
    tree = ttk.Treeview(
        frame, columns=columns, show='headings', selectmode='browse',
        height=height, style=TREE_STYLE)
    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=125, minwidth=85)
    vertical = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
    horizontal = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
    tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    tree.grid(row=0, column=0, sticky='nsew', padx=(1, 0), pady=(1, 0))
    vertical.grid(row=0, column=1, sticky='ns', pady=(1, 0))
    horizontal.grid(row=1, column=0, sticky='ew', padx=(1, 0), pady=(0, 1))
    style_tree_rows(tree)
    return tree


def insert_striped(tree, index, **kwargs):
    kwargs['tags'] = ('even' if index % 2 == 0 else 'odd',)
    return tree.insert('', 'end', **kwargs)


def crop_choices(store):
    return {f'{name} (#{crop_id})': crop_id for crop_id, name in store.crops()}


def open_tracker(kind, parent=None, on_change=None, store=None):
    store = store or FinanceStore()
    sale = kind == 'sales'
    title = 'Sales tracker' if sale else 'Expense tracker'
    subtitle = ('Record harvest income and review every sale.' if sale else
                'Record farm costs and understand where money is going.')
    win = ctk.CTkFrame(parent, fg_color=DEW)

    header = ctk.CTkFrame(win, fg_color=PINE, corner_radius=0)
    header.pack(fill='x')
    ctk.CTkLabel(header, text=title, font=PAGE_FONT, text_color=PAPER).pack(
        anchor='w', padx=24, pady=(16, 2))
    ctk.CTkLabel(header, text=subtitle, font=BODY_FONT, text_color=SAGE).pack(
        anchor='w', padx=24, pady=(0, 14))

    notice = ctk.CTkLabel(
        win, text='', text_color=DANGER, font=BODY_FONT, wraplength=760)
    notice.pack(fill='x', padx=20, pady=(8, 0))
    tabs = ctk.CTkTabview(
        win, fg_color=PAPER, border_width=1, border_color=BORDER,
        segmented_button_fg_color=SAGE,
        segmented_button_selected_color=LEAF,
        segmented_button_selected_hover_color=LEAF_HOVER,
        segmented_button_unselected_color=SAGE,
        segmented_button_unselected_hover_color=BORDER,
        text_color=INK)
    tabs.pack(fill='both', expand=True, padx=18, pady=12)
    add_tab = tabs.add('Add Sale' if sale else 'Add Expense')
    view_tab = tabs.add('View Sales' if sale else 'View Expenses')
    add_tab.configure(fg_color=PAPER)
    view_tab.configure(fg_color=PAPER)

    form = ctk.CTkFrame(
        add_tab, fg_color=DEW, border_width=1, border_color=BORDER,
        corner_radius=12)
    form.pack(padx=24, pady=22)
    fields = {}
    labels = ['Crop', 'Quantity (kg)', 'Price per kg (BDT)', 'Date (DD-MM-YYYY)'] if sale else [
        'Crop', 'Category', 'Amount (BDT)', 'Date (DD-MM-YYYY)', 'Notes (optional)']
    choices = {}
    for i, label in enumerate(labels):
        ctk.CTkLabel(form, text=label, font=BODY_BOLD, text_color=INK).grid(
            row=i, column=0, padx=(22, 24), pady=10, sticky='w')
        if label in ('Crop', 'Category'):
            widget = ttk.Combobox(
                form, state='readonly', width=34, style=COMBO_STYLE)
            if label == 'Category':
                widget.configure(values=CATEGORIES)
                widget.current(0)
        else:
            widget = ctk.CTkEntry(
                form, width=300, height=38, fg_color=PAPER,
                border_color=BORDER, text_color=INK, font=BODY_FONT)
            if label.startswith('Date'):
                widget.insert(0, date.today().strftime('%d-%m-%Y'))
        widget.grid(row=i, column=1, padx=(0, 22), pady=10, sticky='ew')
        fields[label] = widget

    def refresh_crops():
        choices.clear()
        choices.update(crop_choices(store))
        fields['Crop'].configure(values=list(choices))
        if fields['Crop'].get() not in choices:
            fields['Crop'].set(next(iter(choices), 'Add a crop first'))

    columns = ('ID', 'Crop', 'Qty (kg)', 'Price (BDT)', 'Total (BDT)', 'Date') if sale else (
        'ID', 'Crop', 'Category', 'Amount (BDT)', 'Date', 'Notes')
    tree = table(view_tab, columns, height=10)
    status = ctk.CTkLabel(view_tab, text='', font=BODY_FONT, text_color=MUTED)
    status.pack(pady=4)

    def refresh():
        try:
            refresh_crops()
            names = dict(store.crops())
            rows = store.rows(kind)
            for item in tree.get_children():
                tree.delete(item)
            for index, row in enumerate(rows):
                if sale:
                    amount = money(row['total_paisa']) if row['total_paisa'] is not None else 'Invalid amount'
                    crop_label = names.get(row['crop_id'], row['crop_name'] or 'Unassigned')
                    values = (row['id'], crop_label, row['quantity'], row['price'], amount, row['date'])
                else:
                    values = (row['id'], names.get(row['crop_id'], 'Unassigned'), row['category'],
                              money(row['amount_paisa']), row['date'], row['notes'])
                insert_striped(tree, index, iid=str(row['id']), values=values)
            total = store.report()['revenue' if sale else 'expenses']
            status.configure(
                text=f'{len(rows)} records  •  Total BDT {money(total)}' if rows else
                     'No records yet. Add the first entry from the other tab.')
        except (sqlite3.Error, OSError, ValueError) as exc:
            notice.configure(text=f'Cannot load records: {exc}')

    def changed():
        refresh()
        win._root().event_generate('<<FinanceChanged>>', when='tail')
        if on_change:
            on_change()

    def save():
        try:
            crop_id = choices.get(fields['Crop'].get())
            entered_date = fields['Date (DD-MM-YYYY)'].get()
            if sale:
                store.add_sale(crop_id, fields['Quantity (kg)'].get(),
                               fields['Price per kg (BDT)'].get(), entered_date)
            else:
                store.add_expense(crop_id, fields['Category'].get(),
                                  fields['Amount (BDT)'].get(), entered_date,
                                  fields['Notes (optional)'].get())
        except (ValueError, sqlite3.Error, OSError) as exc:
            notice.configure(text=f'Cannot save: {exc}', text_color=DANGER)
            return
        for label, widget in fields.items():
            if label not in ('Crop', 'Category'):
                widget.delete(0, 'end')
                if label.startswith('Date'):
                    widget.insert(0, date.today().strftime('%d-%m-%Y'))
        notice.configure(text='Record saved.', text_color=LEAF)
        changed()
        tabs.set('View Sales' if sale else 'View Expenses')

    pending_delete = None

    def cancel_delete():
        nonlocal pending_delete
        pending_delete = None
        confirmation.pack_forget()

    def delete():
        nonlocal pending_delete
        selected = tree.selection()
        if not selected:
            notice.configure(text='Select one row to delete.', text_color=DANGER)
            return
        pending_delete = int(selected[0])
        confirmation.pack(fill='x', padx=16, pady=8)

    def confirm_delete():
        if pending_delete is None:
            return
        try:
            store.delete(kind, pending_delete)
        except sqlite3.Error as exc:
            notice.configure(text=f'Cannot delete: {exc}', text_color=DANGER)
            return
        cancel_delete()
        notice.configure(text='Record deleted.', text_color=LEAF)
        changed()

    confirmation = ctk.CTkFrame(
        view_tab, fg_color=WARNING, border_width=1, border_color=SOIL)
    ctk.CTkLabel(
        confirmation, text='Permanently delete the selected record?',
        text_color=WARNING_INK, font=BODY_BOLD
    ).pack(side='left', padx=12)
    ctk.CTkButton(
        confirmation, text='Confirm delete', command=confirm_delete,
        fg_color=DANGER, hover_color=DANGER_HOVER, font=BUTTON_FONT
    ).pack(side='left', padx=5, pady=8)
    ctk.CTkButton(
        confirmation, text='Cancel', command=cancel_delete, width=80,
        fg_color=SAGE, hover_color=BORDER, text_color=PINE, font=BUTTON_FONT
    ).pack(side='left', padx=5)

    ctk.CTkButton(
        add_tab, text='Save Sale' if sale else 'Save Expense', command=save,
        fg_color=LEAF, hover_color=LEAF_HOVER, font=BUTTON_FONT,
        width=160, height=40
    ).pack(pady=(4, 8))
    ctk.CTkButton(
        add_tab, text='Refresh crop list', command=refresh,
        fg_color='transparent', hover_color=SAGE, text_color=PINE,
        border_width=1, border_color=BORDER, font=BODY_FONT
    ).pack(pady=5)
    actions = ctk.CTkFrame(view_tab, fg_color='transparent')
    actions.pack(fill='x', padx=16, pady=8)
    ctk.CTkButton(
        actions, text='Refresh', command=refresh, fg_color=SAGE,
        hover_color=BORDER, text_color=PINE, font=BUTTON_FONT
    ).pack(side='left', padx=4, pady=8)
    ctk.CTkButton(
        actions, text='Delete Selected', command=delete,
        fg_color=DANGER, hover_color=DANGER_HOVER, font=BUTTON_FONT
    ).pack(side='right', padx=4)
    bind_refresh(win, refresh)
    refresh()
    return win


def bind_refresh(widget, callback):
    root = widget._root()
    if not hasattr(root, '_finance_listeners'):
        root._finance_listeners = {}

        def notify(event):
            for listener in list(root._finance_listeners.values()):
                listener()
        root.bind('<<FinanceChanged>>', notify, add='+')
    root._finance_listeners[widget] = callback

    def cleanup(event):
        if event.widget == widget:
            root._finance_listeners.pop(widget, None)
    Misc.bind(widget, '<Destroy>', cleanup, add='+')


class FinanceDashboard(ctk.CTkFrame):
    def __init__(self, parent, store=None):
        super().__init__(parent, fg_color=DEW)
        self.store = store or FinanceStore()

        heading = ctk.CTkFrame(self, fg_color='transparent')
        heading.pack(fill='x', padx=22, pady=(18, 8))
        ctk.CTkLabel(
            heading, text='Farm finances', font=PAGE_FONT, text_color=PINE
        ).pack(anchor='w')
        ctk.CTkLabel(
            heading, text='A clear view of recorded income, costs, and balance.',
            font=BODY_FONT, text_color=MUTED
        ).pack(anchor='w', pady=(2, 0))

        filters = ctk.CTkFrame(
            self, fg_color=PAPER, border_width=1, border_color=BORDER,
            corner_radius=12)
        filters.pack(fill='x', padx=18, pady=8)
        ctk.CTkLabel(filters, text='FILTER RECORDS', font=BODY_BOLD,
                     text_color=LEAF).grid(row=0, column=0, columnspan=5,
                                           sticky='w', padx=14, pady=(10, 2))
        self.crop = ttk.Combobox(
            filters, state='readonly', width=23, style=COMBO_STYLE)
        self.crop.grid(row=1, column=0, padx=(14, 6), pady=(4, 12))
        self.start = ctk.CTkEntry(
            filters, placeholder_text='From DD-MM-YYYY', width=165, height=38,
            fg_color=DEW, border_color=BORDER, text_color=INK, font=BODY_FONT)
        self.end = ctk.CTkEntry(
            filters, placeholder_text='To DD-MM-YYYY', width=165, height=38,
            fg_color=DEW, border_color=BORDER, text_color=INK, font=BODY_FONT)
        self.start.grid(row=1, column=1, padx=6, pady=(4, 12))
        self.end.grid(row=1, column=2, padx=6, pady=(4, 12))
        ctk.CTkButton(
            filters, text='Apply filters', command=self.refresh, width=112,
            height=38, fg_color=LEAF, hover_color=LEAF_HOVER,
            font=BUTTON_FONT
        ).grid(row=1, column=3, padx=(10, 5), pady=(4, 12))
        ctk.CTkButton(
            filters, text='Export CSV', command=self.export, width=105,
            height=38, fg_color=SOIL, hover_color=SOIL_HOVER,
            font=BUTTON_FONT
        ).grid(row=1, column=4, padx=(5, 14), pady=(4, 12))

        self.cards = []
        cards = ctk.CTkFrame(self, fg_color='transparent')
        cards.pack(fill='x', padx=18, pady=8)
        card_colors = (SAGE, WARNING, '#E4EFE8')
        for i, (title, color) in enumerate(zip(
                ('Sales revenue', 'Recorded expenses', 'Surplus / deficit'), card_colors)):
            cards.grid_columnconfigure(i, weight=1)
            card = ctk.CTkFrame(
                cards, fg_color=color, border_width=1, border_color=BORDER,
                corner_radius=12)
            card.grid(row=0, column=i, sticky='nsew', padx=5)
            ctk.CTkLabel(
                card, text=title, font=BODY_BOLD, text_color=MUTED
            ).pack(padx=12, pady=(13, 3))
            value = ctk.CTkLabel(
                card, text='BDT 0.00', font=VALUE_FONT, text_color=PINE)
            value.pack(padx=12, pady=(3, 14))
            self.cards.append(value)

        ctk.CTkLabel(
            self, text='RECENT RECORDS', font=BODY_BOLD, text_color=LEAF
        ).pack(anchor='w', padx=22, pady=(6, 0))
        self.tree = table(
            self, ('Type', 'Crop', 'Date', 'Amount (BDT)'),
            height=8, expand=False, fixed_height=285)
        self.status = ctk.CTkTextbox(
            self, height=70, wrap='word', fg_color=PAPER,
            border_width=1, border_color=BORDER, text_color=INK,
            font=BODY_FONT, corner_radius=10)
        self.status.pack(fill='x', padx=18, pady=7)
        ctk.CTkLabel(
            self,
            text='Recorded revenue minus expenses; unsold harvests and missing costs are not included.',
            wraplength=760, text_color=MUTED, font=BODY_FONT
        ).pack(padx=18, pady=(2, 12))
        self.choices = {}
        bind_refresh(self, self.refresh)
        self.refresh()

    def set_status(self, text, warning=False):
        self.status.configure(
            state='normal', fg_color=WARNING if warning else PAPER,
            text_color=WARNING_INK if warning else INK)
        self.status.delete('1.0', 'end')
        self.status.insert('1.0', text)
        self.status.configure(state='disabled')

    def read_report(self):
        return self.store.report(
            self.choices.get(self.crop.get()), self.start.get(), self.end.get())

    def refresh(self):
        try:
            self.choices = {
                'All Crops': None, 'Unassigned records': 'unassigned',
                **crop_choices(self.store)}
            self.crop.configure(values=list(self.choices))
            if self.crop.get() not in self.choices:
                self.crop.set('All Crops')
            report = self.read_report()
        except (ValueError, sqlite3.Error, OSError) as exc:
            self.set_status(f'Cannot refresh report: {exc}', warning=True)
            return None
        for label, key in zip(self.cards, ('revenue', 'expenses', 'balance')):
            label.configure(
                text=f'BDT {money(report[key])}',
                text_color=DANGER if report[key] < 0 else PINE)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for index, row in enumerate(report['records']):
            insert_striped(
                self.tree, index,
                values=(row['kind'].title(), row['crop'], row['date'],
                        money(row['amount_paisa'])))
        message = '\n'.join(report['warnings']) or (
            'No records for these filters.' if not report['records'] else
            f'{len(report["records"])} records shown. All amounts are in BDT.')
        self.set_status(message, warning=bool(report['warnings']))
        return report

    def export(self):
        try:
            report = self.refresh()
            if report is None:
                return
            path = filedialog.asksaveasfilename(
                parent=self, defaultextension='.csv',
                filetypes=[('CSV file', '*.csv')],
                initialfile='farm-finances.csv')
            if path:
                export_csv(path, report)
                self.set_status('Your filtered report has been saved.')
        except (ValueError, sqlite3.Error, OSError) as exc:
            self.set_status(f'Cannot export: {exc}', warning=True)
