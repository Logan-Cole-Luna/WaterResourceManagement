import pandas as pd

accounts= pd.read_csv('accounts.csv')

def addAccount(Username, Password, Account):
    # Create a new row with the provided values
    global accounts
    new_account = pd.DataFrame({'Username': [Username], 'Password': [Password], 'Account': [Account]})
    accounts=pd.concat([accounts,new_account],ignore_index=True)
    accounts.to_csv('accounts.csv', index=False)


addAccount('nnnnn','dfadfa','user')



