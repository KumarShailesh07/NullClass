import pandas as pd 
import plotly.io as pio 
import plotly.graph_objects as go
import webbrowser 
import os
from datetime import datetime
import pytz 

data=pd.read_csv('C:/Users/Pc/Desktop/Null Class Assignment/Assignment 3/app_ratings.csv')

# Data cleaning
data = data.dropna(subset=["Rating"])
for column in data.columns :
    data[column].fillna(data[column].mode()[0],inplace=True) 
data = data[data["Rating"] <= 5] 
data.dropna(subset=["Reviews"],inplace=True)

# Add Rating Group column
def rating_group(rating):
    if rating >= 4:
        return 'Top rated'
    elif rating >= 3:
        return 'Above average'
    elif rating >= 2:
        return 'Average'
    else:
        return 'Below average'

data['Rating_Group'] = data['Rating'].apply(rating_group)

# Apply filtering conditions
filtered_data = data[
    (data['Reviews'] >= 10) &  
    (data['Rating'] >= 4.0) & 
    (data['App Name'].str.contains('C', case=False))  
]

# Filter categories with more than 50 apps
category_counts = data['App Category'].value_counts()
valid_categories = category_counts[category_counts > 50].index
filtered_df = filtered_data[filtered_data['App Category'].isin(valid_categories)]

html_files_path="./"
if not os.path.exists(html_files_path):
    os.makedirs(html_files_path) 
plot_containers=""
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

plot_width=400
plot_height=300
plot_bg_color='black'
text_color='white'
title_font={'size':16}
axis_font={'size':12}

# To create figure
fig = go.Figure()

#Figure 
categories = filtered_df['App Category'].unique()
for category in categories:
    fig.add_trace(go.Violin(
        y=filtered_df[filtered_df["App Category"] == category]['Rating'],  
        name=category,  
        box_visible=True,  
        meanline_visible=True, 
        points="all",  
        line_color="#636EFA"  
        )
    )     

fig.update_layout(
    title="Violin Plot of App Ratings by Category",
    xaxis_title="App Category",
    yaxis_title="Rating",
    template="plotly_white"
)
save_plot_as_html(fig,"Violin Plot.html","")
            
# Get current time in IST (Indian Standard Time)
current_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()

# Define time range
start_time = datetime.strptime("16:00", "%H:%M").time()  
end_time = datetime.strptime("18:00", "%H:%M").time()    

# Check if current time is within the range
if start_time <= current_time <= end_time:
    #Used to open automatically to Display the graph
    webbrowser.open('file://'+os.path.realpath("Violin Plot.html"))
else:
    print("The graph is not available at this time.")