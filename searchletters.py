def searchletters(phrase:str,letters:str="aeoiuAEOIU") -> set:
    return set(letters).intersection(set(phrase))
    
