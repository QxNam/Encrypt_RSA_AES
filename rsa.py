import random

def is_prime(num:int=2) -> bool:
    if num < 2:
        return False
    if all([num%j!=0 for j in range(2, int(num**0.5+1))]):
        return True
    return False

def random_prime(min_value:int=2, max_value:int=1000) -> int:
    while True:
        num = random.randint(min_value, max_value)
        if is_prime(num):
            return num

def gcd(a:int, b:int) -> int:
    while b != 0:
        a, b = b, a % b
    return a

def check_e(e:int, phi:int) -> bool:
    if gcd(e, phi) == 1:
        return True
    return False

def check_d(d:int, e:int, phi:int) -> bool:
    if (d*e)%phi == 1:
        return True
    return False

def random_p_q(min_prime:int=50, max_prime:int=999) -> tuple:
    p = random_prime(min_prime, max_prime)
    while True:
        q = random_prime(min_prime, max_prime)
        if p!=q:
            break
    return p, q

def select_e(phi:int) -> int:
    if phi==2:
        return None
    while True:
        e = random.randint(2, phi-1)
        if check_e(e, phi):
            return e

def generate_d(e:int, phi:int) -> int:
    while True:
        d = random.randint(1, 2*phi)
        if check_d(d, e, phi):
            return d

def generate_key_pair() -> dict:
    # step 1: generate p, q (p and q both prime and p not equal to q)
    p, q = random_p_q(100, 200)

    # step 2: calculate n = p * q
    n = p*q

    # step 3: calculate phi = (p-1) * (q-1)
    phi = (p-1)*(q-1)

    # step 4: select e from 2 to phi-1 such that gcd(e, phi) = 1
    e = select_e(phi)

    # step 5: select d from 1 to 2*phi such that (d*e)%phi = 1
    d = generate_d(e, phi)

    return {'p':p, 'q':q, 'e':e, 'n':n, 'd':d, 'phi':phi, 'public_key': (n, e), 'private_key': (n, d)}

################################
# encrypt and decrypt
def vec2text(lst:list) -> str:
    return ''.join([chr(i) for i in lst])
    
def text2vec(text:str) -> list:
    return [ord(i) for i in text]

def n_plit(dec_number):
    return len(hex(dec_number)[2:])

def dec2hex(num: list, n:int) -> str:
    '''Convert decimal numbers to hex string'''
    n_fill = n_plit(n)
    return ''.join([str(hex(i)[2:]).zfill(n_fill) for i in num])

def hex2dec(text: str, n:int) -> list:
    '''Convert hex string to decimal numbers'''
    i_split = n_plit(n)
    return [int(text[i:i+i_split], 16) for i in range(0, len(text), i_split)]

def encrypt(public_key:tuple, text:str) -> str:
    '''Encrypt text using public key (n, e), fomular: c = m^e mod n.'''
    n, e = public_key
    vector = text2vec(text)
    vector_encrypt = [(pow(num, e, n)) for num in vector]
    return {'vector': vector_encrypt, 'text': dec2hex(vector_encrypt, n)}

def decrypt(private_key:tuple, text:str) -> dict:
    '''Decrypt text using private key (n, d), fomular: m = c^d mod n.'''
    n, d = private_key
    vector = hex2dec(text, n)
    vector_decrypt = [(pow(num, d, n)) for num in vector]
    return {'vector': vector_decrypt, 'text': vec2text(vector_decrypt)}
################################

if __name__ == '__main__':
    gen = generate_key_pair()
    u_key, r_key = gen['public_key'], gen['private_key']
    message = 'chào các bạn'
    print(f'Public key (n, e): {u_key}')
    print(f'Private key (n, d): {r_key}')
    print(f'Message: {message}, {text2vec(message)}')

    print('\n'+'-'*10+'Encrypt'+'-'*10)
    en = encrypt(u_key, message)
    print(f'Dec: {en["vector"]}')
    print(f'Hex: {en["text"]}')

    print('\n'+'-'*10+'Decrypt'+'-'*10)
    de = decrypt(r_key, en['text'])
    print(f'Vector: {de["vector"]}')
    print(f'Text: {de["text"]}')