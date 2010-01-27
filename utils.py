from BeautifulSoup import BeautifulSoup, Tag, NavigableString

def enumerate_paras(html, speech=None):
    "Adds 'id=pX' to each paragraph"
    soup = BeautifulSoup(html)
    paras = soup.findAll('p')
    
    for i, p in enumerate(paras):
        p['id'] = "p%s" % i
        if speech:
            notes = speech.footnotes.filter(index=i)
            if notes:
                count = notes.count()
                a = Tag(soup, 'a')
                a['class'] = 'note-link %s' % notes[0].note_type.slug
                a['href'] = '#i%s' % i
                if count > 1:
                    text = NavigableString('%s Responses' % count)
                else:
                    text = NavigableString('1 Response')
                a.insert(0, text)
                p.append(a)
        
    return soup.prettify()
