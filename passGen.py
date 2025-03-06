import secrets
import string

def gen(length, low, up, dig, symb):
    lower = list(string.ascii_lowercase)
    upper = list(string.ascii_uppercase)
    digits = list(string.digits)
    symbols = list('!#$%&()*^')

    pwd_list = []

    if low:
        pwd_list.append(secrets.choice(lower))

    if up:
        pwd_list.append(secrets.choice(upper))
        
    if dig:
        pwd_list.append(secrets.choice(digits))
        
    if symb:
        pwd_list.append(secrets.choice(symbols))

    remaining_length = length - len(pwd_list)
    
    if remaining_length>0:
        act_categ = []

        if low:
            act_categ.append(lower)

        if up:
            act_categ.append(upper)
            
        if dig:
            act_categ.append(digits)
            
        if symb:
            act_categ.append(symbols)
        
        pwd_list.extend(secrets.choice(secrets.choice(act_categ)) 
                        for _ in range(remaining_length))

    secrets.SystemRandom().shuffle(pwd_list)

    return ''.join(secrets.choice(pwd_list) for _ in range(length))