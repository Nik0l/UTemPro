__author__ = 'root'
from bokeh.models import CustomJS

def callbackTap(source):
    callback_tap = CustomJS(args=dict(source=source), code="""
        var data = source.get('data');
        var num_clusters = 5;
        var inds = cb_obj.get('selected')['1d'].indices;
        data['cluster']=inds
        if (inds >= 0) {
            window.alert("questions: " + data['size'][inds]);
            for (i = 0; i < data['downloads'].length; i++) {
                data['downloads'][i] = 5
            }
        }
        source.trigger('change');
    """)
    return callback_tap

def callbackMin(source):
    callback_min = CustomJS(args=dict(source=source), code="""
        var data = source.get('data');
        var f = cb_obj.get('value')
        min = f
        x = data['x']
        y = data['y']
        size = data['size']
        size_init = data['size_init']
        for (i = 0; i < size.length; i++) {
            if (size_init[i] < min || size_init[i] > max) {
                size[i] = 0
            }
            else {
                size[i] = size_init[i]
            }
        }
        source.trigger('change');
    """)
    return callback_min

def callbackMax(source):
    callback_max = CustomJS(args=dict(source=source), code="""
        var data = source.get('data');
        var f = cb_obj.get('value')
        max = f
        x = data['x']
        y = data['y']
        size = data['size']
        size_init = data['size_init']
        for (i = 0; i < size.length; i++) {
            if (size_init[i] > max || size_init[i] < min) {
                size[i] = 0
            }
            else {
                size[i] = size_init[i]
            }
        }
        source.trigger('change');
    """)
    return callback_max
