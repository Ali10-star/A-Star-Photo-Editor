"""
Widgets responsible for opening, displaying the image,
in addition to closing the editor menus.
"""

import tkinter
from typing import Callable
import customtkinter as ctk
from tkinter import Event, filedialog
from settings import *


class ImageImport(ctk.CTkFrame):
    """
    First frame to display when opening the app, allowing for opening of an image file.
    """
    def __init__(self, parent: ctk.CTk, import_func: Callable[[str], None]):
        super().__init__(master=parent)
        self.grid(column=0, columnspan=2, row=0, sticky='nsew')
        self.import_func = import_func
        ctk.CTkButton(self, text='Open Image', command=self.open_dialog).pack(expand=True)


    def open_dialog(self):
        """
        Ask user to select image file to open.
        """
        path = filedialog.askopenfile().name
        self.import_func(path)


class ImageOutput(tkinter.Canvas):
    """
    Main canvas that displays the open image.
    """
    def __init__(self, parent: ctk.CTk, resize_func: Callable[[Event], None]):
        super().__init__(master=parent, background=CANVAS_BACKGROUND,
                         bd=0, highlightthickness=0, relief='ridge')
        self.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self.bind('<Configure>', resize_func)


class CloseOutputButton(ctk.CTkButton):
    """
    Button to close the open image and editor menus.
    """
    def __init__(self, parent: ctk.CTk, close_func: Callable[[], None]):
        super().__init__(master=parent, text='X',
                         text_color=CLOSE_BUTTON_COLOR,
                         fg_color='transparent',
                         hover_color='firebrick2',
                         border_color='gray25',
                         width=40, height=40, command=close_func)
        self.place(relx = 0.99, rely = 0.02, anchor = 'ne')