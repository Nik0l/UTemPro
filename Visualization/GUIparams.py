__author__ = 'root'
from bokeh.models import HoverTool, WheelZoomTool, HoverTool, PanTool
from bokeh.models.widgets import DateFormatter, TableColumn
from bokeh.models.widgets import Slider, Dropdown, HBox, VBox, VBoxForm, DataTable
from bokeh.plotting import figure

def getHover():
    hover = HoverTool(
        tooltips=[
            ("Questions", "@size"),
            ("tmean, min", "@tmean"),
            ("tmedian, min", "@tmedian"),
            ("sd, min", "@sd"),
        ]
    )
    return hover

def getColumns():
    columns = [
        TableColumn(field="dates", title="QuestionID", formatter=DateFormatter()),
        TableColumn(field="downloads", title="UserID"),
        TableColumn(field="Asked", title="Asked"),
        TableColumn(field="title", title="Title"),
        TableColumn(field="body", title="Body"),
        TableColumn(field="Asked", title="Asked"),
        TableColumn(field="title", title="Title"),
        TableColumn(field="body", title="Body"),
    ]
    return columns

def getSliders():
    q_min = Slider(start=0, end=100, value=0, step=20, title="Min questions")
    q_max = Slider(start=0, end=100, value=100, step=20, title="Max questions")
    t_min = Slider(start=0, end=100, value=0, step=20, title="Min med time")
    t_max = Slider(start=0, end=100, value=100, step=20, title="Max med time")
    tm_min = Slider(start=0, end=100, value=0, step=20, title="Min mean time")
    tm_max = Slider(start=0, end=100, value=100, step=20, title="Max mean time")
    sd_min = Slider(start=0, end=100, value=0, step=20, title="Min SD of time")
    sd_max = Slider(start=0, end=100, value=100, step=20, title="Max SD of time")
    sliders = [q_min, q_max, t_min, t_max, tm_min, tm_max, sd_min, sd_max]
    return sliders

def getDropdown():
    menu = [("Clustering 1", "item_1"), ("Clustering 2", "item_2"), None, ("Clustering 3", "item_3")]
    dropdown = Dropdown(label="Choose clustering to explore", type="warning", menu=menu)
    return dropdown

def groupSliders(sliders):
    hbox_q = HBox(children=[sliders[0], sliders[1]])
    hbox_t = HBox(children=[sliders[2], sliders[3]])
    hbox_tm = HBox(children=[sliders[4], sliders[5]])
    hbox_sd = HBox(children=[sliders[6], sliders[7]])
    hboxes = [hbox_q, hbox_t, hbox_tm, hbox_sd]
    return hboxes

def groupEverything(sliders, dropdown, data_table):
    hboxes = groupSliders(sliders)
    inputs = VBox(children=[dropdown, hboxes[0], hboxes[1], hboxes[2], hboxes[3]], width=100, height=60)
    #hbox = HBox(children=[inputs, p])
    vbox = VBoxForm(children=[inputs, data_table])
    return vbox

def getDataTable():
    data_table = DataTable(columns=getColumns(), height=380)
    return data_table

def getFigure():
    p = figure(plot_width=1100, plot_height=600,
            title = "Clusters of questions", tools = ["tap", getHover(), WheelZoomTool(), PanTool()])
    #p.xaxis.axis_label = 'X1'
    #p.yaxis.axis_label = 'X2'
    return p
