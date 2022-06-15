import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import random
import sys
sys.path.append('../')


class PlotlyBarChart:
    """Creates a Plotly plot"""
    def create(self,
               df: pd.DataFrame,
               item: str,
               history,
               color_fig_bg: str = 'rgba(179, 211, 255, 0.5)'):
               
        dfb = df.query(f'Items == "{item}"')
        dfb = pd.DataFrame(dfb.groupby('date').size()).reset_index()
        dfb = dfb.rename({0: 'true_values'}, axis=1)
        for i in range(len(dfb)):
            d = random.randint(-5, 5)
            if d >= 0:
                dfb.loc[i, 'prediction'] = dfb.loc[i, 'true_values'] + d
            else:
                dfb.loc[i, 'prediction'] = 0

        dfb = dfb[-10:]

        if history:
            fig = make_subplots(vertical_spacing = 0.005, rows=2, cols=1,
                            row_width=[0.3, 0.7])
        else:
            fig = make_subplots(rows=1, cols=1)

        bar_color = 'rgb(19, 216, 242)'
        prob_dist_color = 'rgb(63, 92, 196)'

        if history:
            figx = go.Bar(name='True Sales', x=dfb.date, y=dfb.true_values)
            fig.update_layout(xaxis={'side': 'top'})
            figy = go.Bar(name='Prediction', x=dfb.date, y=dfb.prediction, marker=dict(color=bar_color))
        figz = go.Scatter(y=[0,1,2,4,6,7,6,4,3,2,1], mode="lines", line_color=prob_dist_color)

        #fig.update_layout(autosize=False,height=300)
        if history:
            fig.add_trace(figx, row=1, col=1)
            fig.add_trace(figy, row=1, col=1)
            fig.add_trace(figz, row=2, col=1)
        else:
            fig.add_trace(figz, row=1, col=1)
        fig['layout'].update(margin=dict(l=0,r=0,b=0,t=30))

        # hide all the xticks
        fig.update_xaxes(showticklabels=False)
        fig.update_xaxes(showticklabels=True, row=2, col=1)
        fig.update_layout(showlegend=False)
        fig.update_layout(
            plot_bgcolor= color_fig_bg,
            paper_bgcolor= 'rgba(0, 0, 0, 0)'
        )

        return fig