
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os


# ============================================================
# PRESET
# ============================================================

PRESET = {
    "4K — 3840 × 2160": (3840, 2160),
    "1440p — 2560 × 1440": (2560, 1440),
    "Full HD — 1920 × 1080": (1920, 1080),
    "HD — 1280 × 720": (1280, 720),
    "1024 × 768": (1024, 768),
    "800 × 600": (800, 600),
    "640 × 480": (640, 480),
}


# ============================================================
# VARIABILI
# ============================================================

immagine = None
percorso_immagine = None
preview_image = None

aggiornamento_dimensioni = False


# ============================================================
# FINESTRA
# ============================================================

finestra = tk.Tk()

finestra.title("ImageResizer")

# Dimensione iniziale
finestra.geometry("900x800")

# ORA LA FINESTRA È RIDIMENSIONABILE
finestra.resizable(True, True)

# Dimensione minima
finestra.minsize(750, 650)


# ============================================================
# VARIABILI TKINTER
# ============================================================

modalita = tk.StringVar(
    master=finestra,
    value="Pixel"
)

preset_selezionato = tk.StringVar(
    master=finestra,
    value="Full HD — 1920 × 1080"
)

larghezza_var = tk.StringVar(
    master=finestra
)

altezza_var = tk.StringVar(
    master=finestra
)

percentuale_var = tk.StringVar(
    master=finestra,
    value="50"
)

direzione_var = tk.StringVar(
    master=finestra,
    value="Più piccola"
)

mantieni_proporzioni = tk.BooleanVar(
    master=finestra,
    value=True
)

formato_var = tk.StringVar(
    master=finestra,
    value="PNG"
)


# ============================================================
# PREVIEW
# ============================================================

def aggiorna_preview():

    global preview_image

    if immagine is None:

        preview_label.config(
            image="",
            text="Nessuna immagine"
        )

        return

    try:

        anteprima = immagine.copy()

        # Dimensione attuale dell'area preview
        larghezza_area = max(
            preview_area.winfo_width() - 20,
            200
        )

        altezza_area = max(
            preview_area.winfo_height() - 20,
            150
        )

        larghezza_originale, altezza_originale = (
            anteprima.size
        )

        # Calcolo del rapporto di riduzione
        fattore_larghezza = (
            larghezza_area / larghezza_originale
        )

        fattore_altezza = (
            altezza_area / altezza_originale
        )

        fattore = min(
            fattore_larghezza,
            fattore_altezza
        )

        # Non ingrandire immagini già piccole
        fattore = min(
            fattore,
            1
        )

        nuova_larghezza = max(
            1,
            round(
                larghezza_originale * fattore
            )
        )

        nuova_altezza = max(
            1,
            round(
                altezza_originale * fattore
            )
        )

        anteprima = anteprima.resize(
            (
                nuova_larghezza,
                nuova_altezza
            ),
            Image.Resampling.LANCZOS
        )

        preview_image = ImageTk.PhotoImage(
            anteprima
        )

        preview_label.config(
            image=preview_image,
            text=""
        )

    except Exception as errore:

        preview_label.config(
            image="",
            text=f"Errore preview: {errore}"
        )


# ============================================================
# QUANDO CAMBIA LA DIMENSIONE DELLA FINESTRA
# ============================================================

def preview_resize(event=None):

    if immagine is not None:
        aggiorna_preview()


# ============================================================
# SELEZIONA IMMAGINE
# ============================================================

def scegli_immagine():

    global immagine
    global percorso_immagine

    percorso = filedialog.askopenfilename(
        title="Seleziona un'immagine",
        filetypes=[
            (
                "Immagini",
                "*.png *.jpg *.jpeg *.webp *.bmp"
            ),
            (
                "Tutti i file",
                "*.*"
            )
        ]
    )

    if not percorso:
        return

    try:

        nuova_immagine = Image.open(
            percorso
        )

        nuova_immagine.load()

        immagine = nuova_immagine
        percorso_immagine = percorso

        nome = os.path.basename(
            percorso
        )

        larghezza, altezza = (
            immagine.size
        )

        nome_label.config(
            text=f"Immagine: {nome}"
        )

        dimensioni_label.config(
            text=(
                f"Dimensioni originali: "
                f"{larghezza} × {altezza} px"
            )
        )

        # Partiamo dalle dimensioni originali
        larghezza_var.set(
            str(larghezza)
        )

        altezza_var.set(
            str(altezza)
        )

        aggiorna_preview()
        aggiorna_preview_testuale()

    except Exception as errore:

        messagebox.showerror(
            "Errore",
            (
                "Non è stato possibile aprire "
                "l'immagine.\n\n"
                f"{errore}"
            )
        )


# ============================================================
# CAMBIA MODALITÀ
# ============================================================

def cambia_modalita(event=None):

    if modalita.get() == "Pixel":

        frame_pixel.pack(
            fill="x",
            padx=35,
            pady=8
        )

        frame_percentuale.pack_forget()

    else:

        frame_pixel.pack_forget()

        frame_percentuale.pack(
            fill="x",
            padx=35,
            pady=8
        )

    aggiorna_preview_testuale()


# ============================================================
# PRESET
# ============================================================

def preset_cambiato(event=None):

    if preset_selezionato.get() not in PRESET:
        return

    larghezza, altezza = PRESET[
        preset_selezionato.get()
    ]

    larghezza_var.set(
        str(larghezza)
    )

    altezza_var.set(
        str(altezza)
    )

    aggiorna_preview_testuale()


# ============================================================
# MODIFICA LARGHEZZA
# ============================================================

def modifica_larghezza(event=None):

    global aggiornamento_dimensioni

    if aggiornamento_dimensioni:
        return

    if not mantieni_proporzioni.get():
        aggiorna_preview_testuale()
        return

    if immagine is None:
        return

    try:

        nuova_larghezza = int(
            larghezza_var.get()
        )

        if nuova_larghezza <= 0:
            return

        larghezza_originale, altezza_originale = (
            immagine.size
        )

        nuova_altezza = round(
            nuova_larghezza
            * altezza_originale
            / larghezza_originale
        )

        aggiornamento_dimensioni = True

        altezza_var.set(
            str(nuova_altezza)
        )

        aggiornamento_dimensioni = False

    except (
        ValueError,
        ZeroDivisionError
    ):

        aggiornamento_dimensioni = False

    aggiorna_preview_testuale()


# ============================================================
# MODIFICA ALTEZZA
# ============================================================

def modifica_altezza(event=None):

    global aggiornamento_dimensioni

    if aggiornamento_dimensioni:
        return

    if not mantieni_proporzioni.get():
        aggiorna_preview_testuale()
        return

    if immagine is None:
        return

    try:

        nuova_altezza = int(
            altezza_var.get()
        )

        if nuova_altezza <= 0:
            return

        larghezza_originale, altezza_originale = (
            immagine.size
        )

        nuova_larghezza = round(
            nuova_altezza
            * larghezza_originale
            / altezza_originale
        )

        aggiornamento_dimensioni = True

        larghezza_var.set(
            str(nuova_larghezza)
        )

        aggiornamento_dimensioni = False

    except (
        ValueError,
        ZeroDivisionError
    ):

        aggiornamento_dimensioni = False

    aggiorna_preview_testuale()


# ============================================================
# CAMBIO CHECKBOX
# ============================================================

def cambio_proporzioni():

    aggiorna_preview_testuale()


# ============================================================
# CALCOLA DIMENSIONI
# ============================================================

def calcola_dimensioni():

    if immagine is None:

        raise ValueError(
            "Prima devi selezionare un'immagine."
        )

    larghezza_originale, altezza_originale = (
        immagine.size
    )

    # ========================================================
    # PIXEL
    # ========================================================

    if modalita.get() == "Pixel":

        try:

            larghezza = int(
                larghezza_var.get()
            )

            altezza = int(
                altezza_var.get()
            )

        except ValueError:

            raise ValueError(
                "Inserisci dimensioni valide."
            )

        if larghezza <= 0 or altezza <= 0:

            raise ValueError(
                "Le dimensioni devono essere maggiori di 0."
            )

        return larghezza, altezza

    # ========================================================
    # PERCENTUALE
    # ========================================================

    try:

        percentuale = float(
            percentuale_var.get()
        )

    except ValueError:

        raise ValueError(
            "Inserisci una percentuale valida."
        )

    if percentuale <= 0:

        raise ValueError(
            "La percentuale deve essere maggiore di 0."
        )

    if direzione_var.get() == "Più piccola":

        fattore = 1 - (
            percentuale / 100
        )

    else:

        fattore = 1 + (
            percentuale / 100
        )

    if fattore <= 0:

        raise ValueError(
            "La percentuale non è valida."
        )

    nuova_larghezza = round(
        larghezza_originale * fattore
    )

    nuova_altezza = round(
        altezza_originale * fattore
    )

    return nuova_larghezza, nuova_altezza


# ============================================================
# PREVIEW TESTUALE
# ============================================================

def aggiorna_preview_testuale(event=None):

    if immagine is None:

        risultato_label.config(
            text="Nessuna immagine selezionata"
        )

        return

    try:

        larghezza, altezza = (
            calcola_dimensioni()
        )

        risultato_label.config(
            text=(
                f"Dimensione finale: "
                f"{larghezza} × {altezza} px"
            )
        )

    except Exception:

        risultato_label.config(
            text="Dimensioni non valide"
        )


# ============================================================
# RIDIMENSIONA E SALVA
# ============================================================

def ridimensiona():

    if immagine is None:

        messagebox.showwarning(
            "Nessuna immagine",
            "Prima seleziona un'immagine."
        )

        return

    try:

        nuova_larghezza, nuova_altezza = (
            calcola_dimensioni()
        )

        # L'originale NON viene modificata
        nuova_immagine = immagine.resize(
            (
                nuova_larghezza,
                nuova_altezza
            ),
            Image.Resampling.LANCZOS
        )

        # ====================================================
        # FORMATO
        # ====================================================

        formato = formato_var.get()

        if formato == "PNG":

            formato_pillow = "PNG"
            estensione = ".png"

        elif formato == "JPEG":

            formato_pillow = "JPEG"
            estensione = ".jpg"

        elif formato == "WEBP":

            formato_pillow = "WEBP"
            estensione = ".webp"

        else:

            raise ValueError(
                "Formato non valido."
            )

        # ====================================================
        # NOME
        # ====================================================

        nome_originale = os.path.splitext(
            os.path.basename(
                percorso_immagine
            )
        )[0]

        nome_default = (
            f"{nome_originale}_"
            f"{nuova_larghezza}x"
            f"{nuova_altezza}"
            f"{estensione}"
        )

        percorso_salvataggio = (
            filedialog.asksaveasfilename(
                title="Salva immagine",
                initialfile=nome_default,
                defaultextension=estensione,
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

        if not percorso_salvataggio:
            return

        # JPEG non supporta trasparenza
        if (
            formato_pillow == "JPEG"
            and nuova_immagine.mode
            in ("RGBA", "LA", "P")
        ):

            nuova_immagine = (
                nuova_immagine.convert("RGB")
            )

        nuova_immagine.save(
            percorso_salvataggio,
            format=formato_pillow
        )

        messagebox.showinfo(
            "Operazione completata",
            (
                "Immagine salvata correttamente!\n\n"
                f"Formato: {formato}\n"
                f"Dimensioni: "
                f"{nuova_larghezza} × "
                f"{nuova_altezza} px"
            )
        )

    except ValueError as errore:

        messagebox.showerror(
            "Errore",
            str(errore)
        )

    except Exception as errore:

        messagebox.showerror(
            "Errore",
            (
                "Si è verificato un errore:\n\n"
                f"{errore}"
            )
        )


# ============================================================
# TITOLO
# ============================================================

titolo = tk.Label(
    finestra,
    text="ImageResizer",
    font=("Segoe UI", 24, "bold")
)

titolo.pack(
    pady=(15, 2)
)


sottotitolo = tk.Label(
    finestra,
    text="Ridimensiona le tue immagini facilmente",
    font=("Segoe UI", 10)
)

sottotitolo.pack(
    pady=(0, 8)
)


# ============================================================
# PREVIEW FRAME
# ============================================================

preview_frame = ttk.LabelFrame(
    finestra,
    text="Anteprima"
)

preview_frame.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=8
)


# Area preview
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
    text="Nessuna immagine",
    bg="#202020",
    fg="white",
    font=("Segoe UI", 11)
)

preview_label.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# Aggiorna la preview quando ridimensioniamo la finestra
preview_area.bind(
    "<Configure>",
    preview_resize
)


# ============================================================
# SELEZIONE IMMAGINE
# ============================================================

seleziona_button = ttk.Button(
    finestra,
    text="📁  Seleziona immagine",
    command=scegli_immagine
)

seleziona_button.pack(
    pady=5
)


nome_label = tk.Label(
    finestra,
    text="Nessuna immagine selezionata",
    font=("Segoe UI", 10)
)

nome_label.pack(
    pady=(3, 0)
)


dimensioni_label = tk.Label(
    finestra,
    text="",
    font=("Segoe UI", 10)
)

dimensioni_label.pack()


# ============================================================
# MODALITÀ
# ============================================================

frame_modalita = ttk.LabelFrame(
    finestra,
    text="Ridimensionamento"
)

frame_modalita.pack(
    fill="x",
    padx=35,
    pady=8
)


modalita_menu = ttk.Combobox(
    frame_modalita,
    textvariable=modalita,
    values=[
        "Pixel",
        "Percentuale"
    ],
    state="readonly",
    width=20
)

modalita_menu.pack(
    padx=10,
    pady=7
)

modalita_menu.bind(
    "<<ComboboxSelected>>",
    cambia_modalita
)


# ============================================================
# PIXEL
# ============================================================

frame_pixel = ttk.Frame(
    finestra
)


preset_label = tk.Label(
    frame_pixel,
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
    frame_pixel,
    textvariable=preset_selezionato,
    values=list(PRESET.keys()),
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
    preset_cambiato
)


larghezza_label = tk.Label(
    frame_pixel,
    text="Larghezza:"
)

larghezza_label.grid(
    row=1,
    column=0,
    padx=5,
    pady=3,
    sticky="w"
)


larghezza_entry = ttk.Entry(
    frame_pixel,
    textvariable=larghezza_var,
    width=15
)

larghezza_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=3,
    sticky="w"
)


altezza_label = tk.Label(
    frame_pixel,
    text="Altezza:"
)

altezza_label.grid(
    row=2,
    column=0,
    padx=5,
    pady=3,
    sticky="w"
)


altezza_entry = ttk.Entry(
    frame_pixel,
    textvariable=altezza_var,
    width=15
)

altezza_entry.grid(
    row=2,
    column=1,
    padx=5,
    pady=3,
    sticky="w"
)


proporzioni_check = ttk.Checkbutton(
    frame_pixel,
    text="Mantieni proporzioni",
    variable=mantieni_proporzioni,
    command=cambio_proporzioni
)

proporzioni_check.grid(
    row=3,
    column=0,
    columnspan=2,
    padx=5,
    pady=3,
    sticky="w"
)


# Aggiornamento quando si finisce di modificare
larghezza_entry.bind(
    "<KeyRelease>",
    modifica_larghezza
)

altezza_entry.bind(
    "<KeyRelease>",
    modifica_altezza
)


# ============================================================
# PERCENTUALE
# ============================================================

frame_percentuale = ttk.Frame(
    finestra
)


direzione_label = tk.Label(
    frame_percentuale,
    text="Ridimensiona:"
)

direzione_label.grid(
    row=0,
    column=0,
    padx=5,
    pady=3,
    sticky="w"
)


direzione_menu = ttk.Combobox(
    frame_percentuale,
    textvariable=direzione_var,
    values=[
        "Più piccola",
        "Più grande"
    ],
    state="readonly",
    width=18
)

direzione_menu.grid(
    row=0,
    column=1,
    padx=5,
    pady=3
)

direzione_menu.bind(
    "<<ComboboxSelected>>",
    aggiorna_preview_testuale
)


percentuale_label = tk.Label(
    frame_percentuale,
    text="Percentuale:"
)

percentuale_label.grid(
    row=1,
    column=0,
    padx=5,
    pady=3,
    sticky="w"
)


percentuale_entry = ttk.Entry(
    frame_percentuale,
    textvariable=percentuale_var,
    width=15
)

percentuale_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=3
)

percentuale_entry.bind(
    "<KeyRelease>",
    aggiorna_preview_testuale
)


# ============================================================
# FORMATO
# ============================================================

frame_formato = ttk.LabelFrame(
    finestra,
    text="Formato di output"
)

frame_formato.pack(
    fill="x",
    padx=35,
    pady=8
)


formato_menu = ttk.Combobox(
    frame_formato,
    textvariable=formato_var,
    values=[
        "PNG",
        "JPEG",
        "WEBP"
    ],
    state="readonly",
    width=15
)

formato_menu.pack(
    padx=10,
    pady=6
)


# ============================================================
# RISULTATO
# ============================================================

risultato_label = tk.Label(
    finestra,
    text="Nessuna immagine selezionata",
    font=("Segoe UI", 11, "bold")
)

risultato_label.pack(
    pady=5
)


# ============================================================
# PULSANTE
# ============================================================

ridimensiona_button = ttk.Button(
    finestra,
    text="🔄  RIDIMENSIONA E SALVA",
    command=ridimensiona
)

ridimensiona_button.pack(
    ipadx=15,
    ipady=7,
    pady=(2, 10)
)


# ============================================================
# AVVIO
# ============================================================

cambia_modalita()

finestra.mainloop()
