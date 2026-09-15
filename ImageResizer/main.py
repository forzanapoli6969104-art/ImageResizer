
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os


# ============================================================
# PRESETS
# ============================================================

PRESETS = {
    "4K — 3840 × 2160": (3840, 2160),
    "1440p — 2560 × 1440": (2560, 1440),
    "Full HD — 1920 × 1080": (1920, 1080),
    "HD — 1280 × 720": (1280, 720),
    "1024 × 768": (1024, 768),
    "800 × 600": (800, 600),
    "640 × 480": (640, 480),
}


# ============================================================
# VARIABLES
# ============================================================

image = None
image_path = None
preview_image = None

updating_dimensions = False


# ============================================================
# WINDOW
# ============================================================

window = tk.Tk()

window.title("ImageResizer")

# Initial size
window.geometry("900x800")

# Make the window resizable
window.resizable(True, True)

# Minimum size
window.minsize(750, 650)


# ============================================================
# TKINTER VARIABLES
# ============================================================

resize_mode = tk.StringVar(
    master=window,
    value="Pixel"
)

selected_preset = tk.StringVar(
    master=window,
    value="Full HD — 1920 × 1080"
)

width_var = tk.StringVar(
    master=window
)

height_var = tk.StringVar(
    master=window
)

percentage_var = tk.StringVar(
    master=window,
    value="50"
)

direction_var = tk.StringVar(
    master=window,
    value="Smaller"
)

keep_aspect_ratio = tk.BooleanVar(
    master=window,
    value=True
)

format_var = tk.StringVar(
    master=window,
    value="PNG"
)


# ============================================================
# PREVIEW
# ============================================================

def update_preview():

    global preview_image

    if image is None:

        preview_label.config(
            image="",
            text="No image"
        )

        return

    try:

        preview = image.copy()

        # Current preview area size
        preview_width = max(
            preview_area.winfo_width() - 20,
            200
        )

        preview_height = max(
            preview_area.winfo_height() - 20,
            150
        )

        original_width, original_height = (
            preview.size
        )

        # Calculate the scaling factor
        width_factor = (
            preview_width / original_width
        )

        height_factor = (
            preview_height / original_height
        )

        factor = min(
            width_factor,
            height_factor
        )

        # Do not enlarge already small images
        factor = min(
            factor,
            1
        )

        new_width = max(
            1,
            round(
                original_width * factor
            )
        )

        new_height = max(
            1,
            round(
                original_height * factor
            )
        )

        preview = preview.resize(
            (
                new_width,
                new_height
            ),
            Image.Resampling.LANCZOS
        )

        preview_image = ImageTk.PhotoImage(
            preview
        )

        preview_label.config(
            image=preview_image,
            text=""
        )

    except Exception as error:

        preview_label.config(
            image="",
            text=f"Preview error: {error}"
        )


# ============================================================
# WHEN THE WINDOW IS RESIZED
# ============================================================

def preview_resize(event=None):

    if image is not None:
        update_preview()


# ============================================================
# SELECT IMAGE
# ============================================================

def select_image():

    global image
    global image_path

    path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[
            (
                "Images",
                "*.png *.jpg *.jpeg *.webp *.bmp"
            ),
            (
                "All files",
                "*.*"
            )
        ]
    )

    if not path:
        return

    try:

        new_image = Image.open(
            path
        )

        new_image.load()

        image = new_image
        image_path = path

        name = os.path.basename(
            path
        )

        width, height = (
            image.size
        )

        name_label.config(
            text=f"Image: {name}"
        )

        dimensions_label.config(
            text=(
                f"Original dimensions: "
                f"{width} × {height} px"
            )
        )

        # Start with the original dimensions
        width_var.set(
            str(width)
        )

        height_var.set(
            str(height)
        )

        update_preview()
        update_text_preview()

    except Exception as error:

        messagebox.showerror(
            "Error",
            (
                "The image could not be opened.\n\n"
                f"{error}"
            )
        )


# ============================================================
# CHANGE RESIZE MODE
# ============================================================

def change_resize_mode(event=None):

    if resize_mode.get() == "Pixel":

        pixel_frame.pack(
            fill="x",
            padx=35,
            pady=8
        )

        percentage_frame.pack_forget()

    else:

        pixel_frame.pack_forget()

        percentage_frame.pack(
            fill="x",
            padx=35,
            pady=8
        )

    update_text_preview()


# ============================================================
# PRESETS
# ============================================================

def preset_changed(event=None):

    if selected_preset.get() not in PRESETS:
        return

    width, height = PRESETS[
        selected_preset.get()
    ]

    width_var.set(
        str(width)
    )

    height_var.set(
        str(height)
    )

    update_text_preview()


# ============================================================
# MODIFY WIDTH
# ============================================================

def modify_width(event=None):

    global updating_dimensions

    if updating_dimensions:
        return

    if not keep_aspect_ratio.get():
        update_text_preview()
        return

    if image is None:
        return

    try:

        new_width = int(
            width_var.get()
        )

        if new_width <= 0:
            return

        original_width, original_height = (
            image.size
        )

        new_height = round(
            new_width
            * original_height
            / original_width
        )

        updating_dimensions = True

        height_var.set(
            str(new_height)
        )

        updating_dimensions = False

    except (
        ValueError,
        ZeroDivisionError
    ):

        updating_dimensions = False

    update_text_preview()


# ============================================================
# MODIFY HEIGHT
# ============================================================

def modify_height(event=None):

    global updating_dimensions

    if updating_dimensions:
        return

    if not keep_aspect_ratio.get():
        update_text_preview()
        return

    if image is None:
        return

    try:

        new_height = int(
            height_var.get()
        )

        if new_height <= 0:
            return

        original_width, original_height = (
            image.size
        )

        new_width = round(
            new_height
            * original_width
            / original_height
        )

        updating_dimensions = True

        width_var.set(
            str(new_width)
        )

        updating_dimensions = False

    except (
        ValueError,
        ZeroDivisionError
    ):

        updating_dimensions = False

    update_text_preview()


# ============================================================
# ASPECT RATIO CHECKBOX
# ============================================================

def aspect_ratio_changed():

    update_text_preview()


# ============================================================
# CALCULATE DIMENSIONS
# ============================================================

def calculate_dimensions():

    if image is None:

        raise ValueError(
            "You must select an image first."
        )

    original_width, original_height = (
        image.size
    )

    # ========================================================
    # PIXELS
    # ========================================================

    if resize_mode.get() == "Pixel":

        try:

            width = int(
                width_var.get()
            )

            height = int(
                height_var.get()
            )

        except ValueError:

            raise ValueError(
                "Enter valid dimensions."
            )

        if width <= 0 or height <= 0:

            raise ValueError(
                "Dimensions must be greater than 0."
            )

        return width, height

    # ========================================================
    # PERCENTAGE
    # ========================================================

    try:

        percentage = float(
            percentage_var.get()
        )

    except ValueError:

        raise ValueError(
            "Enter a valid percentage."
        )

    if percentage <= 0:

        raise ValueError(
            "The percentage must be greater than 0."
        )

    if direction_var.get() == "Smaller":

        factor = 1 - (
            percentage / 100
        )

    else:

        factor = 1 + (
            percentage / 100
        )

    if factor <= 0:

        raise ValueError(
            "The percentage is not valid."
        )

    new_width = round(
        original_width * factor
    )

    new_height = round(
        original_height * factor
    )

    return new_width, new_height


# ============================================================
# TEXT PREVIEW
# ============================================================

def update_text_preview(event=None):

    if image is None:

        result_label.config(
            text="No image selected"
        )

        return

    try:

        width, height = (
            calculate_dimensions()
        )

        result_label.config(
            text=(
                f"Final size: "
                f"{width} × {height} px"
            )
        )

    except Exception:

        result_label.config(
            text="Invalid dimensions"
        )


# ============================================================
# RESIZE AND SAVE
# ============================================================

def resize_and_save():

    if image is None:

        messagebox.showwarning(
            "No image",
            "Please select an image first."
        )

        return

    try:

        new_width, new_height = (
            calculate_dimensions()
        )

        # The original image is NOT modified
        new_image = image.resize(
            (
                new_width,
                new_height
            ),
            Image.Resampling.LANCZOS
        )

        # ====================================================
        # FORMAT
        # ====================================================

        image_format = format_var.get()

        if image_format == "PNG":

            pillow_format = "PNG"
            extension = ".png"

        elif image_format == "JPEG":

            pillow_format = "JPEG"
            extension = ".jpg"

        elif image_format == "WEBP":

            pillow_format = "WEBP"
            extension = ".webp"

        else:

            raise ValueError(
                "Invalid format."
            )

        # ====================================================
        # NAME
        # ====================================================

        original_name = os.path.splitext(
            os.path.basename(
                image_path
            )
        )[0]

        default_name = (
            f"{original_name}_"
            f"{new_width}x"
            f"{new_height}"
            f"{extension}"
        )

        save_path = (
            filedialog.asksaveasfilename(
                title="Save image",
                initialfile=default_name,
                defaultextension=extension,
                filetypes=[
                    (
                        "PNG",
                        "*.png"
                    ),
                    (
                        "JPEG",
                        "*.jpg"
                    ),
                    (
                        "WEBP",
                        "*.webp"
                    )
                ]
            )
        )

        if not save_path:
            return

        # JPEG does not support transparency
        if (
            pillow_format == "JPEG"
            and new_image.mode
            in ("RGBA", "LA", "P")
        ):

            new_image = (
                new_image.convert("RGB")
            )

        new_image.save(
            save_path,
            format=pillow_format
        )

        messagebox.showinfo(
            "Operation completed",
            (
                "Image saved successfully!\n\n"
                f"Format: {image_format}\n"
                f"Dimensions: "
                f"{new_width} × "
                f"{new_height} px"
            )
        )

    except ValueError as error:

        messagebox.showerror(
            "Error",
            str(error)
        )

    except Exception as error:

        messagebox.showerror(
            "Error",
            (
                "An error occurred:\n\n"
                f"{error}"
            )
        )


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    window,
    text="ImageResizer",
    font=("Segoe UI", 24, "bold")
)

title_label.pack(
    pady=(15, 2)
)


subtitle_label = tk.Label(
    window,
    text="Resize your images easily",
    font=("Segoe UI", 10)
)

subtitle_label.pack(
    pady=(0, 8)
)


# ============================================================
# PREVIEW FRAME
# ============================================================

preview_frame = ttk.LabelFrame(
    window,
    text="Preview"
)

preview_frame.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=8
)


# Preview area
preview_area = tk.Frame(
    preview_frame,
    bg="#202020"
)

preview_area.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


preview_label = tk.Label(
    preview_area,
    text="No image",
    bg="#202020",
    fg="white",
    font=("Segoe UI", 11)
)

preview_label.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# Update preview when resizing the window
preview_area.bind(
    "<Configure>",
    preview_resize
)


# ============================================================
# IMAGE SELECTION
# ============================================================

select_button = ttk.Button(
    window,
    text="📁  Select image",
    command=select_image
)

select_button.pack(
    pady=5
)


name_label = tk.Label(
    window,
    text="No image selected",
    font=("Segoe UI", 10)
)

name_label.pack(
    pady=(3, 0)
)


dimensions_label = tk.Label(
    window,
    text="",
    font=("Segoe UI", 10)
)

dimensions_label.pack()


# ============================================================
# RESIZE MODE
# ============================================================

mode_frame = ttk.LabelFrame(
    window,
    text="Resize"
)

mode_frame.pack(
    fill="x",
    padx=35,
    pady=8
)


mode_menu = ttk.Combobox(
    mode_frame,
    textvariable=resize_mode,
    values=[
        "Pixel",
        "Percentage"
    ],
    state="readonly",
    width=20
)

mode_menu.pack(
    padx=10,
    pady=7
)

mode_menu.bind(
    "<<ComboboxSelected>>",
    change_resize_mode
)


# ============================================================
# PIXELS
# ============================================================

pixel_frame = ttk.Frame(
    window
)


preset_label = tk.Label(
    pixel_frame,
    text="Preset:"
)

preset_label.grid(
    row=0,
    column=0,
    padx=5,
    pady=3,
    sticky="w"
)


preset_menu = ttk.Combobox(
    pixel_frame,
    textvariable=selected_preset,
    values=list(PRESETS.keys()),
    state="readonly",
    width=27
)

preset_menu.grid(
    row=0,
    column=1,
    padx=5,
    pady=3
)

preset_menu.bind(
    "<<ComboboxSelected>>",
    preset_changed
)


width_label = tk.Label(
    pixel_frame,
    text="Width:"
)

width_label.grid(
    row=1,
    column=0,
    padx=5,
    pady=3,
    sticky="w"
)


width_entry = ttk.Entry(
    pixel_frame,
    textvariable=width_var,
    width=15
)

width_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=3,
    sticky="w"
)


height_label = tk.Label(
    pixel_frame,
    text="Height:"
)

height_label.grid(
    row=2,
    column=0,
    padx=5,
    pady=3,
    sticky="w"
)


height_entry = ttk.Entry(
    pixel_frame,
    textvariable=height_var,
    width=15
)

height_entry.grid(
    row=2,
    column=1,
    padx=5,
    pady=3,
    sticky="w"
)


aspect_ratio_check = ttk.Checkbutton(
    pixel_frame,
    text="Keep aspect ratio",
    variable=keep_aspect_ratio,
    command=aspect_ratio_changed
)

aspect_ratio_check.grid(
    row=3,
    column=0,
    columnspan=2,
    padx=5,
    pady=3,
    sticky="w"
)


# Update while editing
width_entry.bind(
    "<KeyRelease>",
    modify_width
)

height_entry.bind(
    "<KeyRelease>",
    modify_height
)


# ============================================================
# PERCENTAGE
# ============================================================

percentage_frame = ttk.Frame(
    window
)


direction_label = tk.Label(
    percentage_frame,
    text="Resize:"
)

direction_label.grid(
    row=0,
    column=0,
    padx=5,
    pady=3,
    sticky="w"
)


direction_menu = ttk.Combobox(
    percentage_frame,
    textvariable=direction_var,
    values=[
        "Smaller",
        "Larger"
    ],
    state="readonly",
    width=18
)

direction_menu.grid(
    row=0,
    column=1,
    padx=5,
    pady=3
)

direction_menu.bind(
    "<<ComboboxSelected>>",
    update_text_preview
)


percentage_label = tk.Label(
    percentage_frame,
    text="Percentage:"
)

percentage_label.grid(
    row=1,
    column=0,
    padx=5,
    pady=3,
    sticky="w"
)


percentage_entry = ttk.Entry(
    percentage_frame,
    textvariable=percentage_var,
    width=15
)

percentage_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=3
)

percentage_entry.bind(
    "<KeyRelease>",
    update_text_preview
)


# ============================================================
# OUTPUT FORMAT
# ============================================================

format_frame = ttk.LabelFrame(
    window,
    text="Output format"
)

format_frame.pack(
    fill="x",
    padx=35,
    pady=8
)


format_menu = ttk.Combobox(
    format_frame,
    textvariable=format_var,
    values=[
        "PNG",
        "JPEG",
        "WEBP"
    ],
    state="readonly",
    width=15
)

format_menu.pack(
    padx=10,
    pady=6
)


# ============================================================
# RESULT
# ============================================================

result_label = tk.Label(
    window,
    text="No image selected",
    font=("Segoe UI", 11, "bold")
)

result_label.pack(
    pady=5
)


# ============================================================
# BUTTON
# ============================================================

resize_button = ttk.Button(
    window,
    text="🔄  RESIZE AND SAVE",
    command=resize_and_save
)

resize_button.pack(
    ipadx=15,
    ipady=7,
    pady=(2, 10)
)


# ============================================================
# START
# ============================================================

change_resize_mode()

window.mainloop()

