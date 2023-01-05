import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_loading import Load_Data
import streamlit as st

import warnings
warnings.filterwarnings('ignore')

class Graphs:

    def __init__(self):

        dl=Load_Data()
        self.psei=dl.load_stock_data("PSEI")
        self.sectors=dl.load_stock_data("ph_sectors")
        self.stocks=dl.load_stock_data("ph_stocks")
        self.nasdaq=dl.load_stock_data("^IXIC")

        self.ph_gdp_qoq=dl.load_stock_data("ph_gdp_growth_qoq")
        self.ph_gdp_yoy=dl.load_stock_data("ph_gdp_growth_yoy")
        self.ph_inflation=dl.load_stock_data("ph_inflation")
        self.ph_interest_rates=dl.load_stock_data("ph_interest_rates")

        self.us_gdp_qoq=dl.load_stock_data("us_gdp_growth_qoq")
        self.us_gdp_yoy=dl.load_stock_data("us_gdp_growth_yoy")
        self.us_inflation=dl.load_stock_data("us_inflation")
        self.us_interest_rates=dl.load_stock_data("us_interest_rates")

        self.bgcolor="#FAFAF9"  ##F8FBFB"  #FAFAF9  #F0F2F6
        self.gridcolor="#D4E5E6"

        self.ann_text_color="#ffffff"
        self.ann_arrow_color="#636363"
        self.ann_border_color="#c7c7c7"
        self.ann_bg_color="#ff7f0e"

        self.ann_bg_color2="#63A2B6"
        self.ann_bg_color3="black"
        self.ann_bg_color4="red"

        self.line_color1="#B24559"
        self.line_color2="#97879E"
        self.line_color3="#63A2B6"

        #Style- CSS #FAFAF9

    def annotate(self,fig,x,y,text,axv,axy, bg_color, border_color,showarrow=True):
        border_color=border_color
        bg_color=bg_color
        
        
        fig.add_annotation(
        x=x,
        y=y,
        xref="x",
        yref="y",
        text=text,
        showarrow=showarrow,
        font=dict(
            family="Courier New, monospace",
            size=12, 
            color=self.ann_text_color
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1,
        arrowcolor=self.ann_arrow_color,
        ax=axv,
        ay=axy,
        bordercolor=border_color,
        borderwidth=2,
        borderpad=4,
        bgcolor=bg_color,
        opacity=0.8
        )

    def annotate_subplot(self,fig,x,y,text,axv,axy,xref,yref, bgcolor=1,showarrow=True):
        if bgcolor==1:
            bgc=self.line_color3
        elif bgcolor==2:
            bgc=self.ann_bg_color4
        elif bgcolor==3:
            bgc=self.ann_bg_color3
        elif bgcolor==4:
            bgc=self.ann_bg_color4


        fig.add_annotation(
        x=x,
        y=y,
        xref=xref,
        yref=yref,
        text=text,
        showarrow=showarrow,
        font=dict(
            family="Courier New, monospace",
            size=12, 
            color=self.ann_text_color
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1,
        arrowcolor=self.ann_arrow_color,
        ax=axv,
        ay=axy,
        bordercolor=self.ann_border_color,
        borderwidth=2,
        borderpad=4,
        bgcolor=bgc,
        opacity=0.8
        )

    def plot_scatter(self):
        start_date='2000-01-01'
        end_date='2022-12-31'

        df1=self.psei.loc[start_date:end_date]
        df1["ph"]=df1.Close.pct_change()

        #Shifted US timeseries to show how the previous prior US session 
        # at night would affect the local market the next morning
        df2=self.nasdaq.loc[start_date:end_date]
        df2["us"]=df2.Close.pct_change()
        df2["us"]=df2.us.shift(1)

        #Combine and Rename
        merged_df=pd.concat( [df1[["ph"]], df2[["us"]] ], axis=1 )
        merged_df.dropna(inplace=True)
        #display(merged_df.ph.quantile(.95))
        th=0.02
        merged_df["Outlier"]=np.where(np.logical_or( \
                                merged_df["us"]>=th, \
                                merged_df["us"]<=th*-1,  \
                            ),"Volatile Days","Normal Days")
        #display(merged_df.tail())



        #Correlation
        correlation=merged_df.us.corr(merged_df.ph)
        correlation_normal=merged_df.query("Outlier=='Normal Days'").us.corr(merged_df.query("Outlier=='Normal Days'").ph)
        correlation_volatile=merged_df.query("Outlier=='Volatile Days'").us.corr(merged_df.query("Outlier=='Volatile Days'").ph)

        # print("Outlier thresold set as +-2% (90% of all US pct changes belong inside the range of -2% to +2%, the rest are outliers) ")
        # print("Overall Correlation is {:0.2f}%" .format(correlation*100))
        # print("Correlation on normal days is {:0.2f}%" .format(correlation_normal*100))
        # print("Correlation on volatile (Outlier) days is {:0.2f}%" .format(correlation_volatile*100))

        
        
        fig = px.scatter(merged_df, x="us", y="ph",hover_name=merged_df.index.strftime('%m/%d/%Y'),
                        color="Outlier",color_discrete_sequence=["#B24559","#97879E"])



        fig.update_layout(height=450, width=800, title_text="",
                        #paper_bgcolor="#D4E5E6",#F8FBFB
                        plot_bgcolor=self.bgcolor)


        fig.update_xaxes(showgrid=False, 
                        zeroline=False)

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=self.gridcolor, griddash='dot',
                        zeroline=False)


        fig.update_layout(legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ))

        self.annotate(fig,0.08,0.15,"Overall Correlation: {:.2}<br>Correlation (Normal Days): {:.2}<br>Correlation (Volatile Days): {:.2}<br>"
                    .format(correlation,correlation_normal,correlation_volatile) \
                    ,50,-50, self.line_color1,self.ann_border_color,showarrow=False)
        st.plotly_chart(fig,use_container_width=True)
        
    def plot_local_snapshot(self):
        data1=self.psei['Close'].resample("MS").last().loc['2022-01-01':'2022-12-31']
        data1=(data1.divide(data1.iloc[0])-1)*100


        data2=self.sectors.pivot(
            #index ='wpid_random', 
            columns ='symbol', 
            values =['Close']
            ).loc['2022-01-01':'2022-12-31'].resample("MS").last()

        data2=(data2.divide(data2.iloc[0])-1)*100
        data2.columns = data2.columns.droplevel(0)
        data2.drop(columns="ALL",inplace=True)

        sdf=self.stocks.copy()
        sdf["Value"]=sdf.Volume*sdf.Close


        #YTD Price Change
        data3_ytd=sdf.pivot(
            columns ='symbol', 
            values =['Close']
            ).loc['2022-01-01':'2022-12-31'].resample("MS").last()

        data3_ytd=(data3_ytd.divide(data3_ytd.iloc[0])-1)*100
        data3_ytd.columns = data3_ytd.columns.droplevel(0)

        d3_ytd=data3_ytd.iloc[[-1]]
        d3_ytd=pd.melt(d3_ytd)
        d3_ytd.columns=["symbol","ytd"]

        #Average Value Traded (Volume*Close)
        data3_value=sdf.pivot(
            columns ='symbol', 
            values =['Value']
            ).loc['2022-01-01':'2022-12-31'].resample("MS").mean()

        d3_avg_volume=data3_value.mean().to_frame().reset_index()
        d3_avg_volume.columns=["_","symbol","Value"]

        #Merge
        merged_df=pd.merge(d3_avg_volume,d3_ytd, on="symbol", how="inner")
        #display("95th percentile of Value is {:.2f}e+08" .format((merged_df.Value.quantile(0.95)/100000000)) )
        #display(merged_df[merged_df.Value>140000000].sort_values(by="Value", ascending=False).head(10))

        #Selected a few symbols above the 95th percentile of average value traded
        most_liquid=["ICT","MONDE","SM","BDO","CNVRG","AC"]
        data3=data3_ytd[most_liquid]

        data1_psei_ytd=data1
        data2_sectors_ytd=data2
        data3_stocks_ytd=data3


        #Plot
        fig = make_subplots(rows=1, cols=3,vertical_spacing = 0.04,
        subplot_titles=("PSEi YTD%", "PSE Sectors YTD%", "Notable Liquid Stocks YTD%"))

        color1="#63A2B6"


        #PH Traces----------------------------------------------------------------------------------------


        fig.add_trace(
            go.Scatter(x=data1_psei_ytd.index, y=data1_psei_ytd, name="PSEi", 
                    line_color=self.line_color3, 
                    legendgroup=1,
                    ),
                    row=1, col=1)


        for count,i in enumerate(data2_sectors_ytd.columns):
            legend=data2_sectors_ytd.columns[count]
            fig.add_trace(
                go.Scatter(x=data2_sectors_ytd.index, y=data2_sectors_ytd[i], name=legend, 
                legendgroup=2,legendgrouptitle_text="Sectors"
                ),
                row=1, col=2)

        for count,i in enumerate(data3_stocks_ytd.columns):
            legend=data3_stocks_ytd.columns[count]
            fig.add_trace(
                go.Scatter(x=data3_stocks_ytd.index, y=data3_stocks_ytd[i], name=legend, 
                legendgroup=3,legendgrouptitle_text="Stocks"
                ),
                row=1, col=3)

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=self.gridcolor, griddash='dash',
                        zeroline=False)
        fig.update_xaxes(showgrid=False,zeroline=False)

        bgcolor=self.bgcolor
        #bgcolor="#FAFAF9"
        #bgcolor="#F8FBFB"
        fig.update_layout(legend=dict(
            orientation="v",
            groupclick="toggleitem"
            ),
                title={
                        'text': "LOCAL MARKET SNAPSHOT",
                        'y':0.9,
                        'x':0.5,
                        'font_size':20,
                        'xanchor': 'center',
                        'yanchor': 'top'},
            height=490, width=900,
            #font_size=10,
            paper_bgcolor=bgcolor,#F8FBFB
            plot_bgcolor=bgcolor
            )


        #fig.show()
        
        st.plotly_chart(fig,use_container_width=True)

    def plot_pse_vs_ixic(self):
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=self.psei.loc['2000-01-01':'2022-12-31'].index.array, y=self.psei.loc['2000-01-01':'2022-12-31'].Close.array,
                    mode='lines', line_color=self.ann_bg_color4,
                    name='PSEi'))
        #"#63A2B6"

        fig.add_trace(go.Scatter(x=self.nasdaq.loc['2000-01-01':'2022-12-31'].index.array, y=self.nasdaq.loc['2000-01-01':'2022-12-31'].Close.array,
                    mode='lines', line_color=self.ann_bg_color3,opacity=0.2,
                    name='Nasdaq'))

        #"#E08D4A"

        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=self.gridcolor, griddash='dot',
                    zeroline=False)


        fig.update_layout(width=950,height=450,
                    title_text="PSEi Vs Nasdaq Composite Index",
                    paper_bgcolor=self.bgcolor,#F8FBFB
                    plot_bgcolor=self.bgcolor)

        fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01))



        self.annotate(fig,'2022-01-01',7500,"2022-Present<br>Duration->10 Months",100,-50,self.line_color3,self.ann_bg_color3)
        self.annotate(fig,'2020-02-01',7500,"2020 Covid Crash<br>Duration->~2 Months",-60,-100,self.line_color3,self.ann_bg_color3)
        self.annotate(fig,'2007-10-01',4000,"2007-2009<br>Housing Bubble<br>Duration->~16 Months",0,-90,self.line_color3,self.ann_bg_color3)
        self.annotate(fig,'2000-01-01',2200,"2000-2003<br>Dotcom Recession<br>Duration->~39 Months",-50,-80,self.line_color3,self.ann_bg_color3)


        #fig.show()
        #return fig
        st.plotly_chart(fig,use_container_width=True)

    def plot_macro(self):
        #Comparison
        data1_ph=self.ph_gdp_qoq.Close.loc['2000-01-01':'2022-12-31']
        data2_ph=self.ph_gdp_yoy.Close.loc['2000-01-01':'2022-12-31']
        data3_ph=self.ph_inflation.Close.loc['2000-01-01':'2022-12-31']
        data4_ph=self.ph_interest_rates.Close.loc['2000-01-01':'2022-12-31']

        data1_us=self.us_gdp_qoq.Close.loc['2000-01-01':'2022-12-31']
        data2_us=self.us_gdp_qoq.Close.loc['2000-01-01':'2022-12-31']
        data3_us=self.us_inflation.Close.loc['2000-01-01':'2022-12-31']
        data4_us=self.us_interest_rates.Close.loc['2000-01-01':'2022-12-31']


        #Plot
        fig = make_subplots(rows=3, cols=1,vertical_spacing = 0.15,
                subplot_titles=("GDP Growth (MoM%)", "Inflation Rate", "Interest Rates"))

        color1=self.ann_bg_color4
        color2=self.line_color2
        name1="PH"
        name2="US"

        #PH Traces----------------------------------------------------------------------------------------

        # fig.add_trace(
        #     go.Scatter(x=data1_ph.index, y=data1_ph, name=name1, legendgroup=1,
        #             line_color=color1),
        #             row=1, col=1)

        fig.add_trace(
            go.Scatter(x=data2_ph.index, y=data2_ph, name=name1, line_color=color1,showlegend=True, legendgroup=1),
            row=1, col=1)

        


        fig.add_trace(
            go.Scatter(x=data3_ph.index, y=data3_ph, name=name1, line_color=color1,showlegend=False, legendgroup=1),
            row=2, col=1)


        fig.add_trace(
            go.Scatter(x=data4_ph.index, y=data4_ph, name=name1, line_color=color1,showlegend=False, legendgroup=1),
            row=3, col=1)


        #US Traces----------------------------------------------------------------------------------------
        # fig.add_trace(
        #     go.Scatter(x=data1_us.index, y=data1_us, line_color=color2, name=name2, opacity=0.4, legendgroup=2),
        #     row=1, col=1)

        fig.add_trace(
            go.Scatter(x=data2_us.index, y=data2_us, line_color=color2,showlegend=True, opacity=0.4, legendgroup=2,name=name2),
            row=1, col=1)

        fig.add_trace(
            go.Scatter(x=data3_us.index, y=data3_us, line_color=color2,showlegend=False, opacity=0.4, legendgroup=2),
            row=2, col=1)


        fig.add_trace(
            go.Scatter(x=data4_us.index, y=data4_us, line_color=color2,showlegend=False, opacity=0.4, legendgroup=2),
            row=3, col=1)
        #-------------------------------------------------------------------------------------------


        self.annotate_subplot(fig,'2009-03-22',-9,"US-2 Consecutive <br>Down Qrts",90,20,"x1","y1")
        self.annotate_subplot(fig,'2022-06-22',0,"Similar to <br>Since 2009",10,40,"x1","y1")
        self.annotate_subplot(fig,'2022-06-22',7.4,"Relatively<br>Stable",50,-30,"x1","y1",bgcolor=2)

        self.annotate_subplot(fig,'2022-01-22',7.9,"Highest Inflation <br>in 40yrs",-90,-20,"x2","y2")
        self.annotate_subplot(fig,'2022-09-22',6.9,"Relatively<br>Controlled",50,25,"x2","y2",bgcolor=2)

        self.annotate_subplot(fig,'2003-01-22',1.25,"End of 2003<br>Bear Market",50,-70,"x3","y3",bgcolor=1)
        self.annotate_subplot(fig,'2009-03-01',1.25,"End of 2009<br>Bear Market",50,-70,"x3","y3",bgcolor=1)
        self.annotate_subplot(fig,'2022-03-01',0.75,"Early stages of the <br>Tightening Cycle",-50,-70,"x3","y3",bgcolor=1)

        fig.update_layout(height=650, width=900, title_text="")
        #fig.update_layout(paper_bgcolor="#D4E5E6")#F8FBFB
        fig.update_layout(plot_bgcolor=self.bgcolor,paper_bgcolor=self.bgcolor,)


        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor=self.gridcolor, griddash='dash',
                        zeroline=True,zerolinecolor='black',zerolinewidth=1)



        #fig.show()
        st.plotly_chart(fig,use_container_width=True)

    def plot_opportunities(self):
        data1=self.psei['Close'].resample("MS").last().loc['2008-06-01':'2009-12-31']
        data1=(data1.divide(data1.iloc[0])-1)*100

        sdf=self.stocks.copy()
        sdf["Value"]=sdf.Volume*sdf.Close
        #YTD Price Change
        data3_ytd=sdf.pivot(
            columns ='symbol', 
            values =['Close']
            ).loc['2008-06-01':'2009-12-31'].resample("MS").last()



        data3_ytd.dropna(axis=1,inplace=True)

        data3_ytd=(data3_ytd.divide(data3_ytd.iloc[0])-1)*100
        data3_ytd.columns = data3_ytd.columns.droplevel(0)

        d3_ytd=data3_ytd.iloc[[-1]]
        d3_ytd=pd.melt(d3_ytd)
        d3_ytd.columns=["symbol","ytd"]


        #Average Value Traded (Volume*Close)
        data3_value=sdf.pivot(
            columns ='symbol', 
            values =['Value']
            ).loc['2008-06-01':'2009-12-31'].resample("MS").mean()

        d3_avg_volume=data3_value.mean().to_frame().reset_index()
        d3_avg_volume.columns=["_","symbol","Value"]

        #Merge
        merged_df=pd.merge(d3_avg_volume,d3_ytd, on="symbol", how="inner")
 

        #Selected a few symbols above the 90th percentile of average value traded
        most_liquid=merged_df[merged_df.Value>0.57*100000000].sort_values(by="ytd", ascending=False).head(5)["symbol"].values.tolist()
        data3=data3_ytd[most_liquid]
        data3.rename(columns={"DITO":"ISM"},inplace=True)
 

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=data1.index.array, y=data1.array,
                    #mode='lines', 
                    line=dict(color="black", width=2.8),
                    #line_color="#63A2B6",
                    name='PSEi'))

        for count,i in enumerate(data3.columns):
            legend=data3.columns[count]
            if i=="MER":
                o=1
            else:
                o=0.3

            fig.add_trace(
                go.Scatter(x=data3.index, y=data3[i], name=legend, mode="lines",
                legendgroup=2,legendgrouptitle_text="Eventual Leaders",
                opacity=o,
                )
                #row=1, col=1
                )


        # fig.add_trace(go.Scatter(x=self.nasdaq.loc['2000-01-01':'2022-12-31'].index.array, y=self.nasdaq.loc['2000-01-01':'2022-12-31'].Close.array,
        #             mode='lines', line_color="#E08D4A",opacity=0.4,
        #             name='Nasdaq'))



        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=self.gridcolor, griddash='dot',
                    zeroline=False)


        fig.update_layout(width=950,height=450,
                    title_text="PSEi Vs Nasdaq Composite Index",
                    paper_bgcolor=self.bgcolor,#F8FBFB
                    plot_bgcolor=self.bgcolor)


        self.annotate_subplot(fig,'2009-01-01',-15,"PSEI Bear <br> Market Bottom",-30,-100,"x","y",bgcolor=3)
        self.annotate_subplot(fig,'2008-09-01', 60,"MER sustains<br>uptrend even<br>as PSEi tanks",-30,-120,"x","y",bgcolor=4)
        self.annotate_subplot(fig,'2009-06-01', 260,"MER outperforms<br>after<br>market bottom",-110,-60,"x","y",bgcolor=4)
        # self.annotate(fig,'2020-02-01',7500,"2020 Covid Crash<br>Duration->~2 Months",-60,-100)
        # self.annotate(fig,'2007-10-01',4000,"2007-2009<br>Housing Bubble<br>Duration->~16 Months",0,-90)
        # self.annotate(fig,'2000-01-01',2200,"2000-2003<br>Dotcom Recession<br>Duration->~39 Months",-50,-80)


        #fig.show()
        #return fig
        st.plotly_chart(fig,use_container_width=True)


if __name__=='__main__':
    pass
    #dl=Load_Data()
    #psei_df=dl.load_stock_data()
    #print(psei_df.head())