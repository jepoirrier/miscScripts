#!/usr/bin/python
# affiche toutes les possibilites de lettres avec x caracteres
# argument de ligne de commande : x = le nombre de caracteres
# exemple ./possibilites.py 3 ou python possibilites.py 3
# si pas de ligne de commande, modifiez la variable 'n'
# pour stocker les reponses dans un fichier :
# ./possibilites.py 3 > fichier.txt

import sys

def str2list(s): # transforme une chaine en liste
	l = []
	for i in range(len(s)):
		l.append(s[i])
	print 'chaine transformee en list : ' + str(l)
	return(l)

def list2str(l): # transforme une liste en chaine
	s = ""
	for i in range(len(l)):
		s = s + l[i]
	print 'list transformee en chaine : ' + s
	return s

def incremente(s, li): # augmente 1 lettre de la chaine
	n = len(s) # taille de la chaine
	car = li[n-1] # dernier caractere
	fait = 0
	for i in range(n-1, -1, -1):
		if fait==1:
			break
		tmp = str2list(s)
		if s[i] != car:
			# le caractere n'est pas egal au dernier car.
			tmp[i] = li[li.index(s[i-1])+1]
			fait = 1
		else: # le caractere est egal au dernier caractere
			tmp[i] = li[0] # on reset ce caractere
			if i > 1: # sauf si 1er car, on incremente le precedent
				tmp[i-1] = li[li.index(s[i-1])+1]
			fait = 1
		s = list2str(tmp)
	return(s)

li = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z"
li = li.split(",")

n = int(sys.argv[1])
if n < 1:
	n = 1
if n > 26:
	n = 26

# construction chaines initiales
courante = n * li[0]
finale = n * li[n]

while courante != finale: # boucle construction
	print 'chaine courante : ' + courante
	courante = incremente(courante, li)

print li[int(n)-1]
