from bokeh.plotting import figure, show
from bokeh.embed import file_html
from bokeh.models import Legend, HoverTool ,ColumnDataSource, Range1d, FactorRange
from bokeh.resources import CDN
from bokeh.transform import factor_cmap
from bokeh.palettes import magma, Turbo256, Category20
import pandas as pd
from datetime import timedelta, datetime
from math import pi
from resources import create_keyword_ranking_df, string_word_ranking
import datetime as dt


class DataPlotter:

    def __init__(self, raw_dataframe):
        self.raw_dataframe = raw_dataframe
        self.np_palette_dict = {'pagina12': '#000000', 'infobae': '#f27b1a', 'minutouno': '#ba141f', 'tn': '#1475eb',
                                'ellitoral': '#2a4c88'}
        self.kw_ranking_df = []
        self.format_raw_dataframe()
        self.newspapers = self.raw_dataframe['Newspaper'].unique().tolist()

    def format_raw_dataframe(self):
        """ Formats DF to show Buenos Aires time (GMT -3)
            Forces Datetime column to Datetime time
            Sets Headlines as type string
            Creates new column with floored datetime to nearest hour
        """
        # Reset index
        self.raw_dataframe = self.raw_dataframe.reset_index(drop=True)
        # Convert Datetime column into datetime object
        self.raw_dataframe['Datetime'] = pd.to_datetime((self.raw_dataframe['Datetime']), dayfirst=True)
        # Convert UTC (AWS Servers) time to Buenos Aires time
        self.raw_dataframe['Datetime'] = self.raw_dataframe['Datetime'] + timedelta(hours=-3)
        # Create new column with rounding datetime to nearest hour
        self.raw_dataframe['floored_datetime'] = self.raw_dataframe['Datetime'].dt.round('H')
        # Force headlines to string type
        self.raw_dataframe['Headline'] = self.raw_dataframe['Headline'].astype(str)

    def create_kw_freq_bar_graphs(self, start_date=0, end_date=0, freq_threshold=3):
        """
        Creates a keyword frequency bar graph from dataframe and exports it in html with name of newspaper and creation
        timestamp
        Default keyword frequency threshold set at 3
        Can select time scope with start_date and end_date variables, if not set defaults to include all given data
        """
        # Slicing Dataframe to begin at start_date
        if start_date == 0:
            start_date = self.raw_dataframe['Datetime'].min()
        else:
            start_date = start_date
        raw_dataframe = self.raw_dataframe[self.raw_dataframe['Datetime'] >= start_date]
        # Slicing Dataframe to end at end_date
        if end_date == 0:
            end_date = raw_dataframe['Datetime'].min()
        else:
            end_date = end_date
        raw_dataframe = raw_dataframe[raw_dataframe['Datetime'] <= end_date]

        for np_name in self.newspapers:
            df = create_keyword_ranking_df(raw_dataframe[raw_dataframe['Newspaper'] == np_name], freq_threshold)
            # Creating figure
            p1 = figure(title=f'Keyword ranking {np_name}', x_range=df['keyword'], width=1000, height=300,
                        sizing_mode='scale_width')

            # Setting axis names and properties
            p1.xaxis.major_label_orientation = 4 / 3
            p1.yaxis.axis_label = 'Frequency'
            p1.xaxis.axis_label = 'Keyword'
            p1.xaxis.axis_label_text_font_size = '18pt'
            palette = magma(len(df))
            # Creating bar elements
            p1.vbar(x=df['keyword'], top=df['frequency'], width=0.5,
                    fill_color=palette, line_color='black')

            # Adding hover tools
            p1.add_tools(HoverTool(
                tooltips=[
                    ('Count', '@top{0}')
                ]))

            # Setting file name and path
            filename = f'Kw_freq_{np_name.lower()}_{start_date}_to_{end_date}.html'
            path = 'html_graphs/' + filename
            html = file_html(p1, CDN, f'{np_name.lower()} Keyword frequency - {start_date} - {end_date}')
            with open(path, 'w+') as file:
                file.write(html)
            print(f'{filename} succesfully created')

    def create_uq_headlines_html_line_plot(self, start_date_zoom=0, end_date_zoom=0):
        """
            Creates a html Bokeh plot with al the information contained in the datafreame.
            You can set the initial zoom with:
                - start_date_zoom: datetime[64]
                - end_date zoom: datetime[64]
            If initial start or end zoom not selected it will default to include all data in intial zoom
        """
        # Grouping DF
        dataframe = self.raw_dataframe.groupby(["Newspaper", 'floored_datetime']).count().reset_index()

        # Creating figure
        p1 = figure(title='Unique amount of headlines by hour', x_axis_type='datetime', width=1000, height=300,
                    sizing_mode='scale_width')
        # Setting Y axis labels
        p1.yaxis.axis_label = '# of headlines'
        # Setting X axis labels
        p1.xaxis.axis_label = 'Date and time'
        # Creating line glyphs with for loop
        for np in self.newspapers:
            p1.line(self.raw_dataframe[self.raw_dataframe['Newspaper'] == np]['floored_datetime'],
                    self.raw_dataframe[self.raw_dataframe['Newspaper'] == np]['Headline'],
                    line_width=2, legend_label=str(np.title()), color=self.np_palette_dict.get(np))

        # Adding hover tools and giving format to text
        p1.add_tools(HoverTool(tooltips=[('Date', '@x{%F}'), ("Headlines count", '$y{0}')], formatters={'@x': 'datetime'}))

        # Setting custom initial view zoom

        if start_date_zoom == 0:
            timestamp_start = dataframe['floored_datetime'].min()
        else:
            timestamp_start = (start_date_zoom - datetime(1970, 1, 1)) / timedelta(seconds=1)
        p1.x_range.start = int(timestamp_start) * 1e3  # Multiply by 1e3 as JS timestamp is in milliseconds

        if end_date_zoom == 0:
            timestamp_end = dataframe['floored_datetime'].max()
        else:
            timestamp_end = (end_date_zoom - datetime(1970, 1, 1)) / timedelta(seconds=1)
        p1.x_range.end = int(timestamp_end) * 1e3  # Multiply by 1e3 as JS timestamp is in milliseconds

        # Setting legend behaviour on click
        p1.legend.click_policy = "hide"
        # Setting file name

        # Setting path
        path = 'html_graphs/'
        html = file_html(p1, CDN, path)
        time_range = str(start_date_zoom.strftime("%d_%m_%Y")) + '_to_' + str(end_date_zoom.strftime("%d_%m_%Y"))
        filename = f'unique_headline_counts_{time_range}.html'
        path = 'html_graphs/' + filename
        with open(path, 'w+') as file:
            file.write(html)
        print(f'{filename} succesfully created')

    def create_kw_app_ratio_comparison(self, top_words=20, kw_freq_threshold=3):
        # Creating empty DF
        merged_df = pd.DataFrame(columns=['keyword'])
        # Creating empty appearence ratio list
        app_ratio_list = []
        # Iterating for each newspaper in DF
        for np in self.newspapers:
            df = self.raw_dataframe[self.raw_dataframe['Newspaper'] == np].reset_index()
            df['newspaper'] = np
            # Why 20? Check to see if we can find a non-static way
            kw_rank_df = create_keyword_ranking_df(df, kw_freq_threshold)
            kw_rank_df[f'ratio_{np}'] = kw_rank_df['frequency'] / len(df)
            kw_rank_df[f'freq_{np}'] = kw_rank_df['frequency']
            kw_rank_df[f'%_{np}'] = round(kw_rank_df[f'ratio_{np}'] * 100, 2)
            kw_rank_df = kw_rank_df.drop(['frequency'], axis=1)
            app_ratio_list = app_ratio_list + list(kw_rank_df[f'%_{np}'])
            merged_df = merged_df.merge(kw_rank_df, on='keyword', how='outer').reset_index(drop=True)

        # Slicing Dataframe
        merged_df = merged_df[:top_words]

        app_ratio_list = app_ratio_list[:int(top_words*len(self.newspapers))]

        # Building dictionary to plot
        kw_np_tuples = [(keyword, newspaper) for keyword in list(merged_df['keyword']) for newspaper in self.newspapers]
        data_dict = dict(x=kw_np_tuples, y=app_ratio_list)

        # Creating color palette tuple
        np_palette_tup = tuple([self.np_palette_dict[np] for np in self.newspapers])

        # Setting source
        source = ColumnDataSource(data_dict)

        # Creating figure
        p = figure(x_range=FactorRange(*kw_np_tuples), width=1000, height=300, sizing_mode='scale_width',
                   title="Keyword appearence rate by newspaper",
                   toolbar_location=None, tools="")

        # Creating bar glyphs
        p.vbar(x='x', top='y', width=0.9, source=source,
               fill_color=factor_cmap('x', palette=np_palette_tup, factors=self.newspapers, start=1, end=2),
               line_color='black')

        # Adding hover tools
        p.add_tools(HoverTool(
            tooltips=[
                ("Rate", '@y{0.00}%')
            ]
        ))

        # Formatting plot
        p.y_range.start = 0
        p.x_range.range_padding = 0.05
        p.xaxis.major_label_orientation = 1
        p.xgrid.grid_line_color = None

        # Setting path
        path = 'html_graphs/'
        html = file_html(p, CDN, path)
        filename = f'kw_freq_comparative.html'
        path = 'html_graphs/' + filename

        # Saving html file
        with open(path, 'w+') as file:
            file.write(html)
        print(f'{filename} succesfully created')

    def create_keyword_frequency_html_plots(self, n_kwds_plot=5, plot_line=1, plot_scatter=1):
        """Creates an html with a line plot for each newspaper in the raw_dataframe.
            Glyphs to plot can be line, scatter or both controlled with the variables:
                - plot_line
                - plot_scatter
            Setted to 1 by default

        """
        # Gouping by Newspaper name, floored_datetime while concatenating all headlines for that our
        concatenated_headlines_df = self.raw_dataframe.groupby(['Newspaper', 'floored_datetime'])['Headline'].apply(
            ' '.join).reset_index()

        # Creating word ranking for string of concatenated df for each hour
        concatenated_headlines_df['keywords'] = [string_word_ranking(x) for x in concatenated_headlines_df['Headline']]

        # Creating a dictionary wof word and frequency for ease of searching
        concatenated_headlines_df['keywords_dict'] = [dict(x) for x in concatenated_headlines_df['keywords']]

        for np in self.newspapers:
            df = pd.DataFrame(concatenated_headlines_df[concatenated_headlines_df['Newspaper'] == np])
            df_top_kws = get_n_top_kwds(list(df['keywords']), 10)
            df = df[['Newspaper', 'floored_datetime', 'keywords_dict']]

            # Creating figure
            p1 = figure(title=f'Keyword ranking {np.title()}', x_axis_type='datetime', width=1000, height=300,
                        sizing_mode='scale_width')

            # Changing Y labels orientation
            p1.xaxis.major_label_orientation = pi / 3
            # Setting Y axis label
            p1.yaxis.axis_label = 'Frequency'
            # Setting X axis label
            p1.xaxis.axis_label = 'Date'

            # Creating n color palette
            if n_kwds_plot <= 20:
                palette = Category20.get(n_kwds_plot)
            else:
                palette = Turbo256

            # Creating glyphs
            for i in range(n_kwds_plot):
                # Plotting lines
                if plot_line:
                    p1.line(df['floored_datetime'],
                            [x.get(df_top_kws['word'][i], 0) for x in df['keywords_dict']],
                            line_width=3, legend_label=df_top_kws['word'][i], color=palette[i],
                            name=df_top_kws['word'][i].title())
                else:
                    pass
                # Plotting scatter dots
                if plot_scatter:
                    p1.scatter(df['floored_datetime'],
                               [x.get(df_top_kws['word'][i], 0) for x in df['keywords_dict']],
                               line_width=3, legend_label=df_top_kws['word'][i], color=palette[i],
                               name=df_top_kws['word'][i].title())
                else:
                    pass

            # Adding hover tools and formating hover results
            p1.add_tools(HoverTool(
                tooltips=[('Date', '@x{%F}'),
                          ("Appearences", '$y{0}'),
                          ('Keyword', '$name')],

                formatters={'@x': 'datetime'}
            ))

            # Setting label font size
            p1.legend.label_text_font_size = '12pt'

            # Setting legend policy on click
            p1.legend.click_policy = "hide"

            # Setting legend horientation
            p1.legend.orientation = "horizontal"

            # Creating nee legend object
            new_legend = p1.legend[0]

            # Adding new object to layout
            p1.add_layout(new_legend, 'below')

            # Setting file name
            filename = f'{dt.datetime.now().strftime("%Y_%m_%d_%H")}_hist_kw_freq_line_{np}.html'

            # Setting path
            path = 'html_graphs/'
            html = file_html(p1, CDN, path)
            path = 'html_graphs/' + filename

            # Saving html file
            with open(path, 'w+') as file:
                file.write(html)
            print(f'{filename} succesfully created')


def create_kw_freq_bar_graphs(raw_dataframe, start_date=0, end_date=0, freq_threshold=3):
    """
    Creates a keyword frequency bar graph from dataframe and exports it in html with name of newspaper and creation
    timestamp
    Default keyword frequency threshold set at 3
    Can select time scope with start_date and end_date variables, if not set defaults to include all given data
    """
    # Slicing Dataframe to begin at start_date
    if start_date == 0:
        start_date = raw_dataframe['Datetime'].min()
    else:
        start_date = start_date
    raw_dataframe = raw_dataframe[raw_dataframe['Datetime'] >= start_date]
    # Slicing Dataframe to end at end_date
    if end_date == 0:
        end_date = raw_dataframe['Datetime'].min()
    else:
        end_date = end_date
    raw_dataframe = raw_dataframe[raw_dataframe['Datetime'] <= end_date]

    newspapers = raw_dataframe['Newspaper'].unique().tolist()
    for np_name in newspapers:
        df = create_keyword_ranking_df(raw_dataframe[raw_dataframe['Newspaper'] == np_name], freq_threshold)
        # Creating figure
        p1 = figure(title=f'Keyword ranking {np_name}', x_range=df['keyword'], width=1000, height=300,
                    sizing_mode='scale_width')

        # Setting axis names and properties
        p1.xaxis.major_label_orientation = 4 / 3
        p1.yaxis.axis_label = 'Frequency'
        p1.xaxis.axis_label = 'Keyword'
        p1.xaxis.axis_label_text_font_size = '18pt'
        palette = magma(len(df))
        # Creating bar elements
        p1.vbar(x=df['keyword'], top=df['frequency'], width=0.5,
                fill_color=palette, line_color='black')

        # Adding hover tools
        p1.add_tools(HoverTool(
            tooltips=[
                ('Count', '@top{0}')
            ]))

        # Setting file name and path
        filename = f'Kw_freq_{np_name.lower()}_{start_date}_to_{end_date}.html'
        path = 'html_graphs/' + filename
        html = file_html(p1, CDN, 'kw_frequency_plot')
        with open(path, 'w+') as file:
            file.write(html)


def create_uq_headlines_html_line_plot(dataframe, start_date_zoom=0, end_date_zoom=0):
    """
        Creates a html Bokeh plot with al the information contained in the datafreame.
        You can set the initial zoom with:
            - start_date_zoom: datetime[64]
            - end_date zoom: datetime[64]
        If initial start or end zoom not selected it will default to include all data in intial zoom
    """
    # Convert Datetime column into datetime object
    dataframe['Datetime'] = pd.to_datetime((dataframe['Datetime']), dayfirst=True)
    # Convert UTC (AWS Servers) time to Buenos Aires time
    dataframe['Datetime'] = dataframe['Datetime'] + timedelta(hours=-3)
    # Create new column with rounding datetime to nearest hour
    dataframe['floored_datetime'] = dataframe['Datetime'].dt.round('H')
    # Grouping DF
    dataframe = dataframe.groupby(["Newspaper", 'floored_datetime']).count().reset_index()
    # Creating list of unique newspapers
    newspapers = dataframe['Newspaper'].unique().tolist()
    # Setting palette dictionary
    palette_dict = {'pagina12': '#000000', 'infobae': '#f27b1a'}
    # Creating figure
    p1 = figure(title='Unique amount of headlines by hour', x_axis_type='datetime', width=1000, height=300,
                sizing_mode='scale_width')
    # Setting Y axis labels
    p1.yaxis.axis_label = '# of headlines'
    # Setting X axis labels
    p1.xaxis.axis_label = 'Date and time'
    # Creating line glyphs with for loop
    for np in newspapers:
        p1.line(dataframe[dataframe['Newspaper'] == np]['floored_datetime'],
                dataframe[dataframe['Newspaper'] == np]['Headline'],
                line_width=2, legend_label=str(np.title()), color=palette_dict.get(np))

    # Adding hover tools and giving format to text
    p1.add_tools(HoverTool(tooltips=[('Date', '@x{%F}'), ("Headlines count", '$y{0}')], formatters={'@x': 'datetime'}))

    # Setting custom initial view zoom

    if start_date_zoom == 0:
        timestamp_start = dataframe['floored_datetime'].min()
    else:
        timestamp_start = (start_date_zoom - datetime(1970, 1, 1)) / timedelta(seconds=1)
    p1.x_range.start = int(timestamp_start) * 1e3  # Multiply by 1e3 as JS timestamp is in milliseconds

    if end_date_zoom == 0:
        timestamp_end = dataframe['floored_datetime'].max()
    else:
        timestamp_end = (end_date_zoom - datetime(1970, 1, 1)) / timedelta(seconds=1)
    p1.x_range.end = int(timestamp_end) * 1e3  # Multiply by 1e3 as JS timestamp is in milliseconds

    # Setting legend position

    # Setting legend behaviour on click
    p1.legend.click_policy = "hide"
    # Setting file name

    # Setting path
    path = 'html_graphs/'
    html = file_html(p1, CDN, path)
    time_range = str(start_date_zoom.strftime("%d_%m_%Y")) + '_to_' + str(end_date_zoom.strftime("%d_%m_%Y"))
    save_html_line_plot(html, time_range)


def save_html_line_plot(html, time_range):
    filename = f'unique_headline_counts_{time_range}.html'
    path = 'html_graphs/' + filename
    with open(path, 'w+') as file:
        file.write(html)


def get_n_top_kwds(kwd_freq_tuples_list, n):
    """ Gets  a list of lists of tuples with (keyword, frequency) and returns sorted a DataFrame of unique keywords
        with total appearence frequency
    """
    tops_kwds = [kwd_freq_tuples_list[y][:n] for y in range(len(kwd_freq_tuples_list))]
    top_kws_list = [item for sublist in tops_kwds for item in sublist]
    df_tkws = pd.DataFrame(top_kws_list,columns=['word','n_appearences'])
    df_tkws = df_tkws.groupby('word').sum().reset_index()
    df_tkws.sort_values('n_appearences', ascending=False, inplace=True)
    df_tkws = df_tkws.reset_index(drop=True)
    return df_tkws

