import pandas as pd 
import plotly.io as pio 
import plotly.graph_objects as go
import webbrowser 
import os
from datetime import datetime
import pytz  

# Sample data (Top 3 categories: Social, Games, Productivity)
data = pd.read_csv("C:/Users/Pc/Desktop/Null Class Assignment/Assignment 2/app_data2.csv")

# Applying filters:
filtered_data = data[
    (data['Avg_Installs_Free'] >= 10000) & 
    (data['Avg_Revenue_Free'] >= 10000) &  
    (data['Android Version'] > 4.0) &      
    (data['Size (MB)'] > 15) &             
    (data['Content Rating'] == 'Everyone') &  
    (data['App Name'].apply(lambda x: len(x) <= 30))  
]

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

plot_width = 1000 
plot_height = 450 
plot_bg_color = 'black' 
text_color = 'white' 
title_font = {'size':16} 
axis_font = {'size':12}

# To Create figure 1
fig1 = go.Figure()

# Add bar charts for Revenue
# For Free
fig1.add_trace( 
    go.Bar(
    x=data['Category'], 
    y=data['Avg_Revenue_Free'],
    marker_color='blue', 
    name='Revenue (Free Apps)'
    )    
)
# For Paid
fig1.add_trace( 
    go.Bar(
    x=data['Category'], 
    y=data['Avg_Revenue_Paid'], 
    marker_color='green',
    name='Revenue (Paid Apps)'
    ) 
)
# Add line charts for Installs (Secondary y-axis)
# For Free
fig1.add_trace( 
    go.Scatter( 
    x=data['Category'], 
    y=data['Avg_Installs_Free'], 
    marker_color='Red',
    name='Installs (Free Apps)',
    mode='lines+markers',
    yaxis="y2"
    ) 
)
# For Paid
fig1.add_trace( 
    go.Scatter( 
    x=data['Category'], 
    y=data['Avg_Revenue_Paid'], 
    marker_color='Yellow',
    name='Installs (Paid Apps)',
    mode='lines+markers',
    yaxis="y2"
    ) 
)
# Set up dual-axis layout
fig1.update_layout(
    width = plot_width,
    height = plot_height,
    plot_bgcolor='black', 
    paper_bgcolor='black', 
    font_color='white', 
    title_font={'size':16},
    title="Top 3 App Catogeries Average Installs vs Revenue: Free vs Paid Apps",
    xaxis=dict(title="App Category"),
    yaxis=dict(title="Average Revenue ($)", showgrid=False),
    yaxis2=dict(title="Average Installs", overlaying="y", side="right", showgrid=False, type="log"),
    legend=dict(x=0, y=1),
    margin=dict(l=10, r=10, t=30, b=10)
)

save_plot_as_html(fig1,"Top 3 App Catogeries Average_Installs_vs_Revenue_Free_vs_Paid_Apps.html","")

# To Create figure 2
fig2 = go.Figure()

# Add bar charts for Revenue
# For Free
fig2.add_trace( 
    go.Bar(
    x=filtered_data['Category'], 
    y=filtered_data['Avg_Revenue_Free'],
    marker_color='blue', 
    name='Revenue (Free Apps)',
    )    
)
# For Paid
fig2.add_trace( 
    go.Bar( 
    x=filtered_data['Category'], 
    y=filtered_data['Avg_Revenue_Paid'], 
    marker_color='green',
    name='Revenue (Paid Apps)',
    ) 
)
# Add line charts for Installs (Secondary y-axis)
# For Free
fig2.add_trace( 
    go.Scatter( 
    x=filtered_data['Category'], 
    y=filtered_data['Avg_Installs_Free'], 
    marker_color='Red',
    name='Installs (Free Apps)',
    mode='lines+markers',
    yaxis="y2"
    ) 
)
# For Paid
fig2.add_trace( 
    go.Scatter( 
    x=filtered_data['Category'], 
    y=filtered_data['Avg_Revenue_Paid'], 
    marker_color='Yellow',
    name='Installs (Paid Apps)',
    mode='lines+markers',
    yaxis="y2"
    ) 
)

# Set up dual-axis layout
fig2.update_layout(
    width = plot_width,
    height = plot_height,
    plot_bgcolor='black', 
    paper_bgcolor='black', 
    font_color='white', 
    title_font={'size':16},
    title="Average Installs vs Revenue:Free vs Paid Apps",
    xaxis=dict(title="App Category"),
    yaxis=dict(title="Average Revenue ($)", showgrid=False),
    yaxis2=dict(title="Average Installs", overlaying="y", side="right", showgrid=False, type="log"),
    legend=dict(x=0, y=1),
    margin=dict(l=10, r=10, t=30, b=10)
)

save_plot_as_html(fig2,"Average_Installs_vs_Revenue_Free_vs_Paid_Apps.html","")

plot_containers_split=plot_containers.split('</div>')

if len(plot_containers_split) > 1:
    final_plot=plot_containers_split[-2]+'</div>'
else:
    final_plot=plot_containers

dashboard_html= """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name=viewport" content="width=device-width,initial-scale-1.0">
    <title>Average Installs vs Revenue: Free vs Paid Apps</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #333;
            color: #fff;
            margin: 0;
            padding: 0;
        }}
        .header {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            background-color: #444
        }}
        .header img {{
            margin: 0 10px;
            height: 50px;
        }}
        .container {{
            display: flex;
            flex-wrap: wrap;
            justify_content: center;
            padding: 20px;
        }}
        .plot-container {{
            border: 2px solid #555
            margin: 10px;
            padding: 10px;
            width: {plot_width}px;
            height: {plot_height}px;
            overflow: hidden;
            position: relative;
            cursor: pointer;
        }}
        .insights {{
            display: none;
            position: absolute;
            right: 10px;
            top: 10px;
            background-color: rgba(0,0,0,0.7);
            padding: 5px;
            border-radius: 5px;
            color: #fff;
        }}
        .plot-container: hover .insights {{
            display: block;
        }}
        </style>
        <script>
            function openPlot(filename) {{
                window.open(filename, '_blank');
                }}
        </script>
    </head>
    <body>
        <div class= "header">
            <h1>Average Installs vs Revenue: Free vs Paid Apps</h1>
        </div>
        <div class="container">
            {plots}
        </div>
    </body>
    </html>
    """

final_html=dashboard_html.format(plots=plot_containers,plot_width=plot_width,plot_height=plot_height)

dashboard_path=os.path.join(html_files_path,"web page.html")

with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(final_html)

# Get current time in IST (Indian Standard Time)
current_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()

# Define time range
start_time = datetime.strptime("13:00", "%H:%M").time()  # 1 PM
end_time = datetime.strptime("14:00", "%H:%M").time()    # 2 PM

# Check if current time is within the range
if start_time <= current_time <= end_time:
    #Used to open automatically to Display the graph
    webbrowser.open('file://'+os.path.realpath("web page.html"))
else:
    print("The graph is not available at this time.")

