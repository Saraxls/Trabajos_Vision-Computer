import numpy as np
import skimage.io as skio
import matplotlib.pyplot as plt

# Cargar la imagen original
image = skio.imread('image14.jpg')

# Dividir la imagen en tres canales (asumiendo que son partes iguales verticalmente)
height = image.shape[0] // 3
blue_channel = image[:height]  # Canal azul
green_channel = image[height:2 * height]  # Canal verde
red_channel = image[2 * height:3 * height]  # Canal rojo


# Funcion para alinear usando Sum of Squared Differences (SSD)
def align_images(base, to_align, search_range=15):
    best_offset = (0, 0)
    best_score = np.inf  # Valor inicial de "infinito"

    for x_shift in range(-search_range, search_range + 1):
        for y_shift in range(-search_range, search_range + 1):
            # Mover la imagen
            shifted = np.roll(to_align, (x_shift, y_shift), axis=(0, 1))

            # Calcular la metrica SSD
            ssd = np.sum((base - shifted) ** 2)

            # Si el score es mejor, guardamos el offset
            if ssd < best_score:
                best_score = ssd
                best_offset = (x_shift, y_shift)

    # Retornar la imagen alineada
    aligned_image = np.roll(to_align, best_offset, axis=(0, 1))
    return aligned_image


# Alinear los canales
aligned_green = align_images(blue_channel, green_channel)
aligned_red = align_images(blue_channel, red_channel)

# Crear la imagen RGB
rgb_image = np.dstack([aligned_red, aligned_green, blue_channel])

# Mostrar la imagen final
plt.figure(figsize=(8, 8))
plt.imshow(rgb_image)
plt.axis('off')
plt.show()

# Guardar la imagen resultante
skio.imsave('prokudin_result.png', rgb_image)