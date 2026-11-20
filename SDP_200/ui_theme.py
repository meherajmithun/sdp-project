"""Shared field-ledger visual theme for the desktop application."""
from tkinter import ttk


# Palette: deep field greens, paper surfaces, and one harvest-gold accent.
PINE = '#183F2A'
PINE_DARK = '#102D1D'
LEAF = '#2F7D48'
LEAF_HOVER = '#276B3D'
SAGE = '#DDEBDF'
DEW = '#F3F8F3'
PAPER = '#FFFFFF'
SOIL = '#B7792B'
SOIL_HOVER = '#996322'
INK = '#17231B'
MUTED = '#5F6E63'
BORDER = '#C9D8CC'
DANGER = '#B63A3A'
DANGER_HOVER = '#972E2E'
WARNING = '#FFF2D8'
WARNING_INK = '#6D4B12'

DISPLAY_FONT = ('Avenir Next', 25, 'bold')
PAGE_FONT = ('Avenir Next', 22, 'bold')
SECTION_FONT = ('Avenir Next', 16, 'bold')
BODY_FONT = ('Helvetica Neue', 13)
BODY_BOLD = ('Helvetica Neue', 13, 'bold')
SMALL_FONT = ('Helvetica Neue', 11)
BUTTON_FONT = ('Helvetica Neue', 12, 'bold')
VALUE_FONT = ('Avenir Next', 18, 'bold')
TABLE_FONT = ('Helvetica Neue', 12)
TABLE_HEADING_FONT = ('Helvetica Neue', 11, 'bold')

TREE_STYLE = 'Field.Treeview'
COMBO_STYLE = 'Field.TCombobox'


def configure_ttk(root):
    """Force ttk controls into the light application palette on every OS."""
    style = ttk.Style(root)
    if 'clam' in style.theme_names():
        style.theme_use('clam')

    style.configure(
        TREE_STYLE,
        background=PAPER,
        fieldbackground=PAPER,
        foreground=INK,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        borderwidth=1,
        relief='flat',
        rowheight=32,
        font=TABLE_FONT,
    )
    style.configure(
        f'{TREE_STYLE}.Heading',
        background=PINE,
        foreground=PAPER,
        bordercolor=PINE,
        relief='flat',
        padding=(8, 8),
        font=TABLE_HEADING_FONT,
    )
    style.map(
        TREE_STYLE,
        background=[('selected', LEAF)],
        foreground=[('selected', PAPER)],
    )
    style.map(
        f'{TREE_STYLE}.Heading',
        background=[('active', PINE_DARK)],
    )

    style.configure(
        COMBO_STYLE,
        fieldbackground=PAPER,
        background=SAGE,
        foreground=INK,
        arrowcolor=PINE,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        padding=(9, 7),
        font=BODY_FONT,
    )
    style.map(
        COMBO_STYLE,
        fieldbackground=[('readonly', PAPER)],
        foreground=[('readonly', INK)],
        selectbackground=[('readonly', PAPER)],
        selectforeground=[('readonly', INK)],
        background=[('active', SAGE), ('readonly', SAGE)],
    )

    style.configure(
        'Vertical.TScrollbar', background=SAGE, troughcolor=DEW,
        bordercolor=DEW, arrowcolor=PINE)
    style.configure(
        'Horizontal.TScrollbar', background=SAGE, troughcolor=DEW,
        bordercolor=DEW, arrowcolor=PINE)
    return style


def style_tree_rows(tree):
    tree.tag_configure('even', background=PAPER, foreground=INK)
    tree.tag_configure('odd', background=DEW, foreground=INK)
