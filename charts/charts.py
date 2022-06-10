import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class PlotlyCharts():
    """Creates a Plotly plot"""
    def __init__(self, ser: pd.Series, 
                 chart_type: str, 
                 orientation: str = 'v', 
                 sort:str = 'asc',
                 title:str = None,
                 xaxis_text:str = None,
                 yaxis_text:str = None):
        self.ser = ser
        self.chart_type = chart_type
        self.orientation = orientation
        self.sort = sort
        self.title = title
        self.xaxis_text = xaxis_text
        self.yaxis_text = yaxis_text
        self.create()
        
    def create(self):
        if self.chart_type == 'bar':
            if self.sort == 'asc':
                self.ser = self.ser.sort_values(ascending=True)
            if self.sort == 'desc':
                self.ser = self.ser.sort_values(ascending=False)

            if self.orientation == 'v':
                fig = px.bar(self.ser, y=self.ser.index, x=self.ser.values, text_auto='.2s', height=800)
                fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
            if self.orientation == 'h':
                fig = px.bar(self.ser, x=self.ser.index, y=self.ser.values, text_auto='.2s', height=800)
                fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        
            # Labels
            if self.title != None:
                fig.update_layout(title_text=f'{self.title}')
            if self.xaxis_text != None:
                fig.update_layout(xaxis_title=f"{self.xaxis_text}")
            if self.yaxis_text != None:
                fig.update_layout(yaxis_title=f"{self.yaxis_text}")

        return fig