"""
Reusable panel components, used throughout the app to display editor widgets.
"""
from typing import Callable, Optional
import customtkinter as ctk
import colorgram
from tkinter import filedialog, messagebox, END
from settings import *
from color_tools import hex_tools as HEX
from PIL.Image import Image


class Panel(ctk.CTkFrame):
    """
    Base Panel class.
    """
    def __init__(self, parent: ctk.CTkFrame) -> None:
        super().__init__(master=parent, fg_color=PANEL_BG)
        self.pack(fill='x', pady=4, ipady=8)


class CardPanel(ctk.CTkFrame):
    """
    Base card panel (primarily to display text).
    """
    def __init__(self, parent: ctk.CTkFrame, height: int = 200) -> None:
        super().__init__(master=parent, fg_color=PANEL_BG, height=height)
        self.pack(fill='both', pady=4, ipady=8)


class SliderPanel(Panel):
    """
    Panel containing a slider used to implement editor features.
    """
    def __init__(self, parent: ctk.CTkFrame,
                 panel_name: str, data_var: ctk.Variable,
                 min_value: int = 0,
                 max_value: int = 1):
        super().__init__(parent=parent)

        # Layout
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.panel_var = data_var
        self.panel_var.trace('w', self.update_text)

        ctk.CTkLabel(self, text=panel_name).grid(
            row=0, column=0, sticky='W', padx=10
        )
        self.num_label = ctk.CTkLabel(self, text=data_var.get())
        self.num_label.grid(row=0, column=1, sticky='E', padx=10)

        ctk.CTkSlider(
            self,
            fg_color=SLIDER_BG,
            variable=self.panel_var,
            from_=min_value,
            to=max_value,
        ).grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

    def update_text(self, *args):
        """
        Update SliderPanel label to match the slider's value.
        """
        self.num_label.configure(text=f'{round(self.panel_var.get(), 2)}')


class SegmentedPanel(Panel):
    """
    Panel with multiple grouped button using ctk.CTkSegmentedButton.
    """
    def __init__(self, parent: ctk.CTkFrame, panel_name: str, data_var: ctk.Variable,
                       options: list[str]) -> None:
        super().__init__(parent=parent)
        ctk.CTkLabel(self, text=panel_name).pack()
        ctk.CTkSegmentedButton(self, variable=data_var,
                               values=options).pack(expand=True, fill='both', padx=4, pady=4)


class SwitchPanel(Panel):
    """
    Panel supporting a varied-number of switches.
    """
    def __init__(self, parent: ctk.CTkFrame, *args):   # args: ((var1, text1), (var2, text2), ...)
        super().__init__(parent=parent)
        row, col = 0, 0
        for var, text in args:
            switch = ctk.CTkSwitch(
                self,
                text=text,
                variable=var,
                button_color=THEME_COLOR,
                fg_color=SLIDER_BG,
            )
            switch.grid(row=row, column=col, padx=20)
            col += 1
            if col > 1: col, row = 0, row + 1


class FileNamePanel(Panel):
    """
    Panel to name and select output file type.
    """
    def __init__(self, parent: ctk.CTkFrame, file_name: ctk.StringVar, file_extension: ctk.StringVar,
                 quality: ctk.IntVar):
        super().__init__(parent=parent)

        self.name = file_name
        self.name.trace('w', self.update_text)
        self.extension = file_extension
        self.image_quality = quality

        ctk.CTkLabel(self, text='Save Image As').pack(
            anchor='w', padx=20, pady=2
        )
        ctk.CTkEntry(self, textvariable=self.name).pack(
            fill='x', padx=20, pady=5
        )

        frame = ctk.CTkFrame(self, fg_color='transparent')
        jpg_check = ctk.CTkCheckBox(
            frame,
            text='JPG',
            variable=self.extension,
            command=lambda: self.update_extension('jpg'),
            onvalue='jpg',
            offvalue='png',
        )
        png_check = ctk.CTkCheckBox(
            frame,
            text='PNG',
            variable=self.extension,
            command=lambda: self.update_extension('png'),
            onvalue='png',
            offvalue='jpg',
        )
        jpg_check.pack(side='left', fill='x', expand=True)
        png_check.pack(side='left', fill='x', expand=True)
        frame.pack(expand=True, fill='x', padx=20)

        self.output = ctk.CTkLabel(
            self, text='example.jpg', fg_color=DARK_GREY, corner_radius=8
        )
        self.output.pack(pady=5)

        quality_frame = ctk.CTkFrame(self, fg_color='transparent')

        ctk.CTkLabel(quality_frame, text='Quality:').grid(row=0, column=0, padx=2)
        ctk.CTkEntry(quality_frame, width=45, textvariable=self.image_quality).grid(row=0, column=1)
        ctk.CTkLabel(quality_frame, text='%').grid(row=0, column=3, padx=1)

        quality_frame.pack(expand=True, fill='x', padx=82)


    def update_text(self, *args):
        """
        Replace output file's name with underscores instead of spaces,
        then preview the chosen name.
        """
        if self.name.get():
            fixed_text = (
                self.name.get().replace(' ', '_') + '.' + self.extension.get()
            )
            self.output.configure(text=fixed_text)

    def update_extension(self, selected_extension: str) -> None:
        """
        Set the output file extension and display the new file name.
        """
        self.extension.set(selected_extension)
        self.update_text()


class FilePathPanel(Panel):
    """
    Panel to select output folder for exporting.
    """
    def __init__(self, parent: ctk.CTkFrame, path_string: ctk.StringVar) -> None:
        super().__init__(parent=parent)
        self.path = path_string
        ctk.CTkLabel(self, text='Export Image To').pack(
            anchor='w', padx=5, pady=2
        )
        ctk.CTkEntry(self, textvariable=self.path).pack(
            expand=True, fill='x', padx=5, pady=5
        )
        ctk.CTkButton(
            self,
            text='Select output folder',
            command=self.select_file_location,
        ).pack(pady=2, padx=5, fill='x')

    def select_file_location(self) -> None:
        """
        Ask user to select the output directory to export image to.
        """
        self.path.set(filedialog.askdirectory())


class ThumbnailPanel(Panel):
    """
    Panel to create a thumbnail of the image and export it.
    """
    def __init__(self, parent: ctk.CTkFrame,
                 thumb_name: ctk.StringVar,
                 thumb_path: ctk.StringVar,
                 size: tuple[ctk.IntVar, ctk.IntVar],
                 save_thumb_func: Callable[[str, tuple[int, int], str], None]
        ) -> None:

        super().__init__(parent=parent)
        self.configure(height=200)
        self.thumb_name = thumb_name
        self.thumb_path = thumb_path
        self.thumb_width = size[0]
        self.thumb_height = size[1]
        self.save_thumb_func = save_thumb_func

        ctk.CTkLabel(self, text='Create thumbnail').place(relx=0.02, rely=0.01)

        ctk.CTkLabel(self, text='Width').place(relx=0.10, rely=0.18)
        ctk.CTkEntry(self, width=100, textvariable=self.thumb_width).place(relx=0.10, rely=0.30)

        ctk.CTkLabel(self, text='x').place(relx=0.485, rely=0.30)

        ctk.CTkLabel(self, text='Height').place(relx=0.55, rely=0.18)
        ctk.CTkEntry(self, width=100, textvariable=self.thumb_height).place(relx=0.55, rely=0.30)

        ctk.CTkLabel(self, text='Thumbnail name:').place(relx=0.02, rely=0.58)
        ctk.CTkEntry(self, width=270, textvariable=self.thumb_name).place(relx=0.02, rely=0.70)
        ctk.CTkButton(
            self,
            text='Save thumbnail to folder...',
            width=270,
            command=self.save_thumbnail_to,
        ).place(relx=0.02, rely=0.85)

    def save_thumbnail_to(self) -> None:
        """
        Ask user to select the output directory to export thumbnail to.
        """
        self.thumb_path.set(filedialog.askdirectory())
        size = (self.thumb_width.get(), self.thumb_height.get())
        self.save_thumb_func(self.thumb_name.get(), size,
                             self.thumb_path.get()
        )


class DropDownPanel(ctk.CTkOptionMenu):
    """
    Panel with a drop-down menu.
    """
    def __init__(self, parent: ctk.CTkFrame, data_var: ctk.Variable, options: list[str]) -> None:
        super().__init__(
            master=parent,
            values=options,
            fg_color=PANEL_BG,
            button_color=THEME_COLOR,
            button_hover_color=THEME_HOVER,
            dropdown_fg_color=DARK_GREY,
            variable=data_var,
        )
        self.pack(fill='x', pady=4)


class InfoPanel(CardPanel):
    """
    Card that displays information, with a header label.
    """
    def __init__(self, parent: ctk.CTkFrame, panel_name: str, info_str: str,
                 custom_height: int = 200) -> None:
        super().__init__(parent=parent, height=custom_height)

        # Layout
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            self, text=panel_name, font=('Open Sans', 13, 'bold')
        ).grid(row=0, column=0, sticky='W', padx=10)

        self.info = ctk.CTkTextbox(master=self, fg_color=PANEL_BG)
        self.info.insert('0.0', info_str)
        self.info.configure(state='disabled')
        self.info.grid(row=1, column=0, columnspan=2, sticky='ew')


class ColorsPanel(CardPanel):
    """
    Card to display extracted colors from the image.
    """
    def __init__(self, parent: ctk.CTkFrame, image_file: Image):
        super().__init__(parent=parent)
        self.image = image_file
        self.hex_colors = []
        self.run_button = ctk.CTkButton(self, corner_radius=8,
                                        text='Extract colors from image',
                                        command=self.generate_palette).pack(expand=True, fill='x', padx=10)
        self.frame = ctk.CTkFrame(self, fg_color='transparent')


    def generate_palette(self):
        """
        Extract the top 14 most frequent colors from the open image.
        """
        colors = colorgram.extract(self.image.filename, 2**32)
        colors = sorted(colors, key=lambda color: color.proportion)[:14]
        self.hex_colors = [HEX.rgb_to_hex(color.rgb.r, color.rgb.g, color.rgb.b) for color in colors]
        self.draw_colors()

    def draw_colors(self):
        """
        Display extracted colors on the panel.
        """
        self.frame.grid_forget()
        self.frame.pack(expand=True, fill='both', pady=10, padx=5)

        row, col = 0, 0
        for color in self.hex_colors:
            ctk.CTkButton(self.frame, corner_radius=14, width=125, height=18,
                          text=str(color),
                          fg_color=color,
                          text_color=WHITE,
                          hover_color=HEX.colorscale(color, 0.5)).grid(row=row, column=col, padx=5, pady=2)

            col += 1
            if col > 1: col, row = 0, row + 1


class RevertButton(ctk.CTkButton):
    """
    Button used to revert (undo) all effects used in its frame.
    """
    def __init__(self, parent: ctk.CTkFrame, *args) -> None:
        super().__init__(master=parent, text='Revert', command=self.reset_vars)
        self.pack(side='bottom', pady=10)
        self.button_args = args

    def reset_vars(self):
        """
        Reset the values of all provided variables to defaults.
        """
        for tk_var, default_val in self.button_args:
            tk_var.set(default_val)


class ExportButton(ctk.CTkButton):
    """
    Button used to trigger the export image functionality.
    """
    def __init__(self, parent: ctk.CTkFrame,
                 export_func: Callable, filename: ctk.StringVar,
                 extension: ctk.StringVar, path: ctk.StringVar,
                 quality: ctk.IntVar) -> None:
        super().__init__(master=parent, text='Export', command=self.save)

        self.export_func = export_func
        self.filename = filename
        self.extension = extension
        self.path = path
        self.image_quality = quality

        self.pack(side='bottom', pady=10)

    def save(self) -> None:
        """
        Call the export function and provide the full file name and output path.
        """
        self.export_func(
            self.filename.get(), self.extension.get(), self.path.get(),
            int(self.image_quality.get())
        )
