__author__ = 'root'
import numpy as np
import matplotlib.pyplot as plt, mpld3
from bokeh.plotting import figure
from bokeh.models import (
    GMapOptions, GMapPlot, ColumnDataSource, PanTool, WheelZoomTool, Circle, Range1d)
from bokeh.io import output_file, show


def plotGraph(aapl, aapl_dates):

    window_size = 100
    window = np.ones(window_size)/float(window_size)
    aapl_avg = np.convolve(aapl, window, 'same')

    # output to static HTML file
    output_file("stocks.html", title="stocks.py example")

    # create a new plot with a a datetime axis type
    p = figure(width=1000, height=600, x_axis_type="datetime")

    # add renderers
    p.circle(aapl_dates, aapl, size=3, color='darkgrey', alpha=0.8, legend='close')
    p.line(aapl_dates, aapl_avg, color='navy', legend='avg')

    # NEW: customize by setting attributes
    p.title = "Response time in seconds"
    p.legend.orientation = "top_left"
    p.grid.grid_line_alpha=0
    p.xaxis.axis_label = 'Seconds'
    p.yaxis.axis_label = 'Latitude'
    p.ygrid.band_fill_color="olive"
    p.ygrid.band_fill_alpha = 0.1

    # show the results
    show(p)

def plotMap(data):
    # output to static HTML file
    output_file("map.html", title="map example")
    p = GMapPlot(
        x_range=Range1d(-160, 160), y_range=Range1d(-80, 80),
        plot_width=1000,plot_height=500,
        map_options=GMapOptions(lat=42.55, lng=1.533, zoom=2),
        title="Cities with more than 5,000 people",
        webgl=True, responsive=True)
    print data
    circle = Circle(x="lng", y="lat", size=5, line_color=None, fill_color='firebrick', fill_alpha=0.3)
    #circle = Circle(x="LON", y="LAT", size=5, line_color=None, fill_color='firebrick', fill_alpha=0.3)
    #print ColumnDataSource(data)
    p.add_glyph(ColumnDataSource(data), circle)
    #p.add_tools(PanTool(), WheelZoomTool())
    show(p)

def drawScatterPlot():
    fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
    N = 100

    scatter = ax.scatter(np.random.normal(size=N),
                     np.random.normal(size=N),
                     c=np.random.random(size=N),
                     s=1000 * np.random.random(size=N),
                     alpha=0.3,
                     cmap=plt.cm.jet)
    ax.grid(color='white', linestyle='solid')

    ax.set_title("Scatter Plot", size=20)

    labels = ['point {0}'.format(i + 1) for i in range(N)]
    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
    mpld3.plugins.connect(fig, tooltip)
    mpld3.show()

#drawScatterPlot()

