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
    trans_xp_2023 = trans_xp[(trans_xp['Data'] >= '2022-01-01') & (trans_xp['Data'] <= '2022-12-31')]
    # print(trans_xp_2023)

    positions = pd.read_csv('Custodia_2022.csv')
    print(positions[positions['Corretora'] == 'XP'][['Ativo', 'Qtd']])
    for _, row in trans_xp_2023.iterrows():
        asset = row['Ativo']
        price = row['Preco'] 
        broker = row['Corretora']
        price = float(price) + 1
        quantity = row['Quantidade']
        ref = positions.loc[(positions['Ativo'] == asset) & (positions['Corretora'] == broker)]
        if not positions[(positions['Ativo'] == asset) & (positions['Corretora'] == broker)].empty:
            # positions['Qtd'] = positions.mask(positions[(positions['Ativo'] == asset) & (positions['Corretora'] == broker)], positions['Qtd'] + quantity)
                positions.loc[(positions['Ativo'] == asset) & (positions['Corretora']), "Qtd"]  += quantity
                cond = (positions['Ativo'] == asset) & (positions['Corretora'])
                current_qtd = positions[cond]['Qtd'].iloc[0]
                current_amount = positions[cond]['Total'].iloc[0]
                positions.loc[(positions['Ativo'] == asset) & (positions['Corretora']), ("Qtd", "Total")] = (current_qtd+quantity, current_amount+quantity*price)
    print(positions[positions['Corretora'] == 'XP'][['Ativo', 'Qtd', 'Total']])
    positions.to_csv('Processed_2023.csv')

    pass

if __name__ == '__main__':
    main()
