import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st

from data_loading import Load_Data
from visuals import Graphs
from streamlit_option_menu import option_menu

#Layout


st.set_page_config(layout="wide")
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


with st.sidebar:
    selection= option_menu(
        menu_title="Navigating Bear Markets- PSE",
        options=["Today's Market",
                "Learning From History",
                "Next Big Opportunities",
                "Summary"],
        icons=["globe","skip-backward-fill","cash","person-check"],
        menu_icon="graph-down-arrow",
        styles={
        #"container": {"padding": "0!important", "background-color": "#fafafa"},
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        #"icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},  ##eee
        #"nav-link-selected": {"background-color": "#eee"},    
        }
       # orientation="horizontal",
        
    )





# selection= option_menu(
#     menu_title=None,
#     options=["Today's Market",
#             "Learning From History",
#             "Next Big Opportunities",
#             "Summary"],
#     icons=["globe","skip-backward-fill","cash","person-check"],
#     menu_icon="cast",
#     styles={
#     #"container": {"padding": "0!important", "background-color": "#fafafa"},
#     "container": {"padding": "0!important", "background-color": "#fafafa"},
#     #"icon": {"color": "orange", "font-size": "25px"}, 
#     "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},  ##eee
#     #"nav-link-selected": {"background-color": "#eee"},    
#     },
#      orientation="horizontal",
# )

# st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

# st.markdown("""
# <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
#   <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">Data Professor</a>
#   <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
#     <span class="navbar-toggler-icon"></span>
#   </button>
#   <div class="collapse navbar-collapse" id="navbarNav">
#     <ul class="navbar-nav">
#       <li class="nav-item active">
#         <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
#       </li>
#       <li class="nav-item">
#         <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">YouTube</a>
#       </li>
#       <li class="nav-item">
#         <a class="nav-link" href="https://twitter.com/thedataprof" target="_blank">Twitter</a>
#       </li>
#     </ul>
#   </div>
# </nav>
# """, unsafe_allow_html=True)


def today():
    # Write the title and the subheader
    t1,t2=st.columns([0.7,.3])
    t1.title(
        "Navigating Bear Markets"
    )

    t1.subheader(
        """
        1. Managing Risk AND
        """
    )

    t1.subheader(
        """
        2. Finding the Next Big Investment Opportunities

        * Context- In the Philippine Stock Market
        """
    )
    #navigating_road   navigating a ship stormy weather_.png
    t2.image("pictures/navigating_road.png", 
            #caption="generated with  Craiyon.com"
            )


    st.markdown("""---""")
    st.subheader("""What the Market Looks Like Today""")


    text_intro='''
        2022 has a been a tough year for most investors, as different classes from around the world, 
        especially equities and crypto currencies have taken a beating. For many investors (including myself), 
        this is the first time they've encountered a bear market like this, thus, having no prior frameworks 
        on how to navigate such a volatile period. My goal for creating this app is to leverage historical data to help 
        investors/traders (philippine stock market investors in particular) manage risk during these times and to find the next 
        opportunities that come at the end of every bear market cycle. But first, let's take a look at the state of our current market:
    '''

    st.markdown(text_intro, unsafe_allow_html=False)
    st.text("")
    v=Graphs()
    
    #v.plot_scatter()

    a1,a2,a3=st.columns(3)

    text_psei_comm='''
        __PSEI Commentary:__
        ↓16.4% YTD due to:
        1) High Inflation
        2) High Interest Rates
        3) US Recession
        4) Russia-Ukraine War 
    '''

    text_sectors_comm='''
        __Resilient Sectors:__
        1) Mining and Oil
        2) Financials

        _*Due to high gas prices, and high interest rates_
    '''

    text_stocks_comm='''
        __Weakest Liquid Stocks:__
        1) CNVRG
        2) MONDE


    '''   

    a1.markdown (text_psei_comm, unsafe_allow_html=False)
    a2.markdown (text_sectors_comm, unsafe_allow_html=False)
    #a3.markdwon ("sample_text3", "5%", "6%")
    a3.markdown (text_stocks_comm, unsafe_allow_html=False)

    #st.write("TEXT SAMPLE napud")
    v.plot_local_snapshot()
    


def historical_data():
    st.subheader("""Learning From History""")
    text_intro='''
    Bear Markets have occurred in the past. Here, we look the present market and compare it to similar market conditions in the
    past 20 years. Also, since the US is the world's largest and most powerful economy, and has an effect on the world economy, it
    would also be useful to compare the PH market with the US. 
    '''

    st.markdown(text_intro, unsafe_allow_html=False)

    v=Graphs()
    v.plot_pse_vs_ixic()

    text_2='''
    Here, we see a pattern that once every 10 years or so, the US economy faces challenges with it's economy. In 2000, it was the 
    dotcom boom and bust, while in 2009, it was the housing bubble. Now in 2022, they're facing recessionary pressure as well due to
    record high inflation, high interest rates, the Russia-Ukraine War, and the economic slowdown.  From
    historical data from the past 20 years, we can see that bear markets can usually last anywhere from around 16 months to 39 months.
    Since there seems to be some type of visual correlation between the US and PH market, especially during bear markets, from a risk
    management point of view, I would advise individual investors, to be patient in deploying their hard earned money at this stage.
    Things might not always exactly turn out as before, but if history's any guide, we can say that bear markets can last longer than
    you think, especially since we are still at month 10 as of this writing. 
    '''

    st.markdown(text_2, unsafe_allow_html=False)

    v.plot_scatter()

    text_3='''
    Here, I've explored further on the correlation between the closing price percent change in the from the US overnight session, 
    and the closing price percent change in the  PH market the next day. We can see that on more volatile days (the outliers), the 
    correlation is stronger, suggesting that a good risk management technique is to use the US market as a guide. If there is still
    too much volatily in the US market from the prior day, maybe it would be best to wait for volatility to die down before deploying
    capital in the PH market.
    '''

    st.markdown(text_3, unsafe_allow_html=False)

    


    text_index_comparison='''
    For the most part, the PH market has followed the US market until
    '''   
    #a1,a2=st.columns(2)
    #a2.markdown (text_index_comparison, unsafe_allow_html=False)

    st.markdown("""---""")
    st.subheader("""Macroeconomics""")
    text_4='''
    So far we've only studied price action. However, the market is a discounting mechanism, where it tries to take current 
    fundamental and macro-economic news, predicts that several months/years into the future, then reflects this in the share
    price. With that, it would also help to look at  current and historical macro-economic indicators. Feel free to play around with the 
    charts.
    '''

    st.markdown(text_4, unsafe_allow_html=False)
    v.plot_macro()

    text_5='''
    Earlier this year, the US experienced 2 consecutive quarters of negative MoM% GDP growth. This was very similar to 2009, 
    where the bear market lasted for 16 months. Also, US inflation reached its highest levels, since 1981. Part of this had to do
    with the aggressive monetary easing since 2010, which had to be done to help the economy recover from the housing bubble
    recession. Because of this, there is now exists excess liquidity in the markets, and production cannot keep up with the demand. Aside from that
    there are pressures in the supply side due to the Russia-Ukraine War (one of the major oil suppliers). See that historically, the fed
    had to cut rates for several quarters before the bear market bottomed in 2003 and 2009. But the context was different that time
    since interest rates were relatively controlled, unlike today, where inflation is just too high for the Fed to consider
    any type of monetary easing.
    '''

    st.markdown(text_5, unsafe_allow_html=False)   

    
    text_6='''
    Comparing the US to the PH economy, you can see that GDP growth and inflation rates of the PH are relatively stable. Unlike the
    US, PH econonmic indictors don't show anything out of the ordinary, and is still within the range of the previous years' values.
    The Philippines is facing less internal problems, but the drop in the share price is attributed more to global/external pressures,
    such as the high correlation to the downside from global markets like the US. Also, the PH didn't ease as much the past few years,
    and since inflation is still relatively controlled, meaning if some global emergency would happen, they can still cut rates as a last 
    resort. If the external headwinds do subside, we can expect the PH to bounce strong since internals aren't that bad.  
    '''

    st.markdown(text_6, unsafe_allow_html=False)   


    text_6='''
    For investors, I would recommend waiting for specific catalysts that could stabilize the economy before deploying too much money
    into PH stocks. We should wait for inflationary pressures to subside, such as the end of the Russia Ukraine war, or for the US
    to come up with a bills/ways/methods to increase production/productivity in the economy or to stabilize the high prices of goods.
    This would allow the Fed to start easing again, which reversed the bear markets in the past. Until then, caution is advised today
    since we are still in the early stages of the monetary tightening cycle. 
    '''

    st.markdown(text_6, unsafe_allow_html=False)   

def opportunities():
    st.subheader("""Finding the Next Big Opportunities""")
    text_intro='''
    Bear Markets can be tough, but when they do end, that becomes a golden opportunity to make money. Here we will study the
    biggest winners from 2009 so that we can be prepared for the next bullrun.
    '''

    st.markdown(text_intro, unsafe_allow_html=False)

    v=Graphs()
    v.plot_opportunities()


    text_1='''
    During volatile times, global stock markets, the PSEi, and individual stocks are highly correlated. However, as fundamentals and outlook
    for the economy improves, we start to see alpha again. Here we can see that a few months before the market bottomed, several stocks
    were already showing relative strength compared to the market and they became the leaders of the next bullmarket cycle. 
    I've highlighted Meralco (MER), the strongest of the eventual leaders. 6 months prior to the market bottom, it made a strong
    move, and as the PSEI continued to go lower, MER sustained its uptrend. When the market finally bottomed, MER made an even bigger upmove
    and ended the year up 430% from where it was 18 months ago.
    '''

    st.markdown(text_1, unsafe_allow_html=False)


    text_2='''
    In addition to the risk management and market timing recommendations I made earlier, we add another layer to our decision making- stock selection.
    Look for the strongest issues that are holding up well during market downturns, since these could be the leaders of the next bull
    market cycle.'''

    st.markdown(text_2, unsafe_allow_html=False)


def summary():
    st.title("""Summary- Navigating Bear Markets""")
    st.markdown("""---""")
    

    st.subheader("""1. Manage Risk""")
   

    a1,a2,a3=st.columns(3)
    
    comm1='''
    __A) Patience is Key:__  
    - Bear Markets during recessions may last anywhere from 16-39 months.

    '''

    comm2='''
    __B) Use US market as a guide__  
    - During Volatile Periods, use the US Market's percent change in the previous session as a guide/reference.

    '''

    comm3='''
    __C) Monitor local and US news__  
    - Monitor news about gdp growth, inflation rates, and interest rates to understand where we are in the cycle.

    '''

    comm4='''
    __A) Look for price and Macro Signals__  
    - Use a combination of technical analysis and macroeconomic cycle analysis to predict if the bottom is near.

    '''

    comm5='''
    __B) Prioritize Relative Strength__  
    - Monitor individual stocks that are relatively stronger than the PSEi since they could be next big winners in the next bull market cycle.

    '''

    a1.image("pictures/meditation.png", caption="generated with  Craiyon.com")
    a1.markdown(comm1)

    

    a2.image("pictures/us flag.png", caption="generated with  Craiyon.com")
    a2.markdown(comm2)

    a3.image("pictures/newspaper cartoon style blue background.png", caption="generated with  Craiyon.com")
    a3.markdown(comm3)

    #st.markdown("""---""")
    st.text("")
    st.text("")
    st.subheader("""2. Prepare for Big Opportunities""")
    
    st.text("")
    b0,b1,b2,b4=st.columns([.17,.33,.33,.17], gap="large")


    b1.image("pictures/financial markets cartoon style.png", caption="generated with  Craiyon.com")
    b1.markdown(comm4, unsafe_allow_html=True)
    b2.image("pictures/muscle arm only cartoon style blue background.png", caption="generated with  Craiyon.com")
    b2.markdown(comm5, unsafe_allow_html=True)




#Initialize

list_of_pages = [
    "Where We Are Today",
    "Learning From History",
    "Finding the Next Big Opportunities",
    "Summary"
]

#st.sidebar.title(':scroll: Main Pages')
#selection = st.sidebar.radio("Go to: ", list_of_pages)

if selection == "Today's Market":
    today()

elif selection == "Learning From History":
    historical_data()

elif selection == "Next Big Opportunities":
    opportunities()

elif selection == "Summary":
    summary()

