def generate_hashtag(s):
    hash_string ="#"+ ("".join(word.strip().capitalize() for word in s.split()))
    if len(hash_string)==1 or len(hash_string)>140:
        return False
    return hash_string



#print(generate_hashtag(" Hello there thanks for trying my Kata"))
print(generate_hashtag(" "))