Password cracking through Bruteforcing may take a long time and most of the users usually use common English words or names, and numbers as their passwords. Therefore, Dictionary attacks can be quite useful to crack the passwords.

A dictionary is a simple txt file that may contain from a few thousands to a few millions of common words or phrases (includes numbers as well).

If you have a stolen user credential database, you might be able to crack the passwords by matching all dictionary words against the hashed passwords!

A Hash is typically a one-way function that creates a unique digest from an input string. For example, if your password is hello_there, the output hash digest would look like the following

```Algorithm	Output Hash
MD5	290e1c9cc54995453b810dfb15b853a1
SHA-1	f976f0ad02501f0a95bfcf3c1081e0759b508d47
SHA-256	299d2e40d6b7026b6029b8ff4cff0ad0fbfe14b20d704a609a2631cada32fbc1```
Here, MD5, SHA-1, and SHA-256 are widely used hashing algorithms to convert a string into a one-way output.

The term one-way means you cannot retrive the string from the hashed output. It is important to hash the passwords because we do not want to keep passwords in plain sight.

If you are logging into your social media account (e.g., Facebook/Instagram) or your laptop, you have to input your username and password. However, the systems maintain a user database containing your name and the hashed password. For example,

```user_name	password_hash
mrx	678cfd979de6de0ec70d08b0b7a4b6aad645802abe2504aed9c4d1ca3da101c5
guest_user	3809f08dc16f01a7c9393eab3146e38e7ffd7d19b0aa5a3754aa2f7780fc4b77
other	b712430498d0b31595b86c34a939b4dcdde5050a4e8a143e99037a6e6984a68f```
Now, suppose, you have stolen/found a user credential database like this. However, because you cannot calculate the string, you need to match different guessed strings after hashing.

Requirements
Stolen User Credential Database (two columns: username, password_hash)
A dictionary file (each line contains a dictionary word)
Attacker should know which algorithm is being used. Although it???s not a big deal. The attacker can try all algorithms one after another. In this post we will use SHA-256
Create a simple Python Program
First, let???s import the necessary modules

import pandas as pd
from hashlib import sha256
Now, we need to write a function that returns True if the hashed dictionary word matches the database password

```def dictionary_attack(dictionary_word,target_hash):
    pass_bytes = dictionary_word.encode('utf-8')
    pass_hash = sha256(pass_bytes)
    digest = pass_hash.hexdigest()
    if digest == target_hash:
        return True```
Suppose, we want to check whether we can crack the password of the first user. Therefore, we need to get the first password_hash from the user database, and pass all the dictionary words one after another.

```if __name__ == "__main__":
    # read user DB and the dictionary using pandas.read_csv
    dictionary = pd.read_csv("password_dictionary", names=['passwords'])
    users = pd.read_csv("users")
    
    # match all words from the dictionary until it matches/ends
    for test_word in dictionary["passwords"]:
        if dictionary_attack(test_word,users["password_hash"][0]) == True:
            print("Matched Password: ", test_word)
            break
        else:
            continue```
Now, within a few seconds, we get a matched word from our dictionary: 2midrash.

Well, if you want to compromise all user password, you can add a new for loop that iterates over the indices of all users. Or for any range of user, you can create a function like this and call it in the main function.

# inputs an string and returns the sha256 digest
```def create_hash(word):
    pass_bytes = word.encode('utf-8')
    pass_hash = sha256(pass_bytes)
    digest = pass_hash.hexdigest()
    return digest```

# inputs the number of users and returns nothing
# intended for finding passwords for multiple users
```
def find_multiple_users(num_user):
    for i in range(num_user):
        check_pass = users["password_hash"][i]
        for test_word in dictionary["passwords"]:
            if create_hash(test_word) == check_pass:
                print("Found Matched Password:", test_word, "for user", users["username"][i])
                break
```
However, the code we used above is enefficient while calculating for multiple users. Can you guess, why?

Because we are creating hash each time we match against the user database passwords. So, if we try 20000 dictionary words againt 20 user passwords, the number of hashing calculation would be 20000*20.

To avoid the additional computation, we can precompute the hash and keep those values in a dictionary. The new dictionary will have the dictionary words as keys and the hashed outputs will be the values. Therefore, we can add an extra function to the code as follows

```# Returns the dictionary of password and corresponding digests
def hash_dictionary():
    global hash_dict
    hash_dict = {}
    for test_word in dictionary["passwords"]:
        hash_dict[test_word] = create_hash(test_word)
    return hash_dict
```

### Explanations

**Variables**
`dictionary` - list of passwords
`users` - username,password_hash
`users_salted` - username,salt,password_hash

there's atleast *64849* users

salt is unique, random string of characters known to only the site before it's hashed.

`create_hash(word)` creates hash of input word

`salted_hash(salt, password)` hashes them together. (salt + pass)

`hash_dictionary` - dictionary of `dictionary` passwords hashed so unique


**Experiments**
1 => 
- time taken to match 1 result to freshly created hash.


2 => 
- avg time for 10 users


3 =>
- time taken if used precomputed hash


4 =>
shows why we use unique salt.

- key, value pairs in duplicates using `collections.Counter()`
- lookout for `A-Jai` and `Hagop`