import pandas as pd

accounts= pd.read_csv('accounts.csv')

def addAccount(Username, Password, Account):
    # Create a new row with the provided values
    global accounts
    new_account = pd.DataFrame({'Username': [Username], 'Password': [Password], 'Account': [Account]})
    accounts=pd.concat([accounts,new_account],ignore_index=True)
    accounts.to_csv('accounts.csv', index=False)

def checkAccount(Username, Password, accounts):
    #checking user and password
    rightUser = Username in accounts['Username'].values
    if rightUser:
        rightPassword = accounts.loc[accounts['Username']==Username,'Password'].values[0]
        return Password == rightPassword
    else: 
        return False



addAccount('nnnnn','dfadfa','user')
print(checkAccount('Bob','dafd',accounts))


