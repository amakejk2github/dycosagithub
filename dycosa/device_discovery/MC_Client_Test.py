import MCast_Client, json

MC = MCast_Client.MCast_Client(('127.0.0.1', 50010), 'index.txt')
param = {}
param['Name'] = 'Arne'
param['Alter'] = 23
print('Versuch 1')
MC.search(param)

