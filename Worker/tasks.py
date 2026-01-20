from celery import Celery
import cv2
import numpy as np
import os

# Configuración: Solo Redis
celery_app = Celery('tasks', broker='redis://redis:6379/0')

def apply_sepia(img):
    """Filtro Sepia"""
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    return cv2.transform(img, kernel)

def apply_sketch(img):
    """Filtro Boceto"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (21, 21), 0)
    return cv2.divide(gray, 255 - blur, scale=256)

@celery_app.task(name='tasks.process_image')
def process_image(image_path):
    print(f"--- [WORKER] Procesando imagen: {image_path} ---")
    
    if not os.path.exists(image_path):
        return f"Error: Archivo {image_path} no encontrado"
    
    # 1. Leer imagen
    original = cv2.imread(image_path)
    if original is None:
        return "Error: No se pudo leer la imagen (formato incorrecto)"

    base_name = os.path.splitext(image_path)[0]
    
    # 2. Generar y Guardar Variaciones
    noir = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f"{base_name}_scenario_noir.jpg", noir)
    
    sketch = apply_sketch(original)
    cv2.imwrite(f"{base_name}_scenario_sketch.jpg", sketch)

    # Sepia
    sepia = apply_sepia(original)
    cv2.imwrite(f"{base_name}_scenario_sepia.jpg", sepia)
    
    print(f"--- [WORKER] ¡Éxito! Generados 3 escenarios ---")
    return "Procesamiento completado"