import os
from PIL import Image


def optimize_image(file_path, quality=85):
    """Comprime a imagem para a qualidade especificada."""
    try:
        with Image.open(file_path) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(file_path, optimize=True, quality=quality)
            print(f"Imagem otimizada: {file_path}")
    except Exception as e:
        print(f"Erro ao otimizar a imagem {file_path}: {e}")


def scan_directory(directory):
    """Percorre o diretório e otimiza todas as imagens encontradas."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                file_path = os.path.join(root, file)
                optimize_image(file_path)


# Caminho para o diretório que deseja otimizar
directory_path = "images"
scan_directory(directory_path)
