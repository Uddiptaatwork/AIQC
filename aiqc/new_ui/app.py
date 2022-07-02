from dash import Dash, page_registry, page_container, html, dcc, Input, Output
import dash_bootstrap_components as dbc
"""
- Stopped using jupyter_dash when they removed `_terminate_server_for_port`
  It wasn't reliable: hung ports with leaks, silent failures.
- Kill the dash server with `ctrl+c` not `ctrl+z` as z does not release port.
- Mandatory to use absolute aiqc imports, not relative: `aiqc.orm` not `..orm`.
- Homepage '/': see experiments.py `register_page.path` and `def fetch_links` below

- "External css/js files are loaded before the `/assets`."
- "CSS/JS files in `/assets` are auto served." Don't need to be added as externals.
- BOOTSTRAP points to remote cdn: https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css
"""
sheets    = [dbc.themes.BOOTSTRAP]
app       = Dash(
    __name__
    , external_stylesheets         = sheets
    , update_title                 = '♻️'
    , title                        = 'AIQC'
    # Mandatory when using components that are generated by other callbacks
    , suppress_callback_exceptions = True
    , use_pages                    = True
)

"""
Grid system Div(Row(Col(Div)))
dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
"""
app.layout = html.Div(
    [
        # URL
        dcc.Location(id='url'),
        # Navbar
        html.Div(
            [
                # Logo
                html.Div(
                    html.A(
                        html.Img(src='assets/logo_wide_small.svg', height='35px'),
                        href='https://aiqc.io',
                    ),
                    className='logo'
                ),
                # Links
                html.Div(className='all-linx', id='all-linx'),
            ],
            className='navig'
        ),
        # Multi-page content
        page_container
    ],
    className='app-layout'
)

"""
- Populates the links
- Keeps an underline beneath the active link
"""
@app.callback(
    Output(component_id='all-linx', component_property='children'),
    Input(component_id='url', component_property='pathname')
)
def fetch_styledlinks(pathname:str):
    linx = []
    for page in page_registry.values():
        # Workaround for Experiments as home page
        if (pathname=='/'): pathname = '/experiments'

        page_name = page['name']
        match = pathname.endswith(page_name.lower())
        if not match:
            className = "linx"
        else:
            className = "linx linx-live"

        linx_box = html.Div(
            dcc.Link(
                page_name,
                href=page['relative_path'], 
                className=className
            ),
            className='linx-box'
        )
        linx.append(linx_box)
    return linx



if __name__ == '__main__':
    app.run_server(debug=True, port='9992')
