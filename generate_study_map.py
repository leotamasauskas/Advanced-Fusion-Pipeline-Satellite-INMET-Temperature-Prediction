import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import os

# --- 1. Load Data ---
shp_path = r'd:\csbc_wcama\shp\shp_para\limites_municipais_ibge.shp'
output_dir = r'd:\csbc_wcama\img'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

gdf = gpd.read_file(shp_path)

# Filter for Belem (Study Area) and the rest of the state
belem = gdf[gdf['nmmun'] == 'BELÉM'].copy()
para = gdf.copy()

# --- 2. Side-by-Side Plot Configuration ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10), gridspec_kw={'width_ratios': [1, 1]})

# --- PANEL 1: Belém (Local Context - Left) ---
# Plot surrounding municipalities
para.plot(ax=ax1, color='lightgray', edgecolor='white', linewidth=0.5)

# Plot Belem in Red highlight
belem.plot(ax=ax1, color='red', edgecolor='black', linewidth=1.5, label='Área de Belém')

# Set bounds for Belem (Zoomed in)
ax1.set_ylim(-1.6, -1.05)
ax1.set_xlim(-48.7, -48.2)

ax1.set_xlabel('Longitude', fontsize=10)
ax1.set_ylabel('Latitude', fontsize=10)
ax1.set_title('A. Detalhe do Município de Belém', fontsize=14, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.5)

# --- PANEL 2: Pará State (Regional Context - Right) ---
# Plot all municipalities with black borders
para.plot(ax=ax2, color='white', edgecolor='black', linewidth=0.3)

# Highlight Belem in Red in the State Map too
belem.plot(ax=ax2, color='red', edgecolor='black', linewidth=0.5)

# Zoom in on the regional area of Belém (Northeastern Pará)
ax2.set_ylim(-3.5, 0.5)
ax2.set_xlim(-51.5, -46.5)

# Add Grid to State Map
ax2.grid(True, linestyle='--', alpha=0.7)

ax2.set_xlabel('Longitude', fontsize=10)
ax2.set_ylabel('Latitude', fontsize=10)
ax2.set_title('B. Localização Regional (Estado do Pará)', fontsize=14, fontweight='bold')

# --- 3. Cartographic Elements and Meta ---

# Scale Bar (15 km) on the Left Panel (Local)
# Approx 1 degree latitude = 111km. 15km / 111km ~ 0.135 degrees
scalebar = AnchoredSizeBar(ax1.transData, 0.135, '15 km', 'lower right', 
                           pad=0.5, color='black', frameon=False, size_vertical=0.005)
ax1.add_artist(scalebar)

# Global Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='s', color='w', label='Município de Belém', markerfacecolor='red', markersize=12, markeredgecolor='black'),
    Line2D([0], [0], marker='s', color='w', label='Outros Municípios', markerfacecolor='lightgray', markersize=12, markeredgecolor='white'),
    Line2D([1], [0], color='black', label='Divisas Municipais', linewidth=1)
]
fig.legend(handles=legend_elements, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.05), title='Legenda')

# Technical Data Box (Global or bottom right of ax2)
tech_text = (
    "Sist. de Coordenadas: Geográficas (GCS)\n"
    "Datum (Referência): EPSG:4326 (WGS 84)\n"
    "Fonte: IBGE | Criado em: Outubro de 2024"
)
plt.figtext(0.9, 0.02, tech_text, ha='right', va='bottom', fontsize=9, 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))

# Main Figure Title
plt.suptitle('Área de Estudo - Município de Belém, PA', fontsize=18, fontweight='bold', y=0.95)

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0.08, 1, 0.93])

# Save
output_path = os.path.join(output_dir, 'mapa_belem.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Map saved to: {output_path}")
plt.close()
