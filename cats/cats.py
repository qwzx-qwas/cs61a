"""Typing test implementation"""

from utils import (
    lower,
    split,
    remove_punctuation,
    lines_from_file,
    count,
    deep_convert_to_tuple,
)
from ucb import main, interact, trace
from datetime import datetime
import random


###########
# Phase 1 #
###########


def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which the SELECT function returns True.
    If there are fewer than K such paragraphs, return an empty string.

    Arguments:
        paragraphs: a list of strings representing paragraphs
        select: a function that returns True for paragraphs that meet its criteria
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    #从符合select的段落中选取第k个段落，没有则返回''
    tmp = [None] * len(paragraphs)#学会了初始化一个clone列表，元素全为None，长度为len
                                   #对比[]*len(),由于[]乘任何数还是为[],长度没有改变
    j = 0
    for i in paragraphs:
        if select(i):
            tmp[j] = i
            j += 1  

    length = len(tmp)
    if k < 0 or k >= length: 
        return ''
    else:
        return tmp[k] if tmp[k] is not None else ''

    # END PROBLEM 1
    


def about(keywords):
    """Return a function that takes in a paragraph and returns whether
    that paragraph contains one of the words in keywords.

    Arguments:
        keywords: a list of keywords

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in keywords]), "keywords should be lowercase."

    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def check(paragraphs):
        #检查是否为字符串，是则转化为单元素列表
        if isinstance(paragraphs, str):
            paragraphs = [paragraphs]
        word_list =[]
        for s in paragraphs:
            cleaned = remove_punctuation(s)
            #分割
            words = cleaned.split()
            #小写
            lower_word = [word.lower() for word in words]
            #仅当w为非空元素时保留
            word_list.extend(lower_word)#将 lower_word 列表中的所有元素逐个添加到 word_list 的末尾,
                                        #而不是将整个 lower_word 列表作为单个元素加入
        return any(word in keywords for word in word_list)
            
    
    return check

    # END PROBLEM 2


def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    compared to the corresponding words in SOURCE.

    Arguments:
        typed: a string that may contain typos
        source: a model string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    source_words = split(source)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    score = 0.0
    correct = 0

    length1 = len(typed_words)
    length2 = len(source_words)

    def check_strings(length,correct):
        for i in range(length):
            if typed_words[i] == source_words[i]:
                correct += 1
            
        return correct
    
    if not source_words:
        return 100.0 if not typed_words else 0.0
    if not typed_words:
        return 0.0
    length = min(length1,length2)
    
    #多了仍然100.0
    correct = check_strings(length,correct)

    score = score + (correct/length1)*100.0

    return max(0.0,min(score,100.0))       

    
    
    
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, "Elapsed time must be positive"
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    length = len(typed)
    length = length / 5
    time = length * (60 / elapsed)
    return time
    # END PROBLEM 4


################
# Phase 4 (EC) #
################


def memo(f):
    """A general memoization decorator."""
    cache = {}

    def memoized(*args):
        immutable_args = deep_convert_to_tuple(args)  # convert *args into a tuple representation
        if immutable_args not in cache:
            result = f(*immutable_args)
            cache[immutable_args] = result
            return result
        return cache[immutable_args]

    return memoized


def memo_diff(diff_function):
    """A memoization function."""
    cache = {}

    def memoized(typed, source, limit):
        # BEGIN PROBLEM EC
        "*** YOUR CODE HERE ***"
        # END PROBLEM EC

    return memoized


###########
# Phase 2 #
###########


def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD based on DIFF_FUNCTION. If multiple words are tied for the smallest difference,
    return the one that appears closest to the front of WORD_LIST. If the
    lowest difference is greater than LIMIT, return TYPED_WORD instead.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    #word_list中的每个字符串都分别输入到diff_funcyion中，与typed_list比较
    value2 = [None]*len(word_list)
    value1 = [None]*len(word_list)
    i = 0
    for string in word_list:
        if string == typed_word:
            return typed_word
        else:
            current_value = diff_function(typed_word,string,limit)
            value1[i] = abs(current_value)
            value2[i] = string
            i += 1
    
    min_value = min(value1)  
    if min_value > limit:
        return typed_word
    else: 
        min_index = value1.index(min_value)

        return value2[min_index]
                
    # END PROBLEM 5


def furry_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths to this value and returns the result.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> furry_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> furry_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> furry_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> furry_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> furry_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    #assert False, 'Remove this line'
    a = typed
    b = source
    count = 0
    def fixes_check(a,b,count):

        length = min(len(a),len(b))

        if length < 1 or count > limit:
            return count + abs(len(typed) - len(source))
        else:
            if a[0] != b[0]:
                count += 1
            return fixes_check(a[1:],b[1:],count)        
        
        
    return fixes_check(a,b,count)
    # END PROBLEM 6


def minimum_mewtations(typed, source, limit):
    """A diff function for autocorrect that computes the edit distance from TYPED to SOURCE.
    This function takes in a string TYPED, a string SOURCE, and a number LIMIT.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of edits

    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    #assert False, 'Remove this line'
    #两字符串相等直接返回0
    #为空的情况
    if  not typed :
        return len(source)
    if not source :
        return len(typed)
    if typed == source: # Base cases should go here, you may add more base cases as needed.
        # BEGIN
        "*** YOUR CODE HERE ***"
        return 0
        # END
    # Recursive cases should go below here
    #两字符串超过limit,返回一个大于limit的值
    if abs(len(typed) - len(source) > limit) : # Feel free to remove or add additional cases
        # BEGIN
        "*** YOUR CODE HERE ***"
        return limit + 1
    if limit < 0:
        return limit + 1
    #当字符串当前位置与source不同，但是后面一样
    if typed[0] == source[0]:
        return  minimum_mewtations(typed[1:],source[1:],limit)

    
        # END
    else:
        add = 1 + minimum_mewtations(typed,source[1:],limit - 1)#并没有真的插入，所以typed仍然是原来的
        remove = 1 + minimum_mewtations(typed[1:],source,limit -1 )
        substitute = 1 + minimum_mewtations(typed[1:],source[1:],limit -1)
        min_cost = min(add,remove,substitute)

        
        # BEGIN
        "*** YOUR CODE HERE ***"
        return min_cost if min_cost <= limit else limit    
        # END


# Ignore the line below
minimum_mewtations = count(minimum_mewtations)


def final_diff(typed, source, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""
    assert False, "Remove this line to use your final_diff function."


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(typed, source, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        source: a list of the words in the typing source
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> source = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, source, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], source, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    a = typed
    b = source
    i = 0
    
    def check(a,b):
        for i in range((len(a))):
            if a[i] != b[i]:
                return i
        return i + 1
    if not a :
        if not b:
            progress = 100.0
        else:
            progress = 0.0
    elif not b:
        progress = 0

    elif a[0] != b[0]:
        progress = 0.0
    else:
        i = check(a,b)
        progress = (i) / len(source)

    print_progress = lambda d:print('ID:', d['id'], 'Progress:', d['progress'])            

    data = {'id':user_id,'progress':progress}        
    print_progress(data)

    return progress
    # END PROBLEM 8


def time_per_word(words, timestamps_per_player):
    """Return a dictionary {'words': words, 'times': times} where times
    is a list of lists that stores the durations it took each player to type
    each word in words.

    Arguments:
        words: a list of words, in the order they are typed.
        timestamps_per_player: A list of lists of timestamps including the time
                          each player started typing, followed by the time each
                          player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> result = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> result['words']
    ['collar', 'plush', 'blush', 'repute']
    >>> result['times']
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    tpp = timestamps_per_player  # A shorter name (for convenience)
    # BEGIN PROBLEM 9
    for player in timestamps_per_player:
        if len(player) != len(words) + 1:
            raise ValueError
    times = [] 
    #times = [[] for _ in range(len(tpp))]  # 每个玩家对应独立的空列表
    for i in range(len(tpp)):
        player_times = []
        for j in range(len(words)):
            #times[i][j] = tpp[i][j + 1] - tpp[i][j]
            start = timestamps_per_player[i][j]
            end = timestamps_per_player[i][j + 1]
            player_times.append(end - start)
        times.append(player_times)#并非直铺元素，而是生成嵌套列表
    # END PROBLEM 9
    return {'words': words, 'times': times}



def fastest_words(words_and_times):
    """Return a list of lists indicating which words each player typed fastest.
    In case of a tie, the player with the lower index is considered to be the one who typed it the fastest.

    Arguments:
        words_and_times: a dictionary {'words': words, 'times': times} where
        words is a list of the words typed and times is a list of lists of times
        spent by each player typing each word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words({'words': ['Just', 'have', 'fun'], 'times': [p0, p1]})
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    check_words_and_times(words_and_times)  #验证输入格式是否正确 verify that the input is properly formed
    words, times = words_and_times['words'], words_and_times['times']
    player_indices = range(len(times))  # 玩家索引列表（序号）contains an *index* for each player
    word_indices = range(len(words))    # （每个单词的位置）contains an *index* for each word
    # BEGIN PROBLEM 10
    result = [[] for _ in range(len(player_indices))]#创建一个二维列表，内列表个数代表玩家数

    for i in word_indices:
        min_time = None#无效值用于初始化
        fast_player = -1
        for j in player_indices:
            time = get_time(times,j,i)#二维列表，返回j玩家在i单词的时间
            if min_time == None or min_time > time:
                min_time = time
                fast_player = j
        result[fast_player].append(words[i])
    
    return result


    # END PROBLEM 10


def check_words_and_times(words_and_times):
    """Check that words_and_times is a {'words': words, 'times': times} dictionary
    in which each element of times is a list of numbers the same length as words.
    """
    assert 'words' in words_and_times and 'times' in words_and_times and len(words_and_times) == 2
    words, times = words_and_times['words'], words_and_times['times']
    assert all([type(w) == str for w in words]), "words should be a list of strings"
    assert all([type(t) == list for t in times]), "times should be a list of lists"
    assert all([isinstance(i, (int, float)) for t in times for i in t]), "times lists should contain numbers"
    assert all([len(t) == len(words) for t in times]), "There should be one word per time."


def get_time(times, player_num, word_index):
    """Return the time it took player_num to type the word at word_index,
    given a list of lists of times returned by time_per_word."""
    num_players = len(times)
    num_words = len(times[0])
    assert word_index < len(times[0]), f"word_index {word_index} outside of 0 to {num_words-1}"
    assert player_num < len(times), f"player_num {player_num} outside of 0 to {num_players-1}"
    return times[player_num][word_index]


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file("data/sample_paragraphs.txt")
    random.shuffle(paragraphs)
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print("No more paragraphs about", topics, "are available.")
            return
        print("Type the following paragraph and then press enter/return.")
        print("If you only type part of it, you will be scored only on that part.\n")
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print("Goodbye.")
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print("Words per minute:", wpm(typed, elapsed))
        print("Accuracy:        ", accuracy(typed, source))

        print("\nPress enter/return for the next paragraph or type q to quit.")
        if input().strip() == "q":
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse

    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument("topic", help="Topic word", nargs="*")
    parser.add_argument("-t", help="Run typing test", action="store_true")

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)