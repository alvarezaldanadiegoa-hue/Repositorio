from data_manager import TitanicDataLoader
from visualizer import TitanicVisualizer
import os

def main():
    csv_path = "titanic.csv"
    
    if not os.path.exists(csv_path):
        print(f"Error: No se encuentra el archivo {csv_path}")
        return

    print("--- Iniciando análisis del Titanic ---")
    loader = TitanicDataLoader(csv_path)
    df = loader.load_data()
    
    if df is not None:
        df_clean = loader.clean_data()
        viz = TitanicVisualizer(df_clean)
        
        print("Generando dashboard interactivo...")
        viz.render_dashboard()
        print("¡Listo! Se ha abierto el dashboard en tu navegador.")

if __name__ == "__main__":
    main()