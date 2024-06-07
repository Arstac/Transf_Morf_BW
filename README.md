
# Procesamiento de Imágenes con OpenCV y Tkinter

Este proyecto demuestra el uso de varias técnicas de procesamiento de imágenes utilizando OpenCV y Tkinter para la interacción GUI. La aplicación permite a los usuarios cargar una imagen, aplicar diferentes filtros y transformaciones, y luego guardar la imagen procesada.

## Características

- **Cargar y Guardar Imágenes**: Cargar imágenes desde tu sistema de archivos y guardar las imágenes procesadas.
- **Filtros y Transformaciones**: Aplicar una variedad de filtros y transformaciones incluyendo:
  - Suavizado (Gaussian Blur)
  - Afilado
  - Promedio (Average Blur)
  - Mediana (Median Blur)
  - Erosión
  - Dilatación
  - Apertura (Opening)
  - Clausura (Closing)
  - Gradiente
  - White Top-Hat
  - Black Top-Hat
  - Sobel (con diferentes orientaciones)
  - Laplaciano (Laplacian)
  - Detección de bordes de Canny
  - Transformación Log
- **Operaciones Aritméticas**: Realizar operaciones aritméticas como suma, resta, multiplicación, división y transformación negativa.

## Requisitos

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Tkinter
- SciPy

## Instalación

Para ejecutar este proyecto, necesitas tener Python instalado junto con las bibliotecas requeridas. Puedes instalar las bibliotecas necesarias usando pip:

```sh
pip install numpy opencv-python scipy
```

## Uso

1. Clona el repositorio o descarga el código fuente.
2. Ejecuta el script:

   ```sh
   python script_name.py
   ```

3. Se abrirá la ventana de la aplicación. Puedes usar los botones para cargar una imagen y aplicar varios filtros y transformaciones.

## Descripción del Código

### Funciones Principales

- **get_control_by_name**: Busca recursivamente un widget por su nombre.
- **redim_img**: Redimensiona una imagen a una altura específica, manteniendo la relación de aspecto.
- **suavizado**: Aplica desenfoque gaussiano basado en el valor del control.
- **afilado**: Aplica un filtro de enfoque.
- **promedio**: Aplica un filtro de promediado.
- **mediana**: Aplica un filtro de mediana.
- **erosion**: Aplica erosión basada en el valor del control.
- **dilatacion**: Aplica dilatación basada en el valor del control.
- **log**: Aplica una transformación logarítmica.
- **apertura**: Aplica una operación de apertura (erosión seguida de dilatación).
- **clausura**: Aplica una operación de cierre (dilatación seguida de erosión).
- **gradiente**: Calcula el gradiente de la imagen.
- **whitetophat**: Aplica una transformación de sombrero blanco.
- **blacktophat**: Aplica una transformación de sombrero negro.
- **sobel**: Aplica un filtro Sobel en diferentes orientaciones.
- **laplaciano**: Aplica un filtro Laplaciano.
- **canny**: Aplica detección de bordes de Canny basada en los valores del control.
- **final**: Combina dos imágenes usando una operación específica.
- **apply_filter**: Aplica los filtros y transformaciones seleccionados a la imagen.
- **load_image**: Carga una imagen desde el sistema de archivos.
- **save_image**: Guarda la imagen procesada en el sistema de archivos.

### Configuración de la GUI

- **config_controls**: Configura los controles de la GUI, incluyendo botones, deslizadores y menús desplegables para la selección de filtros.

### Variables Globales

- `img`: Almacena la imagen cargada.
- `img_concat`: Almacena la imagen concatenada para su visualización.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
