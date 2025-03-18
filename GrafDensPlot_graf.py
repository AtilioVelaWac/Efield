import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


# Parámetros de entrada
L = 48
tipo_de_red = "Square"   #Square   -   Triangular_J=-1   -   Triangular_J=1
Estr = "Exy"
hstr = "hz"

# Leer el DataFrame desde el archivo CSV
archivo1 = "SquareDMxy_L_"+str(L)+"_J1_-1.0000_DMxy_1.0000_Kan_0.0000"
archivo2 = "_Tf_0.0009"
archivo = archivo1 + archivo2 +"_"+ Estr +"_"+ hstr
df = pd.read_csv("D:\\Doctorado\\data2025\\DensityData\\DensityData_"+archivo+".csv")

# Obtener los valores únicos de CampoB y CampoE (ejes X y Y)
arraycampoB = df['CampoB'].unique()
arraycampoE = df['CampoE'].unique()

# Reconstruir el meshgrid
X, Y = np.meshgrid(arraycampoB, arraycampoE)
Nb = len(arraycampoB)
Ne = len(arraycampoE)
# Elegir una de las columnas de densidad para mostrar en el diagrama de fase
# En este caso, vamos a usar DensityChiral
Z = df['DensityChiral'].values.reshape(Ne, Nb) #'DensityPolarX'  'DensityPolarY'  'DensityPolarZ'  'DensityMagnet'  'DensityabsMagnet'  'DensityChiral'

# Crear la figura con dos subgráficos
fig, axes = plt.subplots(2, 2, figsize=(18, 20))
ax1, ax2, ax3, ax4 = axes.flatten()  # Aplanar el array 2x2 a 1D

# Gráfico principal (diagrama de fase) en el primer subplot
c = ax1.pcolormesh(X, Y, Z, shading='auto', cmap='viridis')
fig.colorbar(c, ax=ax1)
ax1.set_title("Chirality in " + tipo_de_red + " lattice for " + Estr + " y " + hstr)
ax1.set_xlabel("Bz", fontsize=22)
ax1.set_ylabel(Estr, fontsize=22)
# Hacer que los ejes del gráfico principal no se muestren
#ax1.set_axis_off()

# Crear el segundo subplot para las previsualizaciones con ejes invisibles
ax2.set_axis_off()  # Esto hace que no se muestren los ejes en el segundo subplot
ax3.set_axis_off()  # Esto hace que no se muestren los ejes en el segundo subplot
ax4.set_axis_off()  # Esto hace que no se muestren los ejes en el segundo subplot

# Inicializar la variable para almacenar el objeto de la imagen actual
current_image_ax2 = None
current_image_ax3 = None
current_image_ax4 = None

# Función para mostrar y eliminar la imagen de previsualización
def mostrar_previsualizacion(event):
    global current_image_ax2, current_image_ax3, current_image_ax4  # Usamos la variable global para almacenar la imagen actual
    if event.inaxes is not None:
        ix = np.abs(arraycampoB - event.xdata).argmin()  # Encuentra el índice más cercano en X
        iy = np.abs(arraycampoE - event.ydata).argmin()  # Encuentra el índice más cercano en Y
        
        campoB = arraycampoB[ix]
        campoE = arraycampoE[iy]
        # Defino el valor de campoE y campoB del punto donde está el mouse
        hh = float(f'{campoB:.2f}')
        Nint = len(str(int(campoB)))
        ee = float(f'{campoE:.2f}')
        if Estr == "Exy":
            camposE = "_"+str(ee).ljust(4,"0")+"00_"+str(ee).ljust(4,"0")+"00_0.0000"
        if Estr == "Ez":
            camposE = "_0.0000_0.0000_"+str(ee).ljust(4,"0")+"00"
        # Cargar la imagen correspondiente (puedes cambiarla a tus imágenes)
        archivo_im = archivo1 + "_E"+camposE + "_hz_"+str(hh).ljust(3+Nint,"0")+"00" + archivo2
        #print(f"Path de la imagen: D:/Doctorado/Pics/P+XvsT/{tipo_de_red}_{Estr}/PxyvsT_{archivo_im}.png")
        img = mpimg.imread("D:/Doctorado/Pics/P+XvsT/"+tipo_de_red+"_"+Estr+"/PxyvsT"+archivo_im+".png")  # Cambia esto a la ruta de tus imágenes
        #img = mpimg.imread("D:\Doctorado\Pics\P+XvsT\Square_Exy\PxyvsTSquareDMxy_L_48_J1_-1.0000_DMxy_1.0000_Kan_0.0000_E_0.0000_0.0000_0.0000_hz_0.7500_Tf_0.0009.png")

        # Si ya hay una imagen mostrada en el espacio de previsualización, eliminarla
        if current_image_ax2 is not None:
            current_image_ax2.remove()
        if current_image_ax3 is not None:
            current_image_ax3.remove()
        if current_image_ax4 is not None:
            current_image_ax4.remove()
        
        # Redimensionar la imagen para que no se recorte y se ajuste al espacio
        #zoom_factor = 0.16  # Puedes ajustar el factor de zoom según sea necesario
        # **Cálculo dinámico del zoom_factor**
        fig_width, fig_height = fig.get_size_inches()  # Tamaño de la figura en pulgadas
        zoom_factor = min(fig_width, fig_height) * 0.01  # Ajusta el factor según el tamaño
        imagebox = OffsetImage(img, zoom=zoom_factor)
        
 # Crear un AnnotationBbox para mostrar la imagen en los subgráficos correspondientes
        current_image_ax2 = AnnotationBbox(imagebox, (0.35, 0.5), frameon=False)
        current_image_ax3 = AnnotationBbox(imagebox, (0.35, 0.5), frameon=False)
        current_image_ax4 = AnnotationBbox(imagebox, (0.35, 0.5), frameon=False)

        # Agregar las imágenes en los subgráficos correspondientes
        ax2.add_artist(current_image_ax2)
        ax3.add_artist(current_image_ax3)
        ax4.add_artist(current_image_ax4)

        # Redibujar el gráfico para actualizar la visualización
        fig.canvas.draw()

    else:
        # Si el cursor está fuera del área del gráfico, eliminar las imágenes
        if current_image_ax2 is not None:
            current_image_ax2.remove()
            current_image_ax2 = None
        if current_image_ax3 is not None:
            current_image_ax3.remove()
            current_image_ax3 = None
        if current_image_ax4 is not None:
            current_image_ax4.remove()
            current_image_ax4 = None
        
        # Redibujar el gráfico para actualizar la visualización
        fig.canvas.draw()


# Conectar el evento de movimiento del mouse para mostrar y eliminar la imagen
fig.canvas.mpl_connect('motion_notify_event', mostrar_previsualizacion)

# Guardar la figura con bbox_inches='tight' para incluir todo el contenido de la figura
#plt.savefig('diagrama_con_previsualizaciones.png', bbox_inches='tight')

# Mostrar la figura
plt.show()
