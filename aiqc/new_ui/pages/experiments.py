# Local modules
import aiqc.orm
from aiqc.utils.meter import metrics_classify, metrics_regress
# UI modules
import dash
from dash import html
from dash import dcc, html, register_page
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

register_page(__name__, path='/')

refresh_seconds = 10*1000

# Dash naturally wraps in `id=_pages_content`
layout = html.Div(
    [
        html.P('experiments_page')
    ]
)

# layout = html.Div(
#     [
#         dcc.Interval(id="initial_load", n_intervals=0, max_intervals=-1, interval=refresh_seconds),
#         # ====== NAVBAR ======
#         html.Div(
#             html.Center(
#                 html.A(
#                     html.Img(src="assets/logo_wide_small.svg", height="35px"),
#                     href="https://aiqc.readthedocs.io",
#                 ),
#                 className='logo'
#             ),
#             className='navig'
#         ),
#         # Grid system Div(Row(Col(Div)))
#         # dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
#         # ====== EXPERIMENT ======
#         dbc.Row(
#             [
#                 # =CONTROLS=
#                 dbc.Col(
#                     dbc.InputGroup(
#                         [
#                             dbc.InputGroupText("Experiment ID"),
#                             # Not a callback because it is the first inputable object.
#                             dbc.Select(id='exp_dropdown'),
#                         ],
#                         size="sm", className='ctrl_chart ctrl_big ctr'
#                     ),
#                     width=3, align="center", className='ctrl_col_big'
#                 ),
#                 dbc.Col(
#                     dbc.InputGroup(
#                         [
#                             dbc.InputGroupText("Score Type"),
#                             # Defined by downstream callback
#                             dbc.Select(id='exp_type'),
#                         ],
#                         size="sm", className='ctrl_chart ctrl_big ctr'
#                     ),
#                     width=3, align="center", className='ctrl_col_big'
#                 ),
#                 dbc.Col(
#                     dbc.InputGroup(
#                         [
#                             dbc.InputGroupText("Min Score"),
#                             dbc.Input(
#                                 type="number",id='exp_score',
#                                 placeholder="-∞"
#                             ),
#                         ],
#                         size="sm", className='ctrl_chart ctrl_sm ctr'
#                     ),
#                     width=2, align="center", className='ctrl_col_sm'
#                 ),
#                 dbc.Col(
#                     dbc.InputGroup(
#                         [
#                             dbc.InputGroupText("Max Loss"),
#                             dbc.Input(
#                                 type="number",id='exp_loss',
#                                 placeholder="+∞"
#                             ),
#                         ],
#                         size="sm", className='ctrl_chart ctrl_sm ctr'
#                     ),
#                     width=2, align="center", className='ctrl_col_sm'
#                 ),
#                 dbc.Col(
#                     dbc.InputGroup(
#                         [
#                             dbc.Button(
#                                 "Filter", outline=True, 
#                                 n_clicks=0, id="exp_button",
#                                 className='chart_button ctr',
#                             ),
#                         ],
#                         size="sm", className='ctrl_chart ctr'
#                     ),
#                     width=1, align="center",
#                 ),
#             ],
#             className='exp_ctrl_row'
#         ),
#         dbc.Row(
#             [
#                 dbc.Col(
#                     html.Div(
#                         dbc.Spinner(
#                             color="info", delay_hide=1,
#                             spinner_style={"width": "4rem", "height": "4rem"}
#                         ),
#                         className='spinner'
#                     ),
#                     id="exp_plot_contain", width=8, align="center"
#                 ),
#                 dbc.Col(
#                     dbc.Alert(
#                         "Click on a model in the chart on the left to show its parameters.",
#                         className='alert'
#                     ),
#                     id="param_pane", className='hp_contain',
#                     width=4, align="center"
#                 )
#             ],
#             className='exp_row'
#         ),
#         # ====== BOTTOM BAR ======
#         # Stacked so sticks to top regardless of progress bar presence 
#         html.Div(
#             [
#                 # =PROGRESS BAR=
#                 # w/o gutter class the rounded edges of bar don't fill.
#                 dbc.Row(id="progress_container", className='g-0'),
#                 # =OPTIONS=
#                 dbc.Row(
#                     [
#                         dbc.Col(width="4"),
#                         dbc.Col(
#                             dcc.Dropdown(id="multitron", multi=True, className='multitron ctr'),
#                             width="4", align="center",
#                         ),
#                         dbc.Col(width="3"),
#                         dbc.Col(
#                             html.Div(html.A("⇪",href="#",className='up_arrow')),
#                             width="1", align="center",
#                         )
#                     ]
#                 )
#             ],
#             className='middle_bar'
#         ),
#         html.Br(),html.Br(),html.Br(),
#         dbc.Row(id="model_container"),
#         html.Br(),
#         # Multi-page app requires this in layout children
#         page_container
#     ],
#     className='page',
# )


# # Helper functions for callbacks.
# def fetch_params(predictor:object, size:str):
#     hyperparameters = predictor.get_hyperparameters()
#     if (hyperparameters is not None):
#         headers = [html.Th("parameter"), html.Th("value")]
#         table_header = [html.Thead(html.Tr(headers), className='thead')]
#         # bools are not rendering so need to force them to str
#         rows = []
#         for k,v in hyperparameters.items():
#             if isinstance(v,bool):
#                 v = str(v) 
#             rows.append(
#                 html.Tr([html.Td(k), html.Td(v)])
#             )
#         table_body = [html.Tbody(rows)]
#         hp_table = dbc.Table(
#             table_header + table_body,
#             dark=True, hover=True, responsive=True,
#             striped=True, bordered=False, className=f"tbl {size} ctr"
#         )
#     else:
#         msg = "Sorry - This model has no parameters."
#         hp_table = dbc.Alert(msg, className='alert')
#     return hp_table


# """
# - When the page is started and refreshed, this updates things.
# - You can only use objects at the start of the DAG, 
#   e.g. not `exp_plot.clickData` because it doesn't exist yet.
# """
# @app.callback(
#     [
#         Output(component_id="exp_dropdown", component_property="options"),
#         Output(component_id="exp_dropdown", component_property="placeholder"),
#         Output(component_id="exp_dropdown", component_property="value"),        
#         Output(component_id='multitron',    component_property='options'),
#         Output(component_id='multitron',    component_property='placeholder'),
#         Output(component_id="multitron",    component_property="value"),
#     ],
#     Input(component_id="initial_load", component_property="n_intervals"),
#     [
#         State(component_id="exp_dropdown", component_property="value"),        
#         State(component_id='multitron',    component_property='value'),
#     ]
# )
# def refresh(n_intervals:int, queue_id:int, model_ids:int):
#     queues = list(orm.Queue)
#     if (not queues):
#         return [], "None yet", None, [], "None yet", []
    
#     # Initially the IDs are None becuse there is no State.
#     queues.reverse()
#     queue_options = [dict(label=str(q.id), value=q.id) for q in queues]
#     if (queue_id is None):
#         queue_id = queues[0].id
    
#     models = list(orm.Predictor)
#     models.reverse()
#     model_options = [dict(label=f"Model:{m.id}", value=m.id) for m in models]
    
#     return queue_options, None, queue_id, model_options, "Compare models head-to-head", model_ids


# @app.callback(
#     Output(component_id="progress_container", component_property="children"),
#     Input(component_id="exp_dropdown",        component_property="value"),
# )
# def update_progress(queue_id:int):
#     if (queue_id is None):
#         return None
#     queue = orm.Queue.get_by_id(queue_id)
#     progress = round(queue.runs_completed/queue.total_runs*100)
    
#     if (progress<100):
#         children = dbc.Progress(
#             id="progress_bar", className='prog_bar ctr', color="secondary",
#             value=progress, label=f"{progress}%"
#         )
#         return children 
#     else:
#         return None


# @app.callback(
#     [
#         Output(component_id='exp_type', component_property='options'),
#         Output(component_id='exp_type', component_property='value'),
#     ],
#     Input(component_id='exp_dropdown', component_property='value'),
#     [
#         State(component_id='exp_type', component_property='value'),
#     ]
# )
# def type_dropdown(queue_id:object, exp_type:str):
#     if (queue_id is None):
#         raise PreventUpdate
    
#     queue = orm.Queue.get_by_id(queue_id)
#     analysis_type = queue.algorithm.analysis_type
#     if ('classification' in analysis_type):
#         score_types = metrics_classify
#         if (exp_type not in score_types):
#             exp_type = 'accuracy'
#     elif('regression' in analysis_type):   
#         score_types = metrics_regress
#         if (exp_type not in score_types):
#             exp_type = 'r2'
    
#     options = [{"label":m, "value":col} for col, m in score_types.items()]
#     return options, exp_type


# @app.callback(
#     Output(component_id='exp_plot_contain', component_property='children'),
#     Input(component_id='exp_button',        component_property='n_clicks'),
#     [
#         State(component_id='exp_dropdown', component_property='value'),
#         State(component_id='exp_type',     component_property='value'),
#         State(component_id='exp_score',    component_property='value'),
#         State(component_id='exp_loss',     component_property='value'),
#     ]
# )
# def plot_experiment(
#     n_clicks:int, queue_id:object,
#     score_type:str, min_score:float, max_loss:float,
# ):   
#     if (queue_id is None):
#         queues = list(orm.Queue)
#         if (not queues):
#             msg = "Sorry - Cannot display plot because no Queues exist yet. Data will refresh automatically."
#             return dbc.Alert(msg, className='alert')
#         else:
#             # Plot the most recent by default
#             queue = queues[-1]
#     else:
#         queue = orm.Queue.get_by_id(queue_id)
    
#     try:
#         fig = queue.plot_performance(
#             score_type=score_type, min_score=min_score, max_loss=max_loss,
#             call_display=False, height=500
#         )
#     except Exception as err_msg:
#         return dbc.Alert(str(err_msg), className='alert')
#     else:
#         fig = dcc.Graph(id="exp_plot", figure=fig, className='exp_plot_contain ctr')
#         return fig


# @app.callback(
#     Output(component_id='exp_button', component_property='n_clicks'),
#     Input(component_id='exp_type',    component_property='value'),
#     State(component_id='exp_button',  component_property='n_clicks'),
# )
# def trigger_graph(score_type:str, n_clicks:int):
#     n_clicks += 1
#     return n_clicks


# @app.callback(
#     Output(component_id='param_pane', component_property='children'),
#     # `Input...clickAnnotationData` returns None
#     Input(component_id='exp_plot',    component_property='clickData'),
# )
# def interactive_params(new_click:dict):
#     """
#     It's hard to maintain clickData State because exp_plot doesn't exist when 
#     the page loads and exp_plot gets overrode when the page refreshes.
#     """
#     if (new_click is None):
#         raise PreventUpdate
#     # The docs say to use `json.dumps`, but clickData is just a dict.
#     predictor   = new_click['points'][0]['customdata'][0]    
#     predictor   = orm.Predictor.get_by_id(predictor)
#     title       = f"Model ID: {predictor}"
#     model_title = html.P(title, className='header')
#     hp_table    = fetch_params(predictor, "tbig")
#     return [model_title, hp_table]


# @app.callback(
#     Output(component_id='model_container', component_property='children'),
#     Input(component_id='multitron',        component_property='value')
# )
# def model_plots(predictor_ids:list):
#     # Initially it's None, but empty list when it's cleared.
#     if ((predictor_ids is None) or (not predictor_ids)):
#         msg = "Select up to two models from the dropdown above."
#         return dbc.Alert(msg, className='alert', style={"width":"50%"})
#     pred_count = len(predictor_ids)
#     if (pred_count==1):
#         col_width = 12
#     elif (pred_count==2):
#         col_width = 6
#     elif (pred_count>2):
#         msg = "Sorry - Only 2 models can be displayed at once."
#         return dbc.Alert(msg, className='alert')
#     multi_cols = []
#     for predictor_id in predictor_ids:
#         # Only `big_column` is assigned a bootstrap width.
#         big_column = []

#         predictor = orm.Predictor.get_by_id(predictor_id)
#         predictions = list(predictor.predictions)
#         if (not predictions):
#             msg = f"Sorry - Metrics for this model are not ready yet. Data will refresh automatically."
#             return dbc.Col(dbc.Alert(msg, className='alert'))
#         prediction = predictions[0]

#         # === METRICS ===
#         metrics = prediction.metrics
#         # Need the 'split' to be in the same dict as the metrics.
#         metrics_records = []
#         for split, metrix in metrics.items():
#             if (metrix is not None):
#                 split_dikt = {'split':split}
#                 # We want the split to appear first in the dict
#                 split_dikt.update(metrix)
#                 metrics_records.append(split_dikt)
#         cols         = list(metrics_records[0].keys())
#         headers      = [html.Th(c) for c in cols]
#         table_header = [html.Thead(html.Tr(headers))]

#         metrics_raw = []
#         for record in metrics_records:
#             metrics = [v for k,v in record.items()]
#             metrics_raw.append(metrics)

#         rows = []
#         for cells in metrics_raw:
#             row = html.Tr([html.Td(cell) for cell in cells]) 
#             rows.append(row)            
#         table_body = [html.Tbody(rows)]
#         metrics_table = dbc.Table(
#             table_header + table_body
#             , dark       = True
#             , hover      = True
#             , responsive = True
#             , striped    = True
#             , bordered   = False
#             , className  = 'tbl tbig ctr'
#         )

#         row = dbc.Row(
#             dbc.Col(metrics_table, align="center")
#         )
#         big_column.append(row)
#         big_column.append(html.Hr(className='hrz ctr'))

#         # === HYPERPARAMETERS ===
#         hp_table = fetch_params(predictor, "tsmall")
#         row = dbc.Row(
#             dbc.Col(hp_table, align="center")
#         )
#         big_column.append(row)
#         big_column.append(html.Hr(className='hrz ctr'))

#         # === LEARNING ===
#         learning_curves = predictor.plot_learning_curve(
#             call_display=False, skip_head=False
#         )
#         learning_curves = [dcc.Graph(figure=fig, className='plots ctr') for fig in learning_curves]
#         row = dbc.Row(
#             [
#                 dbc.Col(learning_curves, id="learning_plots"),
#             ]
#         )
#         big_column.append(row)
#         big_column.append(html.Hr(className='hrz ctr'))

#         # === IMPORTANCE ===
#         feature_importance = prediction.feature_importance
#         if (feature_importance is not None):
#             prediction = orm.Predictor.get_by_id(predictor_id).predictions[0]
#             content    = prediction.plot_feature_importance(top_n=15, call_display=False)
#             content    = [dcc.Graph(figure=fig, className='plots ctr') for fig in content]
#         elif (feature_importance is None):
#             msg = "Feature importance not calculated for model yet."
#             content = dbc.Alert(msg, className='alert')

#         row = dbc.Row(
#             dbc.Col(content, id="importance_plots")
#         )
#         big_column.append(row)
#         big_column.append(html.Hr(className='hrz ctr'))

#         # === CLASSIFICATION ===
#         analysis_type = predictor.job.queue.algorithm.analysis_type
#         if ('classification' in analysis_type):
#             # === ROC ===
#             roc = prediction.plot_roc_curve(call_display=False)
#             roc = dcc.Graph(figure=roc, className='plots ctr')
#             row = dbc.Row(
#                 dbc.Col(roc, align="center")
#             )
#             big_column.append(row)
#             big_column.append(html.Hr(className='hrz ctr'))
#             # === PRC ===
#             pr = prediction.plot_precision_recall(call_display=False)
#             pr = dcc.Graph(figure=pr, className='plots ctr')
#             row = dbc.Row(
#                 dbc.Col(pr, align="center")
#             )
#             big_column.append(row)
#             big_column.append(html.Hr(className='hrz ctr'))
#             # === CONFUSION ===
#             cms = prediction.plot_confusion_matrix(call_display=False)
#             cms = [dcc.Graph(figure=fig, className='plots ctr') for fig in cms]                
#             row = dbc.Row(
#                 dbc.Col(cms, align="center")
#             )
#             big_column.append(row)
#             big_column.append(html.Br())
#             big_column.append(html.Br())
#         big_column = dbc.Col(big_column, width=col_width)
#         multi_cols.append(big_column)
#     return multi_cols