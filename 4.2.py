#palindromy
p_pali = "kajak"

def palindrom(p_pali):
    p_pali=p_pali.lower().replace(' ','')
    odwslo = ''
    
    for i in range (len(p_pali),0,-1):
        odwslo +=p_pali[i-1]
    return p_pali==odwslo
     
test = palindrom(p_pali)
print(test)