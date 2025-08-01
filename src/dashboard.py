import dash
from dash import html, dcc, Input, Output, State, ctx
import pandas as pd
from sqlalchemy import create_engine, text
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print(result.fetchone())

app = dash.Dash(__name__)
app.title = "New Grad Job Dashboard"
app.config.suppress_callback_exceptions = True

def load_data():
    with engine.connect() as conn:
        df = pd.read_sql(text("SELECT * FROM jobs"), con=conn)
        # Sort by date_posted in descending order (newest first)
        df = df.sort_values('date_posted', ascending=False)
        return df

app.layout = html.Div([
    html.H1("New Grad Software Engineering Jobs"),

    dcc.Dropdown(id="company-filter", placeholder="Filter by company"),
    dcc.Dropdown(id="location-filter", placeholder="Filter by location"),
    dcc.Store(id="page-store", data=1),
    html.Div(id="table-output"),
    html.Div(id="pagination-buttons", style={"margin": "20px 0"}),
    html.Div([
        dcc.Input(id="page-jump-input", type="number", min=1, step=1, placeholder="Page #", style={"width": "80px"}),
        html.Button("Go", id="page-jump-btn", n_clicks=0, style={"marginLeft": "8px"})
    ], style={"marginBottom": "20px"}),
    dcc.Graph(id="job-trend")
])

@app.callback(
    [Output("company-filter", "options"),
     Output("location-filter", "options")],
    Input("company-filter", "value")  # Dummy input to trigger on load
)
def populate_dropdowns(_):
    df = load_data()
    companies = sorted(df["company"].dropna().unique())
    locations = sorted(df["location"].dropna().unique())
    return (
        [{"label": c, "value": c} for c in companies],
        [{"label": l, "value": l} for l in locations]
    )

@app.callback(
    [Output("table-output", "children"),
     Output("pagination-buttons", "children"),
     Output("job-trend", "figure"),
     Output("page-store", "data"),
     Output("page-jump-input", "value")],
    [Input("company-filter", "value"),
     Input("location-filter", "value"),
     Input({"type": "page-btn", "index": dash.ALL}, "n_clicks"),
     Input("page-jump-btn", "n_clicks")],
    [State("page-store", "data"),
     State("page-jump-input", "value")]
)
def update_dashboard(company, location, page_btn_clicks, jump_n_clicks, current_page, jump_value):
    df = load_data()
    if company:
        df = df[df["company"] == company]
    if location:
        df = df[df["location"] == location]

    columns_to_display = ["title", "company", "location", "date_posted", "url", "source"]

    # Pagination logic
    jobs_per_page = 20
    total_jobs = len(df)
    num_pages = max(1, (total_jobs + jobs_per_page - 1) // jobs_per_page)

    # Determine which page to show
    triggered = ctx.triggered_id
    page = current_page if current_page and 1 <= current_page <= num_pages else 1
    if isinstance(triggered, dict) and triggered.get("type") == "page-btn":
        page = triggered["index"]
    elif triggered == "page-jump-btn" and jump_value:
        try:
            page = int(jump_value)
            if page < 1:
                page = 1
            elif page > num_pages:
                page = num_pages
        except Exception:
            page = 1

    start_idx = (page - 1) * jobs_per_page
    end_idx = start_idx + jobs_per_page
    df_page = df.iloc[start_idx:end_idx]

    table = html.Table([
        html.Tr([html.Th(col) for col in ["Title", "Company", "Location", "Date Posted", "Url", "Source"]])
    ] + [
        html.Tr([
            html.Td(
                html.A(
                    html.Button("Apply", n_clicks=0),
                    href=row["url"],
                    target="_blank"
                )
            ) if col == "url" else html.Td(row[col])
            for col in columns_to_display
        ])
        for _, row in df_page.iterrows()
    ])

    # Show page buttons with ellipses and always include last page at the end
    if num_pages > 1:
        buttons = []
        if num_pages <= 6:
            page_range = list(range(1, num_pages + 1))
            for i in page_range:
                buttons.append(html.Button(
                    str(i),
                    id={"type": "page-btn", "index": i},
                    n_clicks=0,
                    style={
                        "margin": "0 2px",
                        "backgroundColor": "#007bff" if i == page else "#f0f0f0",
                        "color": "white" if i == page else "black"
                    }
                ))
        else:
            # Always show first page
            buttons.append(html.Button(
                "1",
                id={"type": "page-btn", "index": 1},
                n_clicks=0,
                style={
                    "margin": "0 2px",
                    "backgroundColor": "#007bff" if page == 1 else "#f0f0f0",
                    "color": "white" if page == 1 else "black"
                }
            ))
            if page <= 4:
                # Show first 5 pages, then ellipsis, then last
                for i in range(2, 6):
                    buttons.append(html.Button(
                        str(i),
                        id={"type": "page-btn", "index": i},
                        n_clicks=0,
                        style={
                            "margin": "0 2px",
                            "backgroundColor": "#007bff" if i == page else "#f0f0f0",
                            "color": "white" if i == page else "black"
                        }
                    ))
                buttons.append(html.Span('...', style={"margin": "0 6px"}))
            elif page >= num_pages - 3:
                # Show first, ellipsis, then last 5 pages
                buttons.append(html.Span('...', style={"margin": "0 6px"}))
                for i in range(num_pages - 4, num_pages):
                    buttons.append(html.Button(
                        str(i),
                        id={"type": "page-btn", "index": i},
                        n_clicks=0,
                        style={
                            "margin": "0 2px",
                            "backgroundColor": "#007bff" if i == page else "#f0f0f0",
                            "color": "white" if i == page else "black"
                        }
                    ))
            else:
                # Show first, ellipsis, 2 before/after current, ellipsis, last
                buttons.append(html.Span('...', style={"margin": "0 6px"}))
                for i in range(page - 1, page + 2):
                    buttons.append(html.Button(
                        str(i),
                        id={"type": "page-btn", "index": i},
                        n_clicks=0,
                        style={
                            "margin": "0 2px",
                            "backgroundColor": "#007bff" if i == page else "#f0f0f0",
                            "color": "white" if i == page else "black"
                        }
                    ))
                buttons.append(html.Span('...', style={"margin": "0 6px"}))
            # Always show last page
            buttons.append(html.Button(
                str(num_pages),
                id={"type": "page-btn", "index": num_pages},
                n_clicks=0,
                style={
                    "margin": "0 2px",
                    "backgroundColor": "#007bff" if page == num_pages else "#f0f0f0",
                    "color": "white" if page == num_pages else "black"
                }
            ))
    else:
        buttons = []

    trend = df["date_posted"].value_counts().sort_index()
    figure = {
        "data": [{"x": trend.index, "y": trend.values, "type": "bar"}],
        "layout": {"title": "Jobs Posted Over Time"}
    }

    # Reset the input box after jump
    return table, buttons, figure, page, None

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8050))
    print(f"Starting dashboard on port {port}")
    print(f"Debug mode: False")
    print(f"Host: 0.0.0.0")
    app.run(debug=False, host="0.0.0.0", port=port)
