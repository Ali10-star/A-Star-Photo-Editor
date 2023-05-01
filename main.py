import customtkinter as ctk
from tkinter import messagebox, Event
from PIL import Image, ImageTk, ImageOps
# App-specific imports
from image_widgets import ImageImport, ImageOutput, CloseOutputButton
from image_tools.manipulator import ImageManipulator
from menu import Menu
from settings import *

class App(ctk.CTk):
    """
    Main application UI and functionality. Instance of CTK Main Window.
    """
    def __init__(self) -> None:
        # Setup
        super().__init__()

        self.image: Image.Image = None
        self.tk_image: ImageTk = None
        self.image_import: ImageImport | None = None
        self.image_output: ImageOutput | None = None

        ctk.set_appearance_mode('System')
        ctk.set_default_color_theme('theme/custom.json')
        self.geometry('1250x660+50+50')
        self.title('A-Star Photo Editor')
        self.iconbitmap('theme/logo.ico')
        self.init_parameters()

        # Layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

        # Canvas data
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        # Widgets
        self.image_import = ImageImport(parent=self, import_func=self.import_image)

        self.mainloop()


    def init_parameters(self) -> None:
        """
        Initialize menu parameters used for various effects.
        """
        self.selected_theme = ctk.StringVar(value='System')

        self.position_vars = {
            'rotate': ctk.DoubleVar(value=ROTATE_DEFAULT),
            'zoom': ctk.DoubleVar(value=ZOOM_DEFAULT),
            'flip': ctk.StringVar(value=FLIP_OPTIONS[0]),
        }

        self.color_vars = {
            'brightness': ctk.DoubleVar(value=BRIGHTNESS_DEFAULT),
            'grayscale': ctk.BooleanVar(value=GRAYSCALE_DEFAULT),
            'sepia': ctk.BooleanVar(value=SEPIA_DEFAULT),
            'invert': ctk.BooleanVar(value=INVERT_DEFAULT),
            '4-color': ctk.BooleanVar(value=FOUR_COLOR_DEFAULT),
            'vibrance': ctk.DoubleVar(value=VIBRANCE_DEFAULT),
        }

        self.effect_vars = {
            'blur': ctk.DoubleVar(value=BLUR_DEFAULT),
            'contrast': ctk.IntVar(value=CONTRAST_DEFAULT),
            'balance': ctk.IntVar(value=BALANCE_DEFAULT),
            'hue': ctk.IntVar(value=HUE_DEFAULT),
            'effect': ctk.StringVar(value=EFFECT_OPTIONS[0]),
        }

        all_vars = (
            list(self.position_vars.values())
            + list(self.color_vars.values())
            + list(self.effect_vars.values())
        )

        for var in all_vars:
            var.trace('w', self.manipulate_image)


    def import_image(self, path: str) -> None:
        """
        Import image file to the app, then display the image and editing menu.

        Args:
            path (str): path to the image file
        """
        self.original = Image.open(path)   # To revert back to the image
        self.image = self.original
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_import.grid_forget()    # Destroy import button to display editor

        self.image_output = ImageOutput(self, self.resize_image)
        self.close_button = CloseOutputButton(self, close_func=self.close_editor)

        self.editor_menu = Menu(
            self,
            self.position_vars,
            self.color_vars,
            self.effect_vars,
            self.image,
            self.export_image,
            self.save_thumbnail,
        )

    def manipulate_image(self, *args):
        self.image = self.original
        manipulator = ImageManipulator(self.image)

        manipulator.rotate_image(self.position_vars['rotate'].get())

        manipulator.zoom_image(self.position_vars['zoom'].get())

        manipulator.flip_image(self.position_vars['flip'].get())

        manipulator.apply_brightness(self.color_vars['brightness'].get())

        manipulator.apply_vibrance(self.color_vars['vibrance'].get())

        manipulator.apply_grayscale(self.color_vars['grayscale'].get())

        try:
            manipulator.invert_colors(self.color_vars['invert'].get())
        except OSError:
            messagebox.showerror("Invalid operation", "Cannot apply this operation on this type of image.")

        manipulator.apply_sepia(self.color_vars['sepia'].get())

        manipulator.apply_4color_filter(self.color_vars['4-color'].get())

        manipulator.blur_image(self.effect_vars['blur'].get())

        manipulator.change_contrast(self.effect_vars['contrast'].get())

        manipulator.change_balance(self.effect_vars['balance'].get())

        manipulator.change_hue(self.effect_vars['hue'].get())

        manipulator.apply_effect(self.effect_vars['effect'].get())


        self.image = manipulator.image_result
        self.display_image()


    def close_editor(self) -> None:
        """
        Close the editing panel and the open image.
        """
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.editor_menu.grid_forget()
        self.editor_menu.pack_forget()
        self.image_import = ImageImport(parent=self, import_func=self.import_image)


    def resize_image(self, event: Event) -> None:
        """
        Resizes the image relative to the canvas size, adapts with
        when changing the window size.

        Args:
            event (tkinter.Event): Window change event.
        """
        self.canvas_height = event.height
        self.canvas_width = event.width
        canvas_ratio = self.canvas_width / self.canvas_height

        # resize image
        if canvas_ratio > self.image_ratio:   # Canvas is wider than image
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:   # Canvas is taller than image
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)

        self.display_image()


    def display_image(self) -> None:
        """
        Display image on the output canvas.
        """
        self.image_output.delete('all')
        resized_image = self.image.resize(
            (self.image_width, self.image_height)
        )
        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(
            self.canvas_width / 2,
            self.canvas_height / 2,
            image=self.tk_image,
            anchor='center',
        )

    def export_image(self, filename: str, extension: str, output_path: str, quality: int = 100) -> None:
        """
        Save image to the output folder.

        Args:
            filename (str): name of the saved file.
            extension (str): file type extension (jpg, png, ...)
            output_path (str): output folder path.
        """
        export_str = f'{output_path}/{filename}.{extension}'

        OPTIMIZE = True if quality != 100 else False
        IS_JPG = self.image.format and self.image.format.lower() in ('jpg', 'jpeg')
        if quality == 100 and IS_JPG:
            quality = 'keep'

        self.image.save(export_str, quality=quality, optimize=OPTIMIZE)
        messagebox.showinfo(
            title='Done', message='Successfully exported image file.'
        )

    def save_thumbnail(self, name: str, size: tuple[int, int], output_path: str) -> None:
        """
        Save thumbnail to the output folder.

        Args:
            name (str): name of the saved file.
            size tuple(int, int): size of the thumbnail
            output_path (str): output folder path.
        """
        copy = self.image
        if copy.mode == 'P':
            copy = copy.convert('RGB')
        export_str = f'{output_path}/{name}.jpg'
        copy.thumbnail(size)
        copy.save(export_str)
        messagebox.showinfo(title='Done', message="Successfully created thumbnail.")


if __name__ == '__main__':
    App()