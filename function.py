from bokeh.models import HoverTool, BoxSelectTool,Legend
from bokeh.embed import components
from bokeh.palettes import viridis,inferno,magma,brewer,d3
from bokeh.resources import CDN
from bokeh.embed import components
import numpy as np
import os
from scipy.ndimage.filters import gaussian_filter
from skimage.feature import blob_log
import colorcet as cc
from bokeh.plotting import figure
from bokeh.io import show

from bokeh.palettes import Viridis3, Viridis256,brewer
from bokeh.models import LogColorMapper,LinearColorMapper,ColorBar,LogTicker,ColorMapper
TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,hover,save"


head = """
<link rel="stylesheet"
 href="https://cdn.pydata.org/bokeh/release/bokeh-0.12.4.min.css"
 type="text/css" />
<script type="text/javascript"
 src="https://cdn.pydata.org/bokeh/release/bokeh-0.12.4.min.js">
</script>
<script type="text/javascript">
Bokeh.set_log_level("info");
</script>
"""


def GDP_PCA_plot(filename=None,threshold=0.025):
    data = np.load('uploads/'+filename)


    image1=data.f.image#-np.median(data.f.image)
    image2=np.array(image1*255/image1.max(),dtype='uint8')
    #H1=cv2.GaussianBlur(image2,(3,3),1.0*np.std(image2))
    H1 = gaussian_filter(image2,0.08*np.std(image2), mode='constant')
    blobs_log = blob_log(H1, max_sigma=0.3*np.std(H1), num_sigma=10, threshold=threshold)
    blobs_log[:, 2] = blobs_log[:, 2] * np.sqrt(2)
    blobs=blobs_log[blobs_log[:,2]>3.0]
    xx=(data.f.X.min(),np.round(data.f.X.max(),-1))
    yy=(data.f.Y.min(),np.round(data.f.Y.max(),-1))
    x_step=(xx[1]-xx[0])/np.shape(H1)[0]
    y_step=(yy[1]-yy[0])/np.shape(H1)[1]
    total=len(blobs)
    per_nv=round(len(blobs)/float(xx[1]-xx[0]),2)
    t=[filename+' : Original Density Plot','Gaussian Filtered Density Plot','Total NVs = '+str(total)+'  , NVs per Pixel square = '+str(per_nv)]

    data_list=[image1,H1,H1]
    color_list=[Viridis256,cc.b_linear_bgy_10_95_c74,cc.b_linear_bgy_10_95_c74]
    return_list=[]
    return_list.append(head)

    for i in range(3):
        color_mapper = LogColorMapper(palette=color_list[i], \
                              low=np.median(data_list[i]), \
                              high=1.0*np.mean(data_list[i])+\
                              3.0*np.std(data_list[i]))


        color_bar = ColorBar(color_mapper=color_mapper,\
                              label_standoff=12, \
                              border_line_color=None, \
                              location=(0,0))


        p1 = figure(plot_width=600, plot_height=600,title=t[i],\
                    x_range=xx,y_range=xx,tools=TOOLS,toolbar_location="below",toolbar_sticky=False,responsive=True)
        p1.image(image=[data_list[i]],color_mapper=color_mapper,
                    dh=yy[1]-yy[0], dw=xx[1]-xx[0], x=xx[0], y=xx[0])
        p1.add_layout(color_bar, 'right')
        if i == 2:
            p1.circle(blobs[:,1]*x_step+xx[0], blobs[:,0]*y_step+yy[0], size=blobs[:,2]*4, line_color='red',alpha=1.0, line_width=3,fill_color=None)

        p1.title.text_font_size = '20pt'
        p1.xaxis.axis_label_text_font_size = "14pt"
        p1.yaxis.axis_label_text_font_size = "14pt"







        #plots = {'Navy': p1, 'Blue': p2};
        tuple_plot = components(p1);
        #script2, div2 = components(p2);


        return_list.append(list(tuple_plot))


    return return_list