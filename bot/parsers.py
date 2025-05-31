## PARSERS

#------------------------------------------------------Add Parser--------------------------------------------------------#
#This is parsing — taking unstructured user input and converting it into structured values your bot can use safely.

def parse_add_command(text):
    def get_parts(parts, index):
        if len(parts) > index:
            value = parts[index].strip()
            return value if value else None
        return None
            
    parts = [part.strip() for part in text.split('|')]  #split always creates a list, so we had a raw string
    #now parts = ["ingewikkeld", "complicated",  "Flikken", "tricky situation"] is another cleared list, without | and whitespaces
        
    user_dutch_word = get_parts(parts, 0)
    user_english_word = get_parts(parts,1 )
    user_source = get_parts(parts, 2)   
    user_comment  = get_parts(parts, 3)
    user_example_sentence = get_parts(parts, 4)
        
    return user_dutch_word, user_english_word, user_source, user_comment, user_example_sentence
        # it gives us a tuple of values ,for example ("ingewikkeld", "complicated", "Flikken", "tricky case", "De situatie is ingewikkeld.")


#------------------------------------------------------Edit Parser--------------------------------------------------------#
def parse_edit_command(text):
    """
    Parses the input text for the /edit command.
    Splits the text by '|' and returns the word to edit, the field, and the new value.
    """
    parts = [part.strip() for part in text.split('|')]

    if len(parts) < 3:
        return None, None, None  # Not enough parts to proceed

    word_to_edit = parts[0]
    field_to_edit = parts[1].lower()
    new_value = parts[2]

    return word_to_edit, field_to_edit, new_value