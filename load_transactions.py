import pandas as pd

def complete_year(date: str):
    day, month, year = date.split('/')    
    return f'{day}/{month}/20{year}'

def main():
    trans = pd.read_csv('trades_fii.csv')
    trans_xp = trans[trans['Ativo'].str.endswith('11')]
    trans_xp = trans_xp[trans_xp['Corretora'].str.endswith('XP')]
    trans_xp = trans_xp[trans_xp['Data'] <= '31']
    trans_xp['Data'] = trans_xp['Data'].transform(complete_year)
    trans_xp['Data'] = pd.to_datetime(trans_xp['Data'], format='%d/%m/%Y')
    trans_xp_2023 = trans_xp[(trans_xp['Data'] >= '2023-01-01') & (trans_xp['Data'] <= '2023-12-31')]
    print(trans_xp_2023)
    
    
    positions = pd.read_csv('position_2023.csv')
    print(positions)
    for _, row in trans_xp_2023.iterrows():
        asset = row['Ativo']
        price = row['Preco'] 
        broker = row['Corretora']
        price = float(price) + 1
        print(price)
    pass

if __name__ == '__main__':
    main()
