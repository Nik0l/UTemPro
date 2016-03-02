__author__ = 'root'

from bokeh.models import (
    TapTool, CustomJS)
from bokeh.io import output_file, show
from bokeh.io import curdoc, vform, gridplot, output_server
import ClusteringSourceData as csd
import GUIparams as gui
import GUICallbacks as cb


output_server("clusteringGUI")

def plotClusters(source, p):
    color = ['red', 'red', 'green', 'blue', 'blue', 'red']
    p.circle('x','y', source=source, color=color, size=source.data['size'], fill_alpha=0.2 )
    p.square('x','y', source=source, size=source.data['tmedian'], color="#74ADD1", fill_alpha=0.2)
    p.triangle('x','y', source=source, size=source.data['sd'], color="#111DFF", fill_alpha=0.4)
    #print source.data['dates']
    #output_file("clusteringGUI.html", title="clusterplot.py example")

def UpdatePlot(source, source1):
    data_table.source=source1
    plotClusters(source, p)
    #set callbacks
    #sliders[0].callback = cb.callbackMin(source)
    #sliders[1].callback = cb.callbackMax(source)
    #taptool.callback = cb.callbackTap(source)

    curdoc().add(vbox)
    #session = push_session(curdoc())
    #session.show(vbox)
    show(curdoc())

#define the graphical elements
dropdown = gui.getDropdown()
sliders = gui.getSliders()
data_table = gui.getDataTable()
p = gui.getFigure()
taptool = p.select(type=TapTool)
#load the data
vbox = gui.groupEverything(sliders, dropdown, data_table)


source = csd.getSource()
source1 = csd.getSource1()
#fill the data
UpdatePlot(source, source1)

