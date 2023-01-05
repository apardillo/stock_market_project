import pandas as pd

class Load_Data:

    def __init__(self):
        #self.psei=pd.read_csv("data/PSEI.csv")
        pass

    def load_stock_data(self,filename):
        df=pd.read_csv(r"data/"+ filename+ ".csv")
        df['date']=pd.to_datetime(df['date'],format='%Y-%m-%d')
        df.set_index("date",inplace=True)

        return df
        

if __name__=='__main__':
    
    dl=Load_Data()
    psei_df=dl.load_stock_data()
    print(psei_df.head())