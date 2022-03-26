"""
Plots
└── Documentation = https://aiqc.readthedocs.io/en/latest/notebooks/visualization.html
"""
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from re import sub


class Plot():
	"""Data is prepared in the Queue and Predictor classes before being fed into the methods below."""
	def __init__(self):
		"""__init__ defines a template that is passed to the other plots."""
		self.plot_template = dict(
            layout=go.Layout(
			    font=dict(family='Avenir', color='#FAFAFA')
                , title=dict(x=0.05, y=0.95)
                , titlefont=dict(family='Avenir')
                , title_pad=dict(b=50, t=20)
                , plot_bgcolor='#182d41'#'#181B1E'
                , paper_bgcolor='#182d41'#'#181B1E'
                , hovermode='closest'
                , hoverlabel=dict(
                    bgcolor="#122536"
                    , font=dict(family="Avenir", size=15)
                )
            )
        )


	def performance(
		self, dataframe:object, score_type:str, 
		score_display:str, call_display:bool=True,
		height:int=None
	):
		fig = px.line(
			dataframe
			, title = 'Models Metrics by Split'
			, x = 'loss'
			, y = score_type
			, color = 'predictor_id'
			, height = height
			, hover_data = ['predictor_id', 'split', 'loss', score_type]
			, line_shape='spline'
		)
		fig.update_traces(
			mode = 'markers+lines'
			, line = dict(width = 2)
			, marker = dict(
				size=8, line=dict(width=2, color='white')
			)
		)
		fig.update_layout(
			title_x=0.5#center
			, xaxis_title = "Loss"
			, yaxis_title = score_display
			, template = self.plot_template
		)
		fig.update_xaxes(zeroline=False, gridcolor='#2c3c4a', tickfont=dict(color='#818487'))
		fig.update_yaxes(zeroline=False, gridcolor='#2c3c4a', tickfont=dict(color='#818487'))
		
		if (call_display==True):
			fig.show()
		else:
			return fig


	def learning_curve(
		self, dataframe:object, history_pairs:dict,
		skip_head:bool=False, call_display:bool=True
	):
		"""Dataframe rows are epochs and columns are metric names."""
		if (skip_head==True):
			dataframe = dataframe.tail(round(dataframe.shape[0]*.85))
		# Spline seems to crash with too many points.
		if (dataframe.shape[0] >= 400):
			line_shape = 'linear'
		elif (dataframe.shape[0] < 400):
			line_shape = 'spline'

		# Create a plot for every pair.
		figs = []
		for train,val in history_pairs.items():
			metric_name = sub("_"," ",train[6:])
			df = dataframe[[train,val]]
			fig = px.line(
				df, title=f"Training History: {metric_name}", line_shape=line_shape
			)
			fig.update_layout(
				xaxis_title = "epochs"
				, yaxis_title = metric_name
				, legend_title = None
				, height = 400
				, template = self.plot_template
				, yaxis = dict(
					side = "right"
					, tickmode = 'linear'
					, tick0 = 0.0
					, dtick = 0.05
				)
				, legend = dict(
					orientation="h"
					, yanchor="bottom"
					, y=1.02
					, xanchor="right"
					, x=1
				)
				, margin=dict(t=5),
			)
			fig.update_xaxes(zeroline=False, gridcolor='#2c3c4a', tickfont=dict(color='#818487'))
			fig.update_yaxes(zeroline=False, gridcolor='#2c3c4a', tickfont=dict(color='#818487'))
			if (call_display==True):
				fig.show()
			else:
				figs.append(fig)
		if (call_display==False):
			return figs


	def confusion_matrix(self, cm_by_split, labels, call_display:bool=True):
		figs = []
		for split, cm in cm_by_split.items():
			# change each element of z to type string for annotations
			cm_text = [[str(y) for y in x] for x in cm]

			fig = ff.create_annotated_heatmap(
				cm
				, x=labels
				, y=labels
				, annotation_text=cm_text
				, colorscale=px.colors.sequential.BuGn
				, showscale=True
				, colorbar={"title": 'Count'})

			# add custom xaxis title
			fig.add_annotation(dict(font=dict(color="white", size=12),
									x=0.5,
									y=1.2,
									showarrow=False,
									text="Predicted Label",
									xref="paper",
									yref="paper"))

			# add custom yaxis title
			fig.add_annotation(dict(font=dict(color="white", size=12),
									x=-0.4,
									y=0.5,
									showarrow=False,
									text="Actual Label",
									textangle=-90,
									xref="paper",
									yref="paper"))

			fig.update_layout(
				title=f"Confusion Matrix: {split.capitalize()}"
				, legend_title='Sample Count'
				, template=self.plot_template
				, height=375  # if too small, it won't render in Jupyter.
				, width=850 # keeps squares square.
				, yaxis=dict(
					tickmode='linear'
					, tick0=0.0
					, dtick=1.0
					, fixedrange=True#prevents zoom/pan
					, tickfont = dict(
						size=10
					)
				)
				, xaxis=dict(
					categoryorder='category descending'
					, fixedrange=True#prevents zoom/pan
					, tickfont=dict(
						size=10
					)
				)
				, margin=dict(
					r=325
					, l=325
				)
			)

			fig.update_traces(
				hovertemplate = """predicted: %{x}<br>actual: %{y}<br>count: %{z}<extra></extra>"""
			)
			if (call_display==True):
				fig.show()
			else:
				figs.append(fig)
		if (call_display==False):
			return figs


	def precision_recall(self, dataframe:object, call_display:bool=True):
		fig = px.line(
			dataframe
			, x = 'recall'
			, y = 'precision'
			, color = 'split'
			, title = 'Precision-Recall Curves'
		)
		fig.update_layout(
			legend_title = None
			, template = self.plot_template
			, height = 500
			, yaxis = dict(
				side = "right"
				, tickmode = 'linear'
				, tick0 = 0.0
				, dtick = 0.05
			)
			, legend = dict(
				orientation="h"
				, yanchor="bottom"
				, y=1.02
				, xanchor="right"
				, x=1
			)
		)
		fig.update_xaxes(zeroline=False, gridcolor='#2c3c4a', tickfont=dict(color='#818487'))
		fig.update_yaxes(zeroline=False, gridcolor='#2c3c4a', tickfont=dict(color='#818487'))
		if (call_display==True):
			fig.show()
		else:
			return fig


	def roc_curve(self, dataframe:object, call_display:bool=True):
		fig = px.line(
			dataframe
			, x = 'fpr'
			, y = 'tpr'
			, color = 'split'
			, title = 'Receiver Operating Characteristic (ROC) Curves'
		)
		fig.update_layout(
			legend_title = None
			, template = self.plot_template
			, height = 500
			, xaxis = dict(
				title = "False Positive Rate (FPR)"
				, tick0 = 0.00
				, range = [-0.025,1]
			)
			, yaxis = dict(
				title = "True Positive Rate (TPR)"
				, side = "left"
				, tickmode = 'linear'
				, tick0 = 0.00
				, dtick = 0.05
				, range = [0,1.05]
			)
			, legend = dict(
				orientation="h"
				, yanchor="bottom"
				, y=1.02
				, xanchor="right"
				, x=1
			)
			, shapes=[
				dict(
					type = 'line'
					, y0=0, y1=1
					, x0=0, x1=1
					, line = dict(dash='dot', width=2, color='#3b4043')
			)]
		)
		fig.update_xaxes(zeroline=False, gridcolor='#2c3c4a', tickfont=dict(color='#818487'))
		fig.update_yaxes(zeroline=False, gridcolor='#2c3c4a', tickfont=dict(color='#818487'))
		if (call_display==True):
			fig.show()
		else:
			return fig
	

	def feature_importance(
		self, feature_impacts:object, feature_id:int,
		permute_count:int, height:int, top_n:int,
		call_display:bool
	):
		if (top_n is not None):
			title = f"Feature Importance <sub>(feature.id:{feature_id}, permute_count:{permute_count}, top_n:{top_n})</sub><br><br>"
		elif (top_n is None):
			title = f"Feature Importance <sub>(feature.id:{feature_id}, permute_count:{permute_count})</sub><br><br>"
		
		fig = go.Figure()
		for feature, impacts in feature_impacts.items():
			fig.add_trace(go.Box(x=impacts, name=feature))
		fig.update_layout(
			template = self.plot_template
			, height = height
			, title = title
			, showlegend = False
		)
		fig.update_xaxes(
			title = f"Importance<br><sup>[permuted column loss - training loss]</sup>",
			# ticks not really showing.
			tickangle=45, nticks=15, gridcolor='#2c3c4a'
		)
		if (call_display==True):
			fig.show()
		else:
			return fig
