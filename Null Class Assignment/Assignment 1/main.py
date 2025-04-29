import pandas as pd 
import plotly.express as px 
import plotly.io as pio 
import webbrowser 
import os

data = pd.read_csv(r"C:\Users\Pc\Desktop\Null Class Assignment\Assignment 1\app_data1.csv")
df = pd.DataFrame(data)

paid_apps = df[df['App Type'] == 'Paid']

html_files_path = "./"
if not os.path.exists(html_files_path): 
    os.makedirs(html_files_path) 
plot_containers = ""
# Save each Plotly figure to an HTML file 
def save_plot_as_html(fig, filename, insight): 
    global plot_containers 
    filepath = os.path.join(html_files_path, filename) 
    html_content = pio.to_html(fig, full_html=False, include_plotlyjs='inline') 
    # Append the plot and its insight to plot_containers 
    plot_containers += f""" 
    <div class="plot-container" id="{filename}" onclick="openPlot('{filename}')"> 
        <div class="plot">{html_content}</div> 
        <div class="insights">{insight}</div> 
    </div> 
    """ 
    fig.write_html(filepath, full_html=False, include_plotlyjs='inline')

plot_width = 400 
plot_height = 300 
plot_bg_color = 'black' 
text_color = 'white' 
title_font = {'size':16} 
axis_font = {'size':12}

# Figure 
fig = px.scatter( 
    paid_apps, 
    x='Revenue', 
    y='Installs', 
    color='Category', 
    trendline='ols', 
    title='Relationship between Revenue and Installs for Paid Apps', 
    color_discrete_sequence=px.colors.qualitative.Vivid, 
    width=1000, 
    height=600 
)

fig.update_layout( 
    plot_bgcolor='black', 
    paper_bgcolor='black', 
    font_color='white', 
    title_font={'size':16}, 
    xaxis=dict(title_font={'size':12}), 
    yaxis=dict(title_font={'size':12}), 
    margin=dict(l=10, r=10, t=30, b=10) 
) 

save_plot_as_html(fig,"Relationship between Revenue and Installs for Paid Apps Graph .html", "")

#used to open automatically
webbrowser.open('file://'+os.path.realpath("Relationship between Revenue and Installs for Paid Apps Graph .html"))