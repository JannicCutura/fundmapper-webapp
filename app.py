from flask import Flask, render_template
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models.callbacks import CustomJS

app = Flask(__name__)


@app.route('/')
def index():
    #genre_list = ['All', 'Comedy', 'Sci-Fi', 'Action', 'Drama', 'War', 'Crime', 'Romance', 'Thriller', 'Music',
    #              'Adventure', 'History', 'Fantasy', 'Documentary', 'Horror', 'Mystery', 'Family', 'Animation',
    #              'Biography', 'Sport', 'Western', 'Short', 'Musical']
    #
    #controls = {
    #    #"reviews": Slider(title="Min # of reviews", value=10, start=10, end=200000, step=10),
    #    "min_year": Slider(title="Start Year", start=1970, end=2021, value=1970, step=1),
    #    "max_year": Slider(title="End Year", start=1970, end=2021, value=2021, step=1),
    #    "genre": Select(title="Genre", value="All", options=genre_list)
    #}

    source_list = ['All','g1','g2']
    country_list = ['All','DE','FR','ES']

    controls = {
        "source": Select(title="Source", value="All", options=source_list),
        "country": Select(title="Country", value="All", options=country_list)
    }

    controls_array = controls.values()

    def selected_data():
        res = [
            {'imdbid': 'tt0099878', 'title': 'Jetsons: The Movie', 'genre': 'Animation, Comedy, Family', 'released': '07/06/1990', 'imdbrating': 5.4, 'imdbvotes': 2731, 'country': 'USA', 'numericrating': 4.3, 'usermeter': 46},
            {'imdbid': 'tt0099892', 'title': 'Joe Versus the Volcano', 'genre': 'Comedy, Romance', 'released': '03/09/1990', 'imdbrating': 5.6, 'imdbvotes': 23680, 'country': 'USA', 'numericrating': 5.2, 'usermeter': 54},
            {'imdbid': 'tt0099938', 'title': 'Kindergarten Cop', 'genre': 'Action, Comedy, Crime', 'released': '12/21/1990', 'imdbrating': 5.9, 'imdbvotes': 83461, 'country': 'USA', 'numericrating': 5.1, 'usermeter': 51},
            {'imdbid': 'tt0099939', 'title': 'King of New York', 'genre': 'Crime, Thriller', 'released': '09/28/1990', 'imdbrating': 7, 'imdbvotes': 19031, 'country': 'Italy, USA, UK', 'numericrating': 6.1, 'usermeter': 79},
            {'imdbid': 'tt0099951', 'title': 'The Krays', 'genre': 'Biography, Crime, Drama', 'released': '11/09/1990', 'imdbrating': 6.7, 'imdbvotes': 4247, 'country': 'UK', 'numericrating': 6.4, 'usermeter': 82}
        ]

        res = [
            {'date':201001, 'country':'DE', 'amnt':3000, 'source':'g1'},
            {'date':201001, 'country':'FR', 'amnt':4000, 'source':'g1'},
            {'date':201001, 'country':'ES', 'amnt':5000, 'source':'g1'},
            {'date':201002, 'country':'DE', 'amnt':3500, 'source':'g1'},
            {'date':201002, 'country':'FR', 'amnt':4400, 'source':'g1'},
            {'date':201002, 'country':'ES', 'amnt':4300, 'source':'g1'},
            {'date':201001, 'country':'DE', 'amnt':3500, 'source':'g2'},
            {'date':201001, 'country':'FR', 'amnt':4900, 'source':'g2'},
            {'date':201001, 'country':'ES', 'amnt':5200, 'source':'g2'},
            {'date':201002, 'country':'DE', 'amnt':3800, 'source':'g2'},
            {'date':201002, 'country':'FR', 'amnt':4100, 'source':'g2'},
            {'date':201002, 'country':'ES', 'amnt':4900, 'source':'g2'},
        ]
        return res

    source = ColumnDataSource()

    callback = CustomJS(args=dict(source=source, controls=controls), code="""
        if (!window.full_data_save) {
            window.full_data_save = JSON.parse(JSON.stringify(source.data));
        }
        var full_data = window.full_data_save;
        var full_data_length = full_data.x.length;
        var new_data = { x: [], y: [], color: [], country: [], source: [] }
        for (var i = 0; i < full_data_length; i++) {
            if (full_data.country[i] === null || full_data.date[i] === null || full_data.source[i] === null || full_data.amnt[i] === null)
                continue;
            if (
                (controls.country.value === 'All' || full_data.country[i].split(",").some(ele => ele.trim() === controls.country.value)) &&
                (controls.source.value === 'All' || full_data.source[i].split(",").some(ele => ele.trim() === controls.source.value))
            ) {
                Object.keys(new_data).forEach(key => new_data[key].push(full_data[key][i]));
            }
        }

        source.data = new_data;
        source.change.emit();
    """)

    fig = figure(plot_height=450, plot_width=720, tooltips=[("Country", "@country"), ("Source", "@source")])
    fig.circle(x="x", y="y", source=source, size=5, color="color", line_color=None)
    fig.xaxis.axis_label = "Date"
    fig.yaxis.axis_label = "MMF investments by country in bn USD"

    mmf_data = selected_data()

    source.data = dict(
        x=[d['date'] for d in mmf_data],
        y=[d['amnt'] for d in mmf_data],
        color=["#FF9900" for d in mmf_data],
        country=[d['country'] for d in mmf_data],
        source=[d['source'] for d in mmf_data]
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
    app.run(debug=True)
