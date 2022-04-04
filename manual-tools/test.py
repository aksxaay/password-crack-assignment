import pandas as pd
from hashlib import sha256

def dictionary_attack(dictionary_word,target_hash):
    pass_bytes = dictionary_word.encode('utf-8')
    pass_hash = sha256(pass_bytes)
    digest = pass_hash.hexdigest()
    if digest == target_hash:
        return True

if __name__ == "__main__":
    # read user DB and the dictionary using pandas.read_csv
    dictionary = pd.read_csv("password_dictionary", names=['passwords'])
    users = pd.read_csv("users")
    
    # match all words from the dictionary until it matches/ends
    for test_word in dictionary["passwords"]:
        if dictionary_attack(test_word,users["password_hash"][0]) == True:
            print("Matched Password: ", test_word)
            break
        else:
            continue

# inputs an string and returns the sha256 digest
def create_hash(word):
    pass_bytes = word.encode('utf-8')
    pass_hash = sha256(pass_bytes)
    digest = pass_hash.hexdigest()
    return digest

# inputs the number of users and returns nothing
# intended for finding passwords for multiple users
def find_multiple_users(num_user):
    for i in range(num_user):
        check_pass = users["password_hash"][i]
        for test_word in dictionary["passwords"]:
            if create_hash(test_word) == check_pass:
                print("Found Matched Password:", test_word, "for user", users["username"][i])
                break