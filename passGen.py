import secrets
import string

def passGen(length, low, up, dig, symb):
    lower = list(string.ascii_lowercase)
    upper = list(string.ascii_uppercase)
    digits = list(string.digits)
    symbols = list(string.punctuation)

    pwdList = []

    lowRand = [secrets.choice(lower) for _ in range(length//4)]
    upperRand = [secrets.choice(upper) for _ in range(length//4)]
    digitsRand = [secrets.choice(digits) for _ in range(length//4)]
    symbolsRand = [secrets.choice(symbols) for _ in range(length//4)]

    if low:
        pwdList += lowRand
        
    if up:
        pwdList += upperRand
        
    if dig:
        pwdList += digitsRand
        
    if symb:
        pwdList += symbolsRand

    secrets.SystemRandom().shuffle(pwdList)
    
    pwd = ''.join(secrets.choice(pwdList) for _ in range(length))

    return pwd