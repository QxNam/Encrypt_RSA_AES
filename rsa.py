import random

def random_p_q(max_prime:int=100) -> tuple:
    num_prime = [i for i in range(2, max_prime) if all([i%j!=0 for j in range(2, int(i**0.5+1))])]
    p = random.choice(num_prime)
    num_prime.remove(p)
    q = random.choice(num_prime)
    return p, q

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

def select_e(phi:int) -> int:
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            return e

def generate_d(e:int, phi:int) -> int:
    d = 0
    while True:
        if (d*e)%phi == 1:
            return d
        d += 1
        
def cvt_list2text(lst:list) -> str:
    return ''.join([chr(i) for i in lst])
    
def cvt_text2list(text:str) -> list:
    return [ord(i) for i in text]

def generate_key_pair() -> dict:
    # step 1: generate p, q (p and q both prime and p not equal to q)
    p, q = random_p_q()

    # step 2: calculate n = p * q
    n = p*q

    # step 3: calculate phi = (p-1) * (q-1)
    phi = (p-1)*(q-1)

    # step 4: select e from 2 to phi-1 such that gcd(e, phi) = 1
    e = select_e(phi)

    # step 5: select d from 1 to 2*phi such that (d*e)%phi = 1
    d = generate_d(e, phi)

    return {'p':p, 'q':q, 'e':e, 'n':n, 'd':d, 'phi':phi, 'public_key': (n, e), 'private_key': (n, d)} #(n, e), (n, d)

def encrypt(public_key:tuple, vector_text:str|list) -> dict:
    '''Encrypt text using public key (n, e), fomular: c = m^e mod n.'''
    n, e = public_key
    if isinstance(vector_text, str):
        vector_text = cvt_text2list(vector_text)
    vector_encrypt = [(pow(num, e, n)) for num in vector_text]
    return {'vector': vector_encrypt, 'text': cvt_list2text(vector_encrypt)}

def decrypt(private_key:tuple, vector_text:str|list) -> dict:
    '''Decrypt text using private key (n, d), fomular: m = c^d mod n.'''
    n, d = private_key
    if isinstance(vector_text, str):
        vector_text = cvt_text2list(vector_text)
    vector_decrypt = [(pow(num, d, n)) for num in vector_text]
    return {'vector': vector_decrypt, 'text': cvt_list2text(vector_decrypt)}

if __name__ == '__main__':
    gen = generate_key_pair()
    u_key, r_key = gen['public_key'], gen['private_key']
    message = 'hello'
    print(f'Public key (n, e): {u_key}')
    print(f'Private key (n, d): {r_key}')
    print(f'Message: {message}')

    print('\n'+'-'*10+'Encrypt'+'-'*10)
    en = encrypt(u_key, message)
    print(f'Vector: {en["vector"]}')
    print(f'Text: {en["text"]}')

    print('\n'+'-'*10+'Decrypt'+'-'*10)
    de = decrypt(r_key, en['vector'])
    print(f'Vector: {de["vector"]}')
    print(f'Text: {de["text"]}')