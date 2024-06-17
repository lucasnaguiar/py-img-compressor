import os
import sys
from PIL import Image
import logging


def resize_image(img, max_width, max_height):
    """Redimensiona a imagem para a resolução especificada se for maior que max_width x max_height."""
    width, height = img.size
    if width > max_width or height > max_height:
        # Calcula a proporção de redimensionamento mantendo a relação de aspecto
        ratio = min(max_width / width, max_height / height)
        new_size = (int(width * ratio), int(height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
        logging.info(f"Imagem redimensionada para: {new_size}")
    return img


def optimize_image(file_path, quality=33, max_width=1920, max_height=1080):
    """Comprime a imagem para a qualidade especificada e redimensiona se necessário."""
    try:
        with Image.open(file_path) as img:
            img = resize_image(img, max_width, max_height)
            if file_path.lower().endswith(".png") and img.mode in ("RGBA", "P"):
                img = img.convert("RGBA")
            elif img.mode != "RGB":
                img = img.convert("RGB")
            img.save(file_path, optimize=True, quality=quality)
            logging.info(f"Imagem otimizada: {file_path}")
    except Exception as e:
        logging.error(f"Erro ao otimizar a imagem {file_path}: {e}")


def scan_directory(
    directory, quality=33, max_width=1920, max_height=1080, min_size_mb=3
):
    """Percorre o diretório e otimiza todas as imagens encontradas que são maiores que min_size_mb."""
    min_size_bytes = min_size_mb * 1024 * 1024
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) > min_size_bytes:
                    optimize_image(file_path, quality, max_width, max_height)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py <caminho_do_diretorio> [qualidade] [min_size_mb]")
        sys.exit(1)

    directory_path = sys.argv[1]
    quality = int(sys.argv[2]) if len(sys.argv) > 2 else 33
    min_size_mb = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    logging.basicConfig(level=logging.INFO)
    scan_directory(directory_path, quality, min_size_mb=min_size_mb)
