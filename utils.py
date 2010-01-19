from BeautifulSoup import BeautifulSoup

def enumerate_paras(html):
    "Adds 'id=pX' to each paragraph"
    soup = BeautifulSoup(html)
    paras = soup.findAll('p')
    
    for i, p in enumerate(paras):
        p['id'] = "p%s" % i
        
    return soup.prettify()