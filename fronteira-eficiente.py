import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from random import random

def risco_carteira(peso_a,peso_b,retorno_a,retorno_b,risco_a,risco_b,corr_ab):
    risco_a = risco_a / 100
    risco_b = risco_b / 100
    return 100 * (peso_a ** 2 * risco_a ** 2 + 2 * peso_a * peso_b * risco_a * risco_b * corr_ab + peso_b ** 2 * risco_b ** 2) ** (1/2)

def retorno_carteira(peso_a,peso_b,retorno_a,retorno_b):
    return (peso_a * retorno_a + peso_b * retorno_b)


tickets = ['ELET3.SA','BBDC4.SA']

df = yf.download(tickets,start='2022-01-01',end='2022-06-07')['Adj Close']

risco_elet3 = df['ELET3.SA'].pct_change(1).std()
risco_bbdc4 = df['BBDC4.SA'].pct_change(1).std()
retorno_elet3 = (( df['ELET3.SA'].iloc[-1] / df['ELET3.SA'].iloc[0] ) - 1) * 100
retorno_bbdc4 = (( df['BBDC4.SA'].iloc[-1] / df['BBDC4.SA'].iloc[0] ) - 1) * 100
corr_elet3_bbdc4 = df['ELET3.SA'].corr(df['BBDC4.SA'])

riscos_carteiras = []
retornos_carteiras = []
for i in range(1000):
    peso_elet3 = random()
    peso_bbdc4 = 1 - peso_elet3
    riscos_carteiras.append(
        risco_carteira(peso_a=peso_elet3,peso_b=peso_bbdc4,retorno_a=retorno_elet3,retorno_b=retorno_bbdc4,risco_a=risco_elet3,risco_b=risco_bbdc4,corr_ab=corr_elet3_bbdc4)
    )
    retornos_carteiras.append(
        retorno_carteira(peso_a=peso_elet3,peso_b=peso_bbdc4,retorno_a=retorno_elet3,retorno_b=retorno_bbdc4)
    )



r = [{'risco':riscos_carteiras[i] , 'retorno':retornos_carteiras[i]} for i in range(len(riscos_carteiras)) ]
r.sort( key = lambda x : x['risco'] )

fig = plt.figure(figsize=(10,8))
plt.scatter(x=riscos_carteiras, y=retornos_carteiras,color='black',marker='.')
plt.axvline(r[0]['risco'],color='green')
plt.axhline(r[0]['retorno'],color='green')
plt.xlim(0.015,0.022)
plt.ylim((8,35))
plt.title('FRONTEIRA EFICIENTE DE MARKOWITZ NA PRÁTICA')
plt.xlabel('Risco')
plt.ylabel('Retorno')
plt.plot()
plt.savefig('markowitz.png')
plt.show()