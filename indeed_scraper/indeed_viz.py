# indeed_viz.py
import plotly.plotly as plt
import pandas as pd
import sqlite3 as lite
import string
import plotly.tools as tls
from plotly.graph_objs import *

con = lite.connect('indeed.db')
cur = con.cursor()
query = "select (select skill from skills where id=skillId), count(*) from post_skills group by skillId order by count(*)"
cts = cur.execute(query)
counts = cts.fetchall()
results = pd.DataFrame(counts, columns=["skill", "count"])
query = "select count(*) from posts"
n = cur.execute(query).fetchall()[0][0]
proportions = pd.Series(results['count'])/n
results['proportions'] = proportions

skillsList = [skill for skill in results.skill]
firstLetter = [skill[0] for skill in skillsList]
allLetters = [s for s in string.ascii_lowercase]
allNumbers = range(1, 27, 1)
allKeys = dict(zip(allLetters, allNumbers))
convert = [allKeys[k] for k in firstLetter]
results['firstLetter'] = firstLetter
results['firstNumeric'] = convert
final = results.copy()
finalCut = final[final.proportions>0.1]
finalDf = finalCut.sort(columns='firstLetter')
# Remove some weird stuff:
finalDf = finalDf[finalDf.skill!="h2"]
finalDf = finalDf[finalDf.skill!="go"]
finalDf = finalDf[finalDf.skill!="html"]
finalDf = finalDf[finalDf.skill!="span"]

skillType = {'skill': 1, 'programming': 2, 'framework': 3, 'background': 4}
skillTypes = [1,1,1,1,4,2,1,1,4,4,3,4,3,3,2,3,4,1,4,2,1,4,1,4,2,4,1,2,2,2,3,2,3,4,1,1,1]
cats = [skillType.keys()[skillType.values().index(j)] for j in skillTypes]
finalDf['type'] = cats

colors = dict(
    skill='#1f77b4',
    programming='#ff7f0e',
    framework='#2ca02c',
    background='#d62728'
    # Oceania='#9467bd'
)

sizemode = 'area'
sizeref = finalDf['count'].max()/1000.0

def make_trace(X, skillType, sizes, color):
    return Scatter(
        x=X['firstLetter'],  # GDP on the x-xaxis
        y=X['proportions'],    # life Exp on th y-axis
        name=skillType,    # label continent names on hover
        mode='markers',    # (!) point markers only on this plot
        marker= Marker(
            color=color,          # marker color
            size=sizes,           # (!) marker sizes (sizes is a list)
            sizeref=sizeref,      # link sizeref
            sizemode=sizemode,    # link sizemode
            opacity=0.6,          # (!) partly transparent markers
            line=Line(width=0.0)  # remove marker borders
        )
    )

data = Data()
for skillType, X in finalDf.groupby('type'):
    sizes = X['count']    # get population array
    color = colors[skillType]     # get bubble color
    data.append(
        make_trace(X, skillType, sizes, color)  # append trace to data object
    )

# Set plot and axis titles
title = "The Most Desired Data Scientist in the U.S."
x_title = "Skills Requested on Indeed.com"
y_title = "Proportion of Job Posts"

# Define a dictionary of axis style options
axis_style = dict(
    zeroline=False,       # remove thick zero line
    gridcolor='#FFFFFF',  # white grid lines
    ticks='outside',      # draw ticks outside axes
    ticklen=8,            # tick length
    tickwidth=1.5         #   and width
)

# Make layout object
layout = Layout(
    title=title,             # set plot title
    plot_bgcolor='#EFECEA',  # set plot color to grey
    xaxis=XAxis(
        axis_style,      # add axis style dictionary
        title=x_title,   # x-axis title
    ),
    yaxis=YAxis(
        axis_style,      # add axis style dictionary
        title=y_title,   # y-axis title
    )
)

fig = Figure(data=data, layout=layout)

fig['layout'].update(
    hovermode='closest',
    showlegend=False # (!) hover -> closest data pt
)

def make_text(X):
    return 'Skill: %s \
    <br>Percent of posts: %s percent'\
    % (X['skill'], round(X['proportions'],2))

# Again, group data frame by continent sub-dataframe (named X),
#   make one trace object per continent and append to data object
i_trace = 0                                        # init. trace counter

for skillType, X in finalDf.groupby('type'):
    text = X.apply(make_text, axis=1).tolist()     # get list of hover texts
    fig['data'][i_trace].update(text=text)         # update trace i
    i_trace += 1                                   # inc. trace counter

# (@) Send to Plotly and show in notebook
plt.iplot(fig, filename='indeed-bubble-chart')

# finalDf.iplot(kind='bubble', x='firstLetter', y='proportions', size='count', text='skill', xTitle='', yTitle='Proportion of Job Posts', colors=colors, filename='indeed-bubble-chart')






