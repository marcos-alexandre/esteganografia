# encoding: utf-8
from PIL import Image
import binascii,optparse ,os ,sys

os.system('clear')
print ('''
	|==================================|
	|	                           |	
	| [+] Author: marcos Alexandre     |
	| [+] NickName: Krypton Zero       |
	| [+] Data: 18/03/2017             |
	| [+] Email:systemmendax@gmail.com |
	|==================================|
''')
def rgb2hex(r, g, b):
	return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex2rgb(hexcodigo):
	return tuple(map(ord, hexcodigo[1:].decode('hex')))

def str2bin(mensagem):
	binario = bin(int(binascii.hexlify(mensagem), 16))
	return binario[2:]

def bin2str(binario):
	mensagem = binascii.unhexlify('%x' % (int('0b'+binario,2)))
	return mensagem

def encode(hexcodigo, digito):
	if hexcodigo[-1] in ('0','1', '2', '3', '4', '5'):
		hexcodigo = hexcodigo[:-1] + digito
		return hexcodigo
	else:
		return None
#Função para decodificar
def decode(hexcodigo):
	if hexcodigo[-1] in ('0', '1'):
		return hexcodigo[-1]
	else:
		return None
#função para esconder
def esconder(nome_do_arquivo, mensagem):
	img = Image.open(nome_do_arquivo)
	binario = str2bin(mensagem) + '1111111111111110'
	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		dados = img.getdata()
		
		novos_dados = []
		digito = 0
		temp = ''
		for item in dados:
			if (digito < len(binario)):
				novopix = encode(rgb2hex(item[0],item[1],item[2]),binario[digito])
				if novopix == None:
					novos_dados.append(item)
				else:
					r, g, b = hex2rgb(novopix)
					novos_dados.append((r,g,b,255))
					digito += 1
			else:
				novos_dados.append(item)	
		img.colocar_dados(novos_dados)
		img.salvar(nome_do_arquivo, "PNG")
		return "Stego Completo!"
			
	return "Modo de imagem incorreta, não foi possível ocultar"

						
				

def ver_mensagem(nome_do_arquivo):
	img = Image.open(nome_do_arquivo)
	binario = ''
	
	if img.mode in ('RGBA'): 
		img = img.convert('RGBA')
		dados = img.getdata()
		
		for item in dados:
			digito = decode(rgb2hex(item[0],item[1],item[2]))
			if digito == None:
				pass
			else:
				binario = binario + digito
				if (binario[-16:] == '1111111111111110'):

					print ("\tMostrar Mensagem ")

					

					return bin2str(binario[:-16])

		return bin2str(binario)
	return "Modo de imagem incorreta, não foi possível recupera"

def Main():
        parser = optparse.OptionParser('Como usar: '+\
		'--esconde/--ver <imagem>')
	parser.add_option('--esconde', dest='esconder', type='string', \
		help='Insira Caminho para da foto para esconder')
	parser.add_option('--ver', dest='ver_mensagem', type='string', \
		help='Insira caminho da imagem para ver mensagem')
	
	(opcao, args) = parser.parse_args()
	if (opcao.esconder != None):
		text = raw_input("Entrar com a mensagem para esconder na foto: ")
		print esconder(opcao.esconder, text)
	elif (opcao.ver_mensagem != None):
                print ver_mensagem(opcao.ver_mensagem)
	else:
		print parser.usage
		exit(0)


if __name__ == '__main__':
	Main()



