import seccure
from speck import SpeckCipher
from simon import SimonCipher

my_speck = SpeckCipher(0x123456789ABCDEF00FEDCBA987654321)
my_simon = SimonCipher(0xABBAABBAABBAABBAABBAABBAABBAABBA)

def generatePublicKey():
    private_Key = 'prueba1'
    public_key = seccure.passphrase_to_pubkey(private_Key.encode())
    print(public_key)
    return public_key

def cipherText(texto):
    #print ('escriba texto  a cifrar')
    #simpleText= input()
    cipher_Text = seccure.encrypt(texto.encode(),str(generatePublicKey()).encode())
   # print(cipher_Text)
    return cipher_Text

def decriptText(cipherText):
    private_key = 'prueba1'
    text = seccure.decrypt(cipherText, private_key.encode())
    print(text)                                                                      
    return text

def cipherTextSpeck ():
    
    text = 0xCCCCAAAA55553333
    speck_ciphertext = my_speck.encrypt(text)
    print (speck_ciphertext)
    return speck_ciphertext

def cipherTextSimon():
    text = 0xFFFF0000EEEE1111
    simon_cipher = my_simon.encrypt(text)
    print(simon_cipher)
    return simon_cipher

def decryptSpeck():
    speck_plaintext = my_speck.decrypt(cipherTextSpeck())
    print (speck_plaintext)
    return speck_plaintext


def decryptSimon():
    simon_plaintext = my_simon.decrypt(cipherTextSimon())
    print (simon_plaintext)
    return simon_plaintext
    

