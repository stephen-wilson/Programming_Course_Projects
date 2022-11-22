# NO ADDITIONAL IMPORTS!
import doctest
from text_tokenize import tokenize_sentences


class PrefixTree:
    def __init__(self):
        self.value = None
        self.children = {}
        
    # def recursively_set_val(tree, key, value):
    #     if 
    
    # def __repr__(self) -> str:
    #     current = self
    #     print('root: ' + self.value)
    #     if not current.children:
    #         return
    #     for k, v in current.children:
    #         # print(f'k: {k}  v: {v}')
    #         to_print = f'k: {k}  v: {v}'
    #         if v is not None:
    #             print(v)
    # def valid_key(self,key):
    #     if type(key) is not str:
    #         raise TypeError

    def find_k(self,key):
        """
        Find and return the tree at end of the key.
        """
        # check if key valid
        if type(key) is not str:
            raise TypeError
        if len(key) == 0:
            return self
        
        first = key[0]
        rest = key[1:]
        if first not in self.children:
            return None
        return self.children[first].find_k(rest)
    
    def set_k(self,key, value):
        """
        Follow the prefixes and set the value at the end of the key. Doesn't return anything
        """
        # start at root
        # if key[0] in children of root, follow that path (recursively)
        # if key[0] not in the children, create add to the children first and set new prefix tree
        # base: if len key == 0, set value at the node to the value
        
        if len(key) == 0:
            self.value = value
        else:
            first = key[0]
            rest = key[1:]
            if first in self.children:
                self.children[first].set_k(rest,value)
            else:
                self.children[first] = PrefixTree()
                self.children[first].set_k(rest,value)

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the prefix tree,
        or reassign the associated value if it is already present.
        Raise a TypeError if the given key is not a string.
        """
        # set tree 
        # self.valid_key(key)
        # current = self
        # while len(key) > 0:
        #     current.children[key[0]] = PrefixTree()
        #     current = current.children[key[0]]
        #     key = key[1:]

        # if len(key) == 0:
        #     current.value = value
        node = self.find_k(key)
        if node == None:
            # current = self
            # while len(key) > 0:
            #     current.children[key[0]] = PrefixTree()
            #     current = current.children[key[0]]
            #     key = key[1:]

            # if len(key) == 0:
            #     current.value = value
            self.set_k(key, value)
        else:
            node.value = value
            
            
    def __getitem__(self, key):
        """
        Return the value for the specified prefix.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        # if type(key) is not str:
        #     raise TypeError
        node = self.find_k(key)
        if node == None:
            raise KeyError
        elif node.value == None:
            raise KeyError
        return node.value

    def __delitem__(self, key):
        """
        Delete the given key from the prefix tree if it exists.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        if key == '':
            raise KeyError
        # if key[:1] == '':
        #     node = self
        # else:
        node = self.find_k(key)
            
        if node == None or node.value == None:
            raise KeyError
        node.value = None
        # del node.children[key[-1]]

    def __contains__(self, key):
        """
        Is key a key in the prefix tree?  Return True or False.
        Raise a TypeError if the given key is not a string.
        """
        node = self.find_k(key)
        if node == None:
            return False
        
        return node.value is not None

    def recursive_iter(self, key=''):
        if self.value is not None:
            yield key, self.value
            
        for child, tree in self.children.items():
            yield from self.children[child].recursive_iter(key+child)
        

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this prefix tree
        and its children.  Must be a generator!
        """
        yield from self.recursive_iter()


def word_frequencies(text):
    """
    Given a piece of text as a single string, create a prefix tree whose keys
    are the words in the text, and whose values are the number of times the
    associated word appears in the text.
    
    >>> t = word_frequencies("bat bat bark bar")
    >>> list(t)
    [('bat', 2), ('bar', 1), ('bark', 1)]
    
    """
    words = tokenize_sentences(text)
    # print(words)
    words = ' '.join(words)
    # print(words)
    words = words.split(' ')
    # print(words)
    freq_dict = {}
    # get the word frequencies
    for word in words:
        freq_dict[word] = freq_dict.get(word, 0) + 1
        
    # create Trie instance
    t = PrefixTree()
    for word, freq in freq_dict.items():
        t[word] = freq
    return t
    
        


def autocomplete(tree, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is not a string.
    
    >>> t = word_frequencies("bat bat bark bar")
    >>> autocomplete(t, "ba", 1)
    ['bat']
    >>> autocomplete(t, "ba", 2)
    ['bark', 'bat']
    >>> autocomplete(t, "ba", None)
    ['bat', 'bar', 'bark']
    """
    start_tree = tree.find_k(prefix)
    if start_tree == None or max_count == 0:
        return []
    
    # trivial case: if max_count None, just return all the keys starting from prefix
    if max_count == None:
        return [prefix + word for word, freq in start_tree]
    
    # otherwise:
    # once you have start location, iterate over every key, value from that location, sort and take top max_count
    # is efficient because you are only iterating over the values in the branches where the prefix is you're looking at
    word_freqs = []
    for word, freq in start_tree:
        word_freqs.append((prefix + word, freq))
        
    # sort by frequency (index 1), ascending order
    word_freqs = sorted(word_freqs, key=lambda x: x[1])
    
    # return the words of the max_count highest frequency, all if there are less than max_count available
    return [word for word, freq in word_freqs[-max_count:]]

def autocorrect(tree, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    
    4 autocorrect cases:
    1. A single-character insertion (add any one character in the range "a" to "z" at any place in the word)
    2. A single-character deletion (remove any one character from the word)
    3. A single-character replacement (replace any one character in the word with a character in the range a-z)
    4. A two-character transpose (switch the positions of any two adjacent characters in the word)
    
    Have something that works first, then try to optimize if necessary.
    """
    auto_comp = autocomplete(tree, prefix, max_count)
    # trivial case
    if max_count is not None and len(auto_comp) == max_count:
        return auto_comp
    
    # # master list
    # valid_edits = []
    # use a set to ensure no duplicates
    valid_edits_set = set()
    letters = 'abcdefghijklmnopqrstuvwxyz'
    # case 1: insertion
    # for each letter, add it to each position in the word, checking if it's a prefix
    for c in letters:
        for i in range(len(prefix)):
            temp = prefix[:i] + c + prefix[i:]
            if temp in tree:
                valid_edits_set.add((temp, tree[temp]))
                
            # case 3: replacement
            if i == len(prefix) - 1:
                temp = prefix[:i] + c
            else:
                temp = prefix[:i] + c + prefix[i+1:]
            if temp in tree:
                valid_edits_set.add((temp, tree[temp]))
                
    # case 2: deletion
    for i in range(len(prefix)):
        if i == len(prefix) - 1:
            temp = prefix[:i]
        else:
            temp = prefix[:i] + prefix[i+1:]
        if temp in tree:
            valid_edits_set.add((temp, tree[temp]))
            
        # case 4: transpose
        if i < len(prefix) - 1:
            temp = prefix[:i] + prefix[i+1] + prefix[i] + prefix[i+2:]
        if temp in tree:
            valid_edits_set.add((temp, tree[temp]))
            
    all_suggestions = set(auto_comp)
    # if the max count is None, just add all the valid sets to the auto completed ones and return it
    if max_count is None:
        for word, freq in valid_edits_set:
            all_suggestions.add(word)
        return list(all_suggestions)
    
    valid_edits = sorted(list(valid_edits_set), key=lambda x: x[1])
    # sort by highest frequency, while you haven't added max_count - len(auto_comp), add starting from top ones
    # if word already in all_suggestions don't add it (covered by using a set, then coverting to list at the end)
    while len(all_suggestions) < max_count:
        current = valid_edits.pop()
        if current[0] not in all_suggestions:
            all_suggestions.add(current[0])
            
    return list(all_suggestions)

def recursive_match(tree, pattern, out_list=[]):
    """
    Recursive search function to match the pattern.
    """
    # base case:
    if len(pattern) == 0:
        # if value of Tree is not None it is a valid path so return successful base case
        if tree.value is not None:
            return ['']
        else: 
            return [] # or none; failed base case
    
    # alpha = "abcdefghijklmnopqrstuvwxyz"
    first = pattern[0]
    rest = pattern[1:]
    out_list = []
    
    # output = ''
    # if (first == '*' or first == '?') or tree.find_k(first):
    #     if first == '?':
    #         for c in alpha:
    #             pass
    #     output += first
    #     return output + recursive_match(tree, rest)
    
    # go through each child
    if first == '*':
        pass
    # go through each child
    elif first == '?':
        for child in tree.children: 
            pass     
    else:
        if first in tree.children:
            return [first + others for others in recursive_match(tree.children[first], rest)]
            out_list += first + recursive_match(tree.children[first], rest)
    pass

def word_filter(tree, pattern):
    """
    Return list of (word, freq) for all words in the given prefix tree that
    match pattern.  pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
         
    >>> word_filter(t, "*")
    [('bat', 2), ('bar', 1), ('bark', 1)]
    >>> word_filter(t, "???")
    [('bat', 2), ('bar', 1)]
    >>> word_filter(t, "*r*")
    [('bar', 1), ('bark', 1)]
    """
    # use recursive search function
    return recursive_match(tree, pattern)


# you can include test cases of your own in the block below.
if __name__ == "__main__":
    print(word_filter(word_frequencies("bat bat bark bar"), 'at'))
        
    with open("C:\\Users\\colos\\OneDrive - Massachusetts Institute of Technology\\Sophomore\\6.1010\\Labs\\Lab 8\\autocomplete\\dracula.txt", encoding="utf-8") as f:
        text = f.read()
    t = word_frequencies(text)
    distinct = 0
    total = 0
    for word, freq in t:
        distinct += 1
        total += freq
    print(distinct)
    print(total)
    
    # print(autocorrect(t, 'hear', None))
    
    # doctest.testmod()
    # t = PrefixTree()
    # print(t)
    # t['bat'] = 7
    # print(t.children['b'].children['a'].children)
    # t['bark'] = ':)'
    # print(t.children['b'].children['a'].children)
    # t['bar'] = 3
    # print(t.children['b'].children['a'].children['r'].children)

    # print(t['bark'])
    # print(t['bat'])
    # print(t['bar'])
    
    # del t['bar']
    # # t['bar']
    # # del t['bar']
    # # t['bar']
    # print(repr(''[:-1]))
    
    # print('bar' in t)
    # print('bark' in t)
    
    # for k, v in t:
    #     print(k)
    # print(list(t))
    
    # # print(autocomplete(word_frequencies('a man at the market murmered that he had met a mermaid. '
    # #                        'mark didnt believe the man had met a mermaid.'), 'm', 4))
    # print(repr("hi"[:0]))