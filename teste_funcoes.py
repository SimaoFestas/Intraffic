# Programa de teste das funções

from client_v4_en import *

print(get_all_ui()) # Suposto dar vazio
print('--------------------------------------------------------------------------------------------\n')
post_ui('1') # Faz o post de um Acidente

print(get_all_ui()) # Suposto dar um Acidente
print('--------------------------------------------------------------------------------------------\n')

post_ui('2') #Faz mais um post

print(get_all_ui()) # Suposto dar dois alertas unsolved
print('--------------------------------------------------------------------------------------------\n')

delete_ui('1')  # Coloca o estado do primeiro alerta como solved

print(get_all_ui()) # Faz o get apenas de um alerta, com o AlertNr = 2
print('--------------------------------------------------------------------------------------------\n')


post_ui('3') #Faz mais um post


print(get_all_ui()) # O alerta correspondente a Road with poor condition/Signaling' esta unsolved

print('--------------------------------------------------------------------------------------------\n')

post_ui('3') #

print(get_all_ui()) # O alerta correspondente a Road with poor condition/Signaling' Nao aparece
print('--------------------------------------------------------------------------------------------\n')

print(get_id_ui('solved')) # O alerta correspondente a Road with poor condition/Signaling' aparece solved
print('--------------------------------------------------------------------------------------------\n')

