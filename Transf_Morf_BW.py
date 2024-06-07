import cv2
import numpy as np
import tkinter as tk
from scipy import ndimage
from tkinter import filedialog
from tkinter import *

def get_control_by_name(frame, name):
    for widget in frame.winfo_children():
        if widget.winfo_name() == name:
            return widget
        elif isinstance(widget, tk.LabelFrame) or isinstance(widget, tk.Frame):
            result = get_control_by_name(widget, name)
            if result is not None:
                return result
    return None

def redim_img(img):
    original_height, original_width = img.shape[:2]
    new_height = 500
    new_width = int((new_height / original_height) * original_width)
    return cv2.resize(img, (new_width, new_height))

def suavizado(img):
    ctrl = get_control_by_name(root, 'scale_suavizado')
    if ctrl is not None:
        val = int(ctrl.get())
        if val > 0:
            val = (val * 2) + 1
            return cv2.GaussianBlur(img, (int(val),int(val)), 0)
    return img

def afilado(img):
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    return cv2.filter2D(img, -1, kernel)

def promedio(img):
    ctrl = get_control_by_name(root, 'scale_promedio')
    if ctrl is not None:
        val = int(ctrl.get())
        if val > 0:
            val = (val * 2) + 1
            return cv2.blur(img, (int(val),int(val)))
    return img
                    
def mediana(img):  
    ctrl = get_control_by_name(root, 'scale_mediana')
    if ctrl is not None:
        val = int(ctrl.get())       
        if val > 0:
            val = (val * 2) + 1
            return cv2.medianBlur(img, (int(val),int(val)))  
    return img
    
def erosion(img):
    ctrl = get_control_by_name(root, 'scale_erosion')
    if ctrl is not None:
        val = int(ctrl.get()) 
        if val > 0:
            val = (val * 2) + 1 
            kernel = np.ones((val, val), np.uint8)
            return cv2.erode(img, kernel, iterations=1)  
    return img
                   

def log(img):
    img = img.astype(float)
    img = np.log1p(img)
    img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return img


def dilatacion(img):
    ctrl = get_control_by_name(root, 'scale_dilatacion')
    if ctrl is not None:
        val = int(ctrl.get()) 
        if val > 0:
            val = (val * 2) + 1 
            kernel = np.ones((val, val), np.uint8)
            return cv2.dilate(img, kernel, iterations=1)   
    return img
    
def apertura(img):
    ero = erosion(img)
    return dilatacion(ero)

def clausura(img):
    dil = dilatacion(img)
    return erosion(dil)
 
def gradiente(img):
    dil = dilatacion(img)
    ero = erosion(img)
    return cv2.subtract(dil, ero)

def whitetophat(img):
    aper = apertura(img)
    return cv2.subtract(img, aper) 

def blacktophat(img):
    clau = clausura(img)
    return cv2.subtract(clau, img) 

def sobel(img):
    global radio_var
    if radio_var.get() == 'opcion0':
        sobel_h = np.array([[ 1,  2,  1],
                            [ 0,  0,  0],
                            [-1, -2, -1]])
        return ndimage.convolve(img, sobel_h)
    elif radio_var.get() == 'opcion90':
        sobel_v = np.array([[1, 0, -1],
                            [2, 0, -2],
                            [1, 0, -1]])
        return ndimage.convolve(img, sobel_v)
    elif radio_var.get() == 'opcion45':
        prewitt_x = np.array([[-1, 0, 1],
                              [-1, 0, 1],
                              [-1, 0, 1]])
        return ndimage.convolve(img, prewitt_x)
    elif radio_var.get() == 'opcion135':
        prewitt_y = np.array([[-1, -1, -1],
                              [ 0,  0,  0],
                              [ 1,  1,  1]])
        return ndimage.convolve(img, prewitt_y) 
    else:
        return img

def laplaciano(img):
    laplaciankernel = np.array([[1, 1, 1],[1, -8, 1],[1, 1, 1]])
    return cv2.filter2D(img, -1, laplaciankernel)

def canny(img):
    ctrl_min = get_control_by_name(root, 'scale_canny_min')
    ctrl_max = get_control_by_name(root, 'scale_canny_max')
    if ctrl_min is not None and ctrl_max is not None:
        val_min = int(ctrl_min.get()) 
        val_max = int(ctrl_max.get()) 
        if val_min > val_max:
            val_min, val_max = val_max, val_min
        img = img.astype(np.uint8)
        return cv2.Canny(img, val_min, val_max)   
    return img  

def sumar(img2):
    global img
    return cv2.add(img, img2)

def restar(img2):
    global img
    return cv2.subtract(img, img2)

def multiplicar(img2):
    global img
    return cv2.multiply(img, img2)

def dividir(img2):
    global img
    sal = cv2.divide(img.astype(float), img2.astype(float))
    return cv2.normalize(sal, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

def negativo(img2):
    return 255 - img2

def final(img1, img2):
    global radio_final
    if radio_final.get() == 'no':
        return img2
    elif radio_final.get() == 'sum':
        return cv2.add(img1, img2)
    elif radio_final.get() == 'sub':
        return cv2.subtract(img1, img2)
    elif radio_final.get() == 'mul':
        return cv2.multiply(img1, img2)
    elif radio_final.get() == 'div':
        return cv2.divide(img1, img2)
    elif radio_final.get() == 'neg':
        return negativo(img2)
                     
def apply_filter(*args):
    global img, img_concat
    if img is not None:
        img2 = img.copy()
        
        for i in range(10):
            texto = combo_vars[i].get()
        
            if texto == 'Suavizado':
                img2 = suavizado(img2)
            elif texto == 'Afilado':
                img2 = afilado(img2)
            elif texto == 'Promedio':
                img2 = promedio(img2)
            elif texto == 'Mediana':
                img2 = mediana(img2)
            elif texto == 'Erosion':
                img2 = erosion(img2)
            elif texto == 'Dilatacion':
                img2 = dilatacion(img2)
            elif texto == 'Apertura':
                img2 = apertura(img2)
            elif texto == 'Clausura':
                img2 = clausura(img2)
            elif texto == 'Gradiente':
                img2 = gradiente(img2)
            elif texto == 'White Top-Hat':
                img2 = whitetophat(img2)
            elif texto == 'Black Top-Hat':
                img2 = blacktophat(img2)
            elif texto == 'Sobel':
                img2 = sobel(img2)
            elif texto == 'Laplaciano':
                img2 = laplaciano(img2)
            elif texto == 'Canny':
                img2 = canny(img2)
            elif texto == 'Sumar':
                img2 = sumar(img2)
            elif texto == 'Restar':
                img2 = restar(img2)
            elif texto == 'Multiplicar':
                img2 = multiplicar(img2)
            elif texto == 'Dividir':
                img2 = dividir(img2)
            elif texto == 'Negativo':
                img2 = negativo(img2)
            elif texto == 'Log':
                img2 = log(img2)
        
        img1 = img.astype(float)
        img2 = img2.astype(float)        
        img3 = final(img1, img2)

        # Normaliza las imágenes a un rango de 0 a 255
        img1 = cv2.normalize(img1, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        img2 = cv2.normalize(img2, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        img3 = cv2.normalize(img3, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        # Redimensiona las imágenes a la mitad de su tamaño original
        res1 = redim_img(img1)
        res2 = redim_img(img2)
        res3 = redim_img(img3)
        res4 = np.zeros_like(res1)
        # Concatena las imágenes en una matriz de 2x2
        img_top = np.concatenate((res1, res2), axis=1)
        img_bottom = np.concatenate((res3, res4), axis=1)
        img_concat = np.concatenate((img_top, img_bottom), axis=0)
        
        # Muestra la imagen concatenada
        cv2.imshow('image', img_concat)

def on_filter_select(*args):
    apply_filter()

def set_widget_state(master, enable):
    # Determina el estado basado en el valor de 'enable'
    state = 'normal' if enable else 'disabled'
    
    for child in master.winfo_children():
        wtype = child.winfo_class()
        if wtype not in ('Frame', 'Labelframe'):
            child.config(state=state)
        else:
            set_widget_state(child, enable)
            
# Función para cargar la imagen
def load_image():
    global img
    file_path = filedialog.askopenfilename()
    # Lee la imagen como un archivo binario
    with open(file_path, 'rb') as f:
        arr = np.asarray(bytearray(f.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    cv2.imshow('image', img)
    
    # Habilita los controles una vez que se ha cargado la imagen
    set_widget_state(frame_controles, True)

def save_image():
    global img_concat
    if img_concat is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, img)
            tk.messagebox.showinfo("Imagen guardada", "La imagen ha sido guardada exitosamente.")
            
def config_controls(root):
    global combo_vars, radio_var, radio_final
    
    # Botón para cargar la imagen
    Button(root, text='Cargar imagen', command=load_image).pack()
    # Botón para guardar la imagen
    Button(root, text='Guardar imagen', command=save_image).pack()

    # Marco de todos los controles
    frame_controles = LabelFrame(root, text="CONTROLES", padx=5, pady=5)
    frame_controles.pack(padx=10, pady=10)

    # PASOS
    frame_filtros = LabelFrame(frame_controles, text="Pasos", padx=5, pady=5)
    frame_filtros.pack(padx=10, pady=10) 
    # Menú desplegable para seleccionar el filtro
    opciones = ['Ninguno', 'Suavizado', 'Afilado', 'Promedio', 'Mediana', 'Erosion', 'Dilatacion',
                'Apertura', 'Clausura', 'Gradiente', 'White Top-Hat', 'Black Top-Hat', 'Sobel', 'Laplaciano', 'Canny',
                'Sumar', 'Restar', 'Multiplicar', 'Dividir', 'Negativo', 'Log']
    combo_vars  = []
    for i in range(10):
        var = StringVar(frame_filtros)
        var.set('Ninguno') # valor inicial
        var.trace_add('write', on_filter_select)
        
        # Etiqueta
        label = Label(frame_filtros, text=f'Filtro {i+1}', anchor='w')
        label.grid(row=2*(i//5), column=i%5, padx=10, pady=0, sticky='nsew')
        
        # Combo
        combo = OptionMenu(frame_filtros, var, *opciones)
        combo.grid(row=2*(i//5)+1, column=i%5, padx=10, pady=0, sticky='nsew') 
        combo_vars.append(var)
    set_widget_state(frame_filtros, False)

    # Marco para controles de parámetros
    frame_col = LabelFrame(frame_controles, padx=5, pady=5)
    frame_col.pack(padx=10, pady=10) 

    # SUAVIZADO
    frame_suavizado = LabelFrame(frame_col, text="Suavizado", padx=5, pady=5)
    frame_suavizado.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
    # Control deslizante 
    scale_suavizado = Scale(frame_suavizado, name='scale_suavizado', from_=0, to=50, orient=HORIZONTAL, length=250, command=apply_filter)
    scale_suavizado.pack(fill='x', expand=True)
    set_widget_state(frame_suavizado, False)

    # PROMEDIO
    frame_promedio = LabelFrame(frame_col, text="Promedio", padx=5, pady=5)
    frame_promedio.grid(row=1, column=0, padx=10, pady=10, sticky='nsew') 
    # Control deslizante
    scale_promedio = Scale(frame_promedio, name='scale_promedio', from_=0, to=50, orient=HORIZONTAL, length=250, command=apply_filter)
    scale_promedio.pack(fill='x', expand=True)
    set_widget_state(frame_promedio, False)

    # MEDIANA
    frame_mediana = LabelFrame(frame_col, text="Mediana", padx=5, pady=5)
    frame_mediana.grid(row=1, column=1, padx=10, pady=10, sticky='nsew') 
    # Control deslizante
    scale_mediana = Scale(frame_mediana, name='scale_mediana', from_=0, to=50, orient=HORIZONTAL, length=250, command=apply_filter)
    scale_mediana.pack(fill='x', expand=True)
    set_widget_state(frame_mediana, False)

    # EROSION
    frame_erosion = LabelFrame(frame_col, text="Erosion", padx=5, pady=5)
    frame_erosion.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')  
    # Control deslizante 
    scale_erosion= Scale(frame_erosion, name='scale_erosion', from_=0, to=50, orient=HORIZONTAL, length=250, command=apply_filter)
    scale_erosion.pack(fill='x', expand=True)
    set_widget_state(frame_erosion, False)

    # DILATACION
    frame_dilatacion = LabelFrame(frame_col, text="Dilatacion", padx=5, pady=5)
    frame_dilatacion.grid(row=2, column=1, padx=10, pady=10, sticky='nsew') 
    # Control deslizante
    scale_dilatacion = Scale(frame_dilatacion, name='scale_dilatacion', from_=0, to=50, orient=HORIZONTAL, length=250, command=apply_filter)
    scale_dilatacion.pack(fill='x', expand=True)
    set_widget_state(frame_dilatacion, False)
    # LOG
    frame_log = LabelFrame(frame_col, text="Log", padx=5, pady=5)
    frame_log.grid(row=3, column=0, padx=10, pady=10)
    set_widget_state(frame_log, False)

    # SOBEL
    frame_sobel = LabelFrame(frame_col, text="Sobel", padx=5, pady=5)
    frame_sobel.grid(row=3, column=0, padx=10, pady=10) 
    # Frame Radiobuttons
    frame_radios = Frame(frame_sobel)
    frame_radios.pack()
    # Variable para almacenar el valor
    radio_var = StringVar()
    radio_var.trace_add('write', apply_filter)
    # Radiobuttons
    Radiobutton(frame_radios, text='Horizontal', variable=radio_var, value='opcion0').grid(row=0, column=0)
    Radiobutton(frame_radios, text='Vertical', variable=radio_var, value='opcion90').grid(row=0, column=1)
    Radiobutton(frame_radios, text='45º', variable=radio_var, value='opcion45').grid(row=0, column=2)
    Radiobutton(frame_radios, text='135º', variable=radio_var, value='opcion135').grid(row=0, column=3)
    radio_var.set('opcion0')
    set_widget_state(frame_sobel, False)

    # CANNY
    frame_canny = LabelFrame(frame_col, text="Canny", padx=5, pady=5)
    frame_canny.grid(row=3, column=1, padx=10, pady=10, sticky='nsew') 
    # Control deslizante
    scale_canny_min = Scale(frame_canny, name='scale_canny_min', from_=1, to=400, orient=HORIZONTAL, length=250, command=apply_filter)
    scale_canny_min.pack(fill='x', expand=True)
    # Control deslizante
    scale_canny_max = Scale(frame_canny, name='scale_canny_max', from_=1, to=400, orient=HORIZONTAL, length=250, command=apply_filter)
    scale_canny_max.pack(fill='x', expand=True)
    set_widget_state(frame_canny, False)

    # OPERACION FINAL
    frame_final = LabelFrame(frame_controles, text="Operación final", padx=5, pady=5)
    frame_final.pack()
    # Frame Radiobuttons
    frame_radios_2 = Frame(frame_final)
    frame_radios_2.pack()
    # Variable para almacenar el valor
    radio_final = StringVar()
    radio_final.trace_add('write', apply_filter)
    # Radiobuttons
    Radiobutton(frame_radios_2, text='Ninguno', variable=radio_final, value='no').grid(row=0, column=0)
    Radiobutton(frame_radios_2, text='Suma', variable=radio_final, value='sum').grid(row=0, column=1)
    Radiobutton(frame_radios_2, text='Resta', variable=radio_final, value='sub').grid(row=0, column=2)
    Radiobutton(frame_radios_2, text='Multiplicación', variable=radio_final, value='mul').grid(row=0, column=3)
    Radiobutton(frame_radios_2, text='División', variable=radio_final, value='div').grid(row=0, column=4)
    Radiobutton(frame_radios_2, text='Negativo', variable=radio_final, value='neg').grid(row=0, column=5)
    radio_final.set('no')
    
    return frame_controles

img = None
img_concat = None

# Crea la ventana de la interfaz de usuario
root = Tk()

# Añade todos los controles
frame_controles = config_controls(root)

# Ejecuta la interfaz de usuario
root.mainloop()