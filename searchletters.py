def searchletters(phrase:str,letters:str="aeoiu") -> set:
    return set(letters).intersection(set(phrase))
    