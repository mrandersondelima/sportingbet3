from random import randrange
 
jogos = [2, 5]
distribuicao = [0, 0, 0, 0, 0, 0]
 
for i in range(1000):
	temp = jogos[randrange(2)]
	#print(temp)
	distribuicao[temp] += 1
 
print( distribuicao[2] )
print( distribuicao[5] )