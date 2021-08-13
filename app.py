import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
#from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#%%capture
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])


mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')



gss_clean=gss_clean.replace({'female':'Female', 'male':'Male','strongly agree':'Strongly agree', 'agree':'Agree',
                    'disagree':'Disagree', 'strongly disagree':'Strongly disagree'})



gss_clean = gss_clean.assign(education_level = 
                               pd.cut(gss_clean.education,
                                      
                                      bins=[-.01,10,11,12,13,14,15,16,100], 
                                      labels=("10 years or fewer",
                                              "11 years", 
                                              "12 years",
                                              "13 years",
                                              "14 years",
                                              "15 years",
                                              "16 years",
                                              " More than 16 years")))


website1="""
According to research conducted by the Pew Research Center, the U.S historical gender pay gap was still persistent in 2020. Experts have found that factors such as years of education, occupational segregation, and work experience contribute to this gap. As a result, women as a whole continue to be overrepresented in lower positions in the workforce. Moreover, motherhood experience leads to interrupt their path and impacts their salaries in the long term.(https://www.pewresearch.org/fact-tank/2021/05/25/gender-pay-gap-facts/)
"""

website2="""
Women’s participation in the labor force contribute to the economy. The Brookings  Institution, a nonprofit policy organization, has demonstrated how the gender gap is an impediment to economic grow. Women earn around 85 % less than their male counterparts. The disparity persists regardless of women’s level of education. A way governments and employers can help curb this endemic problem is by examining child-care policies and pay transparency.(https://www.brookings.edu/blog/brookings-now/2019/03/22/charts-of-the-week-the-gender-wage-gap/)
"""

gss_desc="""
The [General Social Survey]( http://www.gss.norc.org/About-The-GSS) (GSS) is a massive public opinion survey to monitor and illustrate trends in opinions in the United States. It contains people’s views on special interest topics, such as crime and violence. Also, it covers trend data of demographics and attitudinal.  
"""

gss_clean2=gss_clean.rename({'sex':'Sex'}, axis=1)
gss_clean2=gss_clean2.groupby('Sex').agg({'income':'mean', 'job_prestige':'mean', 'socioeconomic_index':'mean', 'education':'mean'}).round(2)

gss_clean2 = gss_clean2.reset_index()
gss_clean2 = gss_clean2.rename({'sex':'Sex',
                                     'income':'Annual Income',
                                     'job_prestige':'Job Prestige',
                                     'socioeconomic_index':'Socioeconomic Index',
                                     'education':'Years of Education'}, axis=1)

t2=ff.create_table(gss_clean2)
#t2.show()

gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].astype('category')
gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].cat.reorder_categories(['Strongly agree', 
                                                            'Agree', 
                                                            'Disagree', 
                                                            'Strongly disagree'])


gss_breadbar=gss_clean.groupby(['sex', 'male_breadwinner']).size().reset_index()
gss_breadbar.rename({0:'freq'}, axis=1, inplace=True)

fig3=px.bar(gss_breadbar, x='male_breadwinner',y='freq', color='sex',
            labels={'sex':'Sex', 'freq':'Count', 'male_breadwinner':'Man must be breadwinner'},
            hover_data = ['freq'],
            #text='coltext',
            barmode = 'group'
            )

fig3.update_layout(showlegend=True)
fig3.update(layout=dict(title=dict(x=0.5)))
#fig3.show()

fig4= px.scatter(gss_clean, x='job_prestige', y='income', color='sex',
                 opacity=.4,
                 trendline='ols',
                 height=700, width=1000,
                labels={'sex':'Sex','job_prestige':'Job Prestige', 'income':'Income', 'education':'Years of Education',
                        'socioeconomic_index':'Socioeconomic Index'},
                 hover_data={'education', 'socioeconomic_index'}
                )
#fig4.show()


fig5_1=px.box(gss_clean, x='sex',y='income', 
            labels={'sex':'Sex', 'income':'Annual Income'},
            hover_data = {'sex':False},
            #text='coltext',
            )
fig5_1.update_layout(showlegend=False)
#fig5_1.show()


fig5_2=px.box(gss_clean, x='sex',y='job_prestige', 
            labels={'sex':'Sex', 'job_prestige':'Job Prestige'},
            hover_data = {'sex':False},
            #text='coltext'
            )
fig5_2.update_layout(showlegend=False)
#fig5_2.show()

gss_clean6 = gss_clean[['income','sex','job_prestige']]
gss_clean6['prestige_ranges'] = pd.cut(gss_clean6.job_prestige,6,
                                       labels=(1,2,3,4,5,6))
gss_clean6 =gss_clean6.dropna()

gss_clean6['prestige_ranges'] = gss_clean6['prestige_ranges'].cat.reorder_categories([1,2,3,4,5,6])
#gss_clean6



fig6=px.box(gss_clean6, x='sex',y='income', color='sex',
            #points="all",
            labels={'sex':'Sex', 'job_prestige':'Job Prestige', 'income':'Annual Income', 'prestige_ranges':'Prestige Ranges'},
            color_discrete_map = {'Male':'blue', 'Female':'red'},
            category_orders={'prestige_ranges':[1,2,3,4,5,6]},
            facet_col='prestige_ranges',
            facet_col_wrap=2,
            height=1200           
            )
fig6.update_layout(showlegend=False)
fig6.for_each_annotation(lambda a: a.update(text=a.text.replace("Prestige Ranges=", "Prestige Level ")))
#fig6.show()

#app = JupyterDash(__name__)
app = dash.Dash(__name__)
#server=app.server

app.layout=html.Div(
    [
        
        dcc.Tabs([
            dcc.Tab(label='Intro', children=[
                html.H1("Exploring the Gender Wage Gap in the United States of America"),
                dcc.Markdown(children = website1),
                dcc.Markdown(children = website2),
            ]),
            dcc.Tab(label='Dataset', children=[
                html.H1("The GSS Dataset"),
                dcc.Markdown(children = gss_desc),
            ]),
            dcc.Tab(label='Workforce Statistics', children=[
                html.H2("Statistics of Workforce by Sex"),
                dcc.Graph(figure=t2),
            ]),
            dcc.Tab(label='Perception', children=[
                                
                html.Div([

                    html.H3("Survey"),

                    dcc.Dropdown(id='x-axis',
                        #options=[{'label': i, 'value': i} for i in ['satjob','relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork']],
                        options=[{'label': 'Job Satisfaction', 'value': 'satjob'},
                                 {'label': 'Working mother can be a good mother', 'value': 'relationship'},
                                 {'label': 'Man must be the breadwinner', 'value': 'male_breadwinner'},
                                 {'label': 'Men are better suited for politics', 'value': 'men_bettersuited'},
                                 {'label': 'A child suffers if his or her mother works', 'value': 'child_suffer'},
                                 {'label': 'Family suffers because men overwork', 'value': 'men_overwork'}
                                ],
                        value='male_breadwinner'),

                    html.H3("Group answers by"),

                    dcc.Dropdown(id='y-axis',
                        #options=[{'label': i, 'value': i} for i in ['sex', 'region', 'education_level']],
                        options=[{'label': 'Sex', 'value': 'sex'},
                                 {'label': 'Region', 'value': 'region'},
                                 {'label': 'Education Level', 'value': 'education_level'},
                                ],
                        value='sex'),


                ], style={'width': '25%', 'float': 'left'}),
                
                html.Div([
            
                    dcc.Graph(id="graph")

                ], style={'width': '70%', 'float': 'right'})
                        
                
                
            ]),
            dcc.Tab(label='Income v. Prestige', children=[
                
                dcc.Tab(label='Trends', children=[
                    #Figure point 4
                    html.H2("Income v. Job Prestige"),
                    dcc.Graph(figure=fig4),
                ]),
                dcc.Tab(label='Distribution', children=[
                    #Figure point 5
                    html.Div([
                                html.H2("Annual Income Distribution"),
                                dcc.Graph(figure=fig5_1)
                    ], style={'width':'48%', 'float':'left'}),

                    html.Div([
                                html.H2("Job Prestige Distribution"),
                                dcc.Graph(figure=fig5_2)
                    ], style={'width':'48%', 'float':'right'}),
                ]),
                dcc.Tab(label='Income by Prestige Level', children=[
                    #Figure point 6
                    html.H2("Annual Income by Job Prestige Level"),
                    dcc.Graph(figure=fig6)
                ]),
                                            
            ])
        ])
    ])



@app.callback(Output(component_id="graph",component_property="figure"), 
                  [Input(component_id='x-axis',component_property="value"),
                   Input(component_id='y-axis',component_property="value")])

def make_figure(x, y):
    
    gss_bar=gss_clean.groupby([y, x]).size().reset_index()
    gss_bar.rename({0:'freq'}, axis=1, inplace=True)
    
    
    fig = px.bar(gss_bar,x=x,y='freq',color=y,
                 labels={'sex':'Sex', 'freq':'Count', 
                        'male_breadwinner':'Man must be breadwinner',
                        'satjob':'On the whole, how satisfied are you with the work you do?',
                        'men_bettersuited':'Most men are better suited emotionally for politics than are most women',
                        'child_suffer':'A preschool child is likely to suffer if his or her mother works',
                        'relationship':'A working mother can establish just as warm and secure a relationship with her children as a mother who does not work',
                        'men_overwork':'Family life often suffers because men concentrate too much on their work'
                        },
                 hover_data = ['freq'],
                 barmode = 'group'
                )
    return fig


if __name__ == '__main__':
    #app.run_server(mode='inline', debug=True, port=8051)
    #app.run_server(debug=True, port=8051, host='0.0.0.0')
    app.run_server(debug=True)
