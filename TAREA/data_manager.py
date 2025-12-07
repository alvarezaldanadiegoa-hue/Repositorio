import polars as pl

class TitanicDataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """Carga los datos desde el archivo CSV."""
        try:
            self.df = pl.read_csv(self.file_path, ignore_errors=True)
            print(f"Datos cargados exitosamente. Dimensiones: {self.df.shape}")
            return self.df
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            return None

    def clean_data(self):
        if self.df is None:
            raise ValueError("El DataFrame está vacío. Carga los datos primero.")

        median_age = self.df["Age"].median()
        self.df = self.df.with_columns(
            pl.col("Age").fill_null(median_age)
        )

        self.df = self.df.with_columns(
            pl.when(pl.col("Survived") == 1)
            .then(pl.lit("Sobreviviente"))
            .otherwise(pl.lit("Fallecido"))
            .alias("Status")
        )

        self.df = self.df.with_columns(
            pl.col("Pclass").cast(pl.Utf8).alias("Class_Str")
        )

        return self.df