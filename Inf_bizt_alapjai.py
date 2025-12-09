import random
import math
#Kibővített Euklideszi algoritmus
def extended_gcd(a,b):
    if b==0:
        return a,1,0
    else:
        gcd,x1,y1=extended_gcd(b,a%b)
        x=y1
        y=x1-(a//b)*y1
        return gcd,x,y

#Moduláris multiplikativ inverz
def mod_inverse(a,m):
    gcd,x,y=extended_gcd(a,m)
    if gcd!=1:
        raise Exception("Nincs inverz, nem relatív prímek.")
    return x%m

#Gyorshatványozás
def mod_exp(base,exp,mod):
    result=1
    base=base%mod
    while exp>0:
        if exp%2==1:
            result=(result*base)%mod
        exp=exp//2
        base=(base*base)%mod
    return result

#Miller-Rabin prímteszt
def miller_rabin_test(n,k=10):
    if n==2 or n==3: return True
    if n%2==0 or n<2: return False

    r,d=0,n-1
    while d%2==0:
        r+=1
        d=d//2

    for _ in range(k):
        a=random.randint(2,n-2)
        x=mod_exp(a,d,n)
        if x==1 or x==n-1:
            continue
        for _ in range(r-1):
            x=mod_exp(x,2,n)
            if x==n-1:
                break
        else:
            return False
    return True

#Prímek generálása
def generate_prime(bits=32):
    while True:
        candidate=random.getrandbits(bits)
        candidate|=1
        if miller_rabin_test(candidate):
            return candidate

#Kínai maradéktétel
def crt_decrypt_sign(c,p,q,d):
    dp=d%(p-1)
    dq=d%(q-1)

    m_p=mod_exp(c,dp,p)
    m_q=mod_exp(c,dq,q)

    q_inv_p=mod_inverse(q,p)
    p_inv_q=mod_inverse(p,q)

    term_1=m_p*q*q_inv_p
    term_2=m_q*p*p_inv_q

    m=(term_1+term_2)%(p*q)

    return m

#q és p generálása
def rsa_keygen(bits=64):
    print("RSA kulcsgenerálás folyamatban...")
    p=generate_prime(bits)
    q=generate_prime(bits)
    while p==q:
        q=generate_prime(bits)

    n=p*q
    phi_n=(p-1)*(q-1)

    e=65537
    if math.gcd(e,phi_n)!=1:
        e=3
        while math.gcd(e,phi_n)!=1:
            e+=2
    #Privát kulcs generálása
    d=mod_inverse(e,phi_n)

    print(f"p:{p},q:{q}")
    print(f"Nyilvános kulcs (e,n):({e},{n})")
    print(f"Privát kulcs (d,n):({d},{n})")
    print("-"*100)
    return p,q,e,n,d


if __name__=="__main__":

    p,q,e,n,d=rsa_keygen(bits=64)
    print(f"n={n}")
    print("-"*100)
    while True:
        try:
            msg_input=int(input(f"Írjon be egy titkosítani kívánt üzenetet (számot), ami kisebb mint {n}.:"))
            if msg_input>=n:
                print(f"Az üzenet túl nagy, kérem próbálkozzon kisebbel mint {n}.")
                continue
            break
        except ValueError:
            print("Csak számot adhat meg.")
    #Üzenet titkosítás
    encrypted_msg=mod_exp(msg_input,e,n)
    print(f"Titkosított üzenet:{encrypted_msg}")
    #Üzenet visszafejtés
    decrypted_msg=crt_decrypt_sign(encrypted_msg,p,q,d)
    print(f"Visszafejtett üzenet:{decrypted_msg}")
    #Üzenet aláírás
    signature=crt_decrypt_sign(msg_input,p,q,d)
    print(f"Digitális aláírás:{signature}")

    verified_msg=mod_exp(signature,e,n)
    print(f"Ellenőrzött aláírás:{verified_msg}")
    print()
    #Aláírás ellenőrzés
    if verified_msg==msg_input:
        print("Az aláírás érvényes.")
    else:
        print("Az aláírás NEM érvényes.")