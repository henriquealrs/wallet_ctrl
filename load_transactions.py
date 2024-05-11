import pandas as pd

def complete_year(date: str):
    day, month, year = date.split('/')    
    return f'{day}/{month}/20{year}'

def main():
    trans_fii = pd.read_csv('trades_fii.csv')
    trans_stocks = pd.read_csv('ops_stocks_br.csv')
    trans = pd.concat([trans_fii, trans_stocks])
    trans.loc[trans['Corretora'] == 'Rico', 'Corretora'] = 'XP'
    trans = trans[trans['Data'] <= '31']
    trans['Data'] = trans['Data'].transform(complete_year)
    trans['Data'] = pd.to_datetime(trans['Data'], format='%d/%m/%Y')
    trans_2023 = trans[(trans['Data'] >= '2023-01-01') & (trans['Data'] <= '2023-12-31')]

    positions = pd.read_csv('Custodia_2022.csv')
    positions = positions.drop(columns=['Data', 'Retorno'])
    # print(positions[positions['Corretora'] == 'XP'][['Ativo', 'Qtd']])
    for _, row in trans_2023.iterrows():
        asset = row['Ativo']
        if asset.endswith('12'):
            continue
        op_type = row['Op']
        price = row['Preco'] 
        broker = row['Corretora']
        price = float(price)
        quantity = int(row['Quantidade'])
        if op_type == 'Venda':
            quantity = -quantity
        if not positions[(positions['Ativo'] == asset) & (positions['Corretora'] == broker)].empty:
            # positions['Qtd'] = positions.mask(positions[(positions['Ativo'] == asset) & (positions['Corretora'] == broker)], positions['Qtd'] + quantity)
                cond = (positions['Ativo'] == asset) & (positions['Corretora'] == 'XP')
                current_qtd = int(positions[cond]['Qtd'].iloc[0])
                current_amount = positions[cond]['Total'].iloc[0]
                new_amount = current_amount+quantity*price
                new_qtd = int(current_qtd+quantity)
                new_pm = new_amount/float(new_qtd)
                if op_type == 'Venda':
                    new_pm = positions.loc[cond, 'PM'].iloc[0]
                positions.loc[cond, ("Qtd", "Total", "PM")] = (new_qtd, new_amount, new_pm)
        else:
            print(broker, asset)
            new_data = {
                'Corretora' : [broker],
                'Ativo' : [asset],
                'Qtd' : [quantity],
                'PM' : [price],
                'Total' : [quantity * price]}
            new_row = pd.DataFrame(new_data)
            positions = pd.concat([positions, new_row])
    # print(positions[positions['Corretora'] == 'XP'][['Ativo', 'Qtd', 'Total']])
    positions = positions.drop(positions[positions['Qtd'] < 1].index)
    positions.to_csv('Processed_2023.csv')

    pass

if __name__ == '__main__':
    main()
