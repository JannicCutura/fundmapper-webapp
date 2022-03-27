from flask import Flask, render_template
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models.callbacks import CustomJS
from datetime import datetime, timedelta
import pandas as pd
from utils.get_data import get_data, format_data
app = Flask(__name__)



@app.route('/')
def index():
    investment_type_list = ['All','Asset Backed Commercial Paper', 'Certificate of Deposit',
       'Financial Company Commercial Paper', 'Government Agency Debt',
       'Repurchase Agreement', 'Insurance Company Funding Agreement',
       'Investment Company', 'Other Commercial Paper', 'Other Instrument',
       'Other Municipal Debt', 'Other Note', 'Treasury Debt',
       'Variable Rate Demand Note',
       'Non-Financial Company Commercial Paper',
       'Non-Negotiable Time Deposit',
       'Other Asset Backed Securities', 'Other Municipal Security',
       'Tender Option Bond']
    fund_type_list = ['All','Government/Agency', 'Other Tax Exempt Fund', 'Prime',
       'Single State Fund', 'Treasury', 'Other']

    controls = {
        "investment_category": Select(title="Investment category", value="All", options=investment_type_list),
        "fund_type": Select(title="Fund type", value="All", options=fund_type_list)
    }

    controls_array = controls.values()



    source = ColumnDataSource()

    callback = CustomJS(args=dict(source=source, controls=controls), code="""
        if (!window.full_data_save) {
            window.full_data_save = JSON.parse(JSON.stringify(source.data));
        }
        
        var full_data = window.full_data_save;
        var full_data_length = full_data.x.length;
        
        var new_data = { x: [], y: [], color: [], fund_type: [], investment_type: [] }
        
        for (var i = 0; i < full_data_length; i++) {
            if (
                (controls.fund_type.value === 'All' ||
                 String(full_data.fund_type[i]) === controls.fund_type.value)
                  &&
                (controls.investment_type.value === 'All' ||
                 String(full_data.investment_type[i]) === controls.investment_type.value))
            ) {

                Object.keys(new_data).forEach(key => new_data[key].push(full_data[key][i]));
            }
        }

        source.data = new_data;
        source.change.emit();
        
    """)

    fig = figure(plot_height=450, plot_width=720, x_axis_type='datetime',
                 tooltips=[("Fund type", "@fund_type"), ("Investment category", "@investment_type")],
                 title="US MMF investments")
    fig.circle(x="x", y="y", source=source, size=5, color="color", line_color=None)

    fig.xaxis.axis_label = "Date"
    fig.yaxis.axis_label = "MMF investments by country in bn USD"

    #fig.y_range.start = 0
    #fig.x_range.range_padding = 0.1
    #fig.xgrid.grid_line_color = None
    #fig.axis.minor_tick_line_color = None
    #fig.outline_line_color = None
    #fig.legend.location = "top_left"
    #fig.legend.orientation = "horizontal"

    mmf_data = format_data(get_data())

    source.data = dict(
        x=[d['date'] for d in mmf_data],
        y=[d['sum_amount'] for d in mmf_data],
        color=[d['color'] for d in mmf_data],
        fund_type=[d['investmenttypedomain'] for d in mmf_data],
        investment_type=[d['type']for d in mmf_data]
        )

    for single_control in controls_array:
        single_control.js_on_change('value', callback)

    inputs_column = column(*controls_array, width=320, height=1000)
    layout_row = row([inputs_column, fig])

    script, div = components(layout_row)
    return render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)












