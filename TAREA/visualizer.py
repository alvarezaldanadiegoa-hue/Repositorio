from math import pi
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category20c, Spectral6
from bokeh.layouts import gridplot
from bokeh.transform import cumsum, dodge
import polars as pl
import numpy as np

class TitanicVisualizer:
    def __init__(self, df: pl.DataFrame):
        self.df = df

    def plot_pie_survivors(self):
        data = self.df.group_by("Status").len().rename({"len": "value"})
        total = data["value"].sum()

        data = data.with_columns(
            (pl.col("value") / total * 2 * pi).alias("angle"),
            (pl.col("value") / total * 100).alias("percentage")
        )
        
        colors = ["#ff9999", "#66b3ff"]
        data = data.with_columns(pl.Series(name="color", values=colors[:len(data)]))

        p = figure(height=350, title="Porcentaje de Fallecidos vs Supervivientes",
                   toolbar_location=None, tools="hover", tooltips="@Status: @percentage{0.2f}%", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='Status', source=data.to_pandas())
        
        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None
        return p

    def plot_hist_age(self):
        
        ages = self.df["Age"].to_numpy()
        
        hist, edges = np.histogram(ages, bins=20) 
        
        p = figure(title="Distribución de Edades", height=350, x_axis_label="Edad", y_axis_label="Cantidad")
        
        p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], 
               fill_color="navy", line_color="white", alpha=0.5)
        return p

    def plot_bar_class(self):
        data = self.df.group_by("Class_Str").len().sort("Class_Str")
        classes = data["Class_Str"].to_list()
        counts = data["len"].to_list()

        p = figure(x_range=classes, height=350, title="Pasajeros por Clase",
                   toolbar_location=None, tools="")
        
        p.vbar(x=classes, top=counts, width=0.9, color=Spectral6[:len(classes)])
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        return p

    def plot_bar_survival_per_class(self):
        classes = sorted(self.df["Class_Str"].unique().to_list())
        statuses = ["Fallecido", "Sobreviviente"]
        
        data = {'classes': classes}
        for status in statuses:
            counts = []
            for cls in classes:
                cnt = self.df.filter((pl.col("Class_Str") == cls) & (pl.col("Status") == status)).height
                counts.append(cnt)
            data[status] = counts

        source = ColumnDataSource(data=data)

        p = figure(x_range=classes, height=350, title="Supervivencia por Clase (Comparativa)",
                   toolbar_location=None, tools="hover", tooltips="$name @classes: @$name")

        p.vbar(x=dodge('classes', -0.2, range=p.x_range), top='Fallecido', width=0.4, source=source,
               color="#e84d60", legend_label="Fallecido")

        p.vbar(x=dodge('classes',  0.2, range=p.x_range), top='Sobreviviente', width=0.4, source=source,
               color="#718dbf", legend_label="Sobreviviente")

        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"
        return p

    def plot_stacked_bar(self):
        classes = sorted(self.df["Class_Str"].unique().to_list())
        statuses = ["Fallecido", "Sobreviviente"]
        
        data = {'classes': classes}
        for status in statuses:
            counts = []
            for cls in classes:
                cnt = self.df.filter((pl.col("Class_Str") == cls) & (pl.col("Status") == status)).height
                counts.append(cnt)
            data[status] = counts

        p = figure(x_range=classes, height=350, title="Supervivencia por Clase (Acumulado)",
                   toolbar_location=None, tools="hover", tooltips="$name @classes: @$name")

        p.vbar_stack(statuses, x='classes', width=0.9, color=["#e84d60", "#718dbf"], source=data,
                     legend_label=statuses)

        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"
        
        return p

    def render_dashboard(self):
        p1 = self.plot_pie_survivors()
        p2 = self.plot_hist_age()
        p3 = self.plot_bar_class()
        p4 = self.plot_bar_survival_per_class()
        p5 = self.plot_stacked_bar()

        grid = gridplot([[p1, p2], [p3, p4], [p5, None]])
        show(grid)