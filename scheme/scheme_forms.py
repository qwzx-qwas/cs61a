from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

#################
# Special Forms #
#################

# Each of the following do_xxx_form functions takes the cdr of a special form as
# its first argument---a Scheme list representing a special form without the
# initial identifying symbol (if, lambda, quote, ...). Its second argument is
# the environment in which the form is to be evaluated.

def do_define_form(expressions, env):
    """Evaluate a define form.
    >>> env = create_global_frame()
    >>> do_define_form(read_line("(x 2)"), env) # evaluating (define x 2)
    'x'
    >>> scheme_eval("x", env)
    2
    >>> do_define_form(read_line("(x (+ 2 8))"), env) # evaluating (define x (+ 2 8))
    'x'
    >>> scheme_eval("x", env)
    10
    >>> # problem 10
    >>> env = create_global_frame()
    >>> do_define_form(read_line("((f x) (+ x 2))"), env) # evaluating (define (f x) (+ x 8))
    'f'
    >>> scheme_eval(read_line("(f 3)"), env)
    5
    """
    validate_form(expressions, 2) # Checks that expressions is a list of length at least 2
    signature = expressions.first
    if scheme_symbolp(signature):
        # assigning a name to a value e.g. (define x (+ 1 2))
        validate_form(expressions, 2, 2) # Checks that expressions is a list of length exactly 2
        # BEGIN PROBLEM 4
        "*** YOUR CODE HERE ***"
        target = expressions.first #被绑定的参数
        value = scheme_eval(expressions.rest.first,env)#evaluate绑定的内容，即使
        env.define(target,value)#在当前环境绑定变量
        return target
        # END PROBLEM 4
    elif isinstance(signature, Pair) and scheme_symbolp(signature.first):
        # defining a named procedure e.g. (define (f x y) (+ x y))
        # BEGIN PROBLEM 10
        "*** YOUR CODE HERE ***"
        #signature包括name(symbol)和formals(形参列表)
        symbol = signature.first
        formals = signature.rest
        body = expressions.rest
        #由于do_lambda_form只接受两个参数，所以将其合并成一个expression
        lambda_expression = Pair(formals,body)

        current = do_lambda_form(lambda_expression,env)
        env.define(symbol,current) 
        return symbol
        # END PROBLEM 10
    else:
        bad_signature = signature.first if isinstance(signature, Pair) else signature
        raise SchemeError('non-symbol: {0}'.format(bad_signature))

def do_quote_form(expressions, env):
    """Evaluate a quote form.

    >>> env = create_global_frame()
    >>> do_quote_form(read_line("((+ x 2))"), env) # evaluating (quote (+ x 2))
    Pair('+', Pair('x', Pair(2, nil)))
    """
    validate_form(expressions, 1, 1)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if not isinstance(expressions.rest,Pair):
        return expressions.first
    else:
        return expressions 
    # END PROBLEM 5

def do_begin_form(expressions, env):
    """Evaluate a begin form.

    >>> env = create_global_frame()
    >>> x = do_begin_form(read_line("((print 2) 3)"), env) # evaluating (begin (print 2) 3)
    2
    >>> x
    3
    """
    validate_form(expressions, 1)
    return eval_all(expressions, env)

def do_lambda_form(expressions, env):
    """Evaluate a lambda form.

    >>> env = create_global_frame()
    >>> do_lambda_form(read_line("((x) (+ x 2))"), env) # evaluating (lambda (x) (+ x 2))
    LambdaProcedure(Pair('x', nil), Pair(Pair('+', Pair('x', Pair(2, nil))), nil), <Global Frame>)
    """
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    return LambdaProcedure(formals,expressions.rest,env)

    # END PROBLEM 7

def do_if_form(expressions, env):
    """Evaluate an if form.

    >>> env = create_global_frame()
    >>> do_if_form(read_line("(#t (print 2) (print 3))"), env) # evaluating (if #t (print 2) (print 3))
    2
    >>> do_if_form(read_line("(#f (print 2) (print 3))"), env) # evaluating (if #f (print 2) (print 3))
    3
    """
    #验证表达式是否符合if的语法要求：if 表达式必须包含 ​​条件、then 分支​​ 两个必要部分，并可选的
    # ​​else 分支​​（总长度为 2 或 3）。若表达式长度不合法（如少于 2 或超过 3），会抛出错误。
    validate_form(expressions, 2, 3)

    #通过 scheme_eval(expressions.first, env) 对条件部分求值，并使用 is_scheme_true 判断其真值
    if is_scheme_true(scheme_eval(expressions.first, env)):
    #条件为真​​：执行 then 分支，即 scheme_eval(expressions.rest.first, env)，对第二个表达式求值。    
        return scheme_eval(expressions.rest.first, env)
    #条件为假：若有 else 分支（表达式长度为 3），执行 scheme_eval(expressions.rest.rest.first, env)
    # 对第三个表达式求值；若无 else 分支，根据 Scheme 规范返回值未定义（代码中可能返回 None）。
    elif len(expressions) == 3:
        return scheme_eval(expressions.rest.rest.first, env)

def do_and_form(expressions, env):
    """Evaluate a (short-circuited) and form.

    >>> env = create_global_frame()
    >>> do_and_form(read_line("(#f (print 1))"), env) # evaluating (and #f (print 1))
    False
    >>> # evaluating (and (print 1) (print 2) (print 4) 3 #f)
    >>> do_and_form(read_line("((print 1) (print 2) (print 3) (print 4) 3 #f)"), env)
    1
    2
    3
    4
    False
    """
    # BEGIN PROBLEM 12
    "*** YOUR CODE HERE ***"
    if expressions is nil:
        return True
    first_eval = scheme_eval(expressions.first,env)
    if is_scheme_false(first_eval):
        return first_eval 
    else:
        if expressions.rest is nil:
            return first_eval
        else:
            return do_and_form(expressions.rest,env)
    # END PROBLEM 12

def do_or_form(expressions, env):
    """Evaluate a (short-circuited) or form.

    >>> env = create_global_frame()
    >>> do_or_form(read_line("(10 (print 1))"), env) # evaluating (or 10 (print 1))
    10
    >>> do_or_form(read_line("(#f 2 3 #t #f)"), env) # evaluating (or #f 2 3 #t #f)
    2
    >>> # evaluating (or (begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))
    >>> do_or_form(read_line("((begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))"), env)
    1
    2
    6
    """
    # BEGIN PROBLEM 12
    "*** YOUR CODE HERE ***"
    if expressions is nil:
        return False
    first_eval = scheme_eval(expressions.first,env)
    if is_scheme_false(first_eval):
        if expressions.rest is nil:
            return first_eval
        else:
            return do_or_form(expressions.rest,env)
    else:
        return first_eval
    # END PROBLEM 12

def do_cond_form(expressions, env):
    """Evaluate a cond form.

    >>> do_cond_form(read_line("((#f (print 2)) (#t 3))"), create_global_frame())
    3
    """
    while expressions is not nil:
        clause = expressions.first#当前子句
        validate_form(clause, 1)
        if clause.first == 'else':
            test = True
            if expressions.rest != nil:
                raise SchemeError('else must be last')
        else:
            test = scheme_eval(clause.first, env)#求值谓词
        if is_scheme_true(test):
            # BEGIN PROBLEM 13
            "*** YOUR CODE HERE ***"
            if clause.rest is nil:
                return test#返回谓词
            else:
                return eval_all(clause.rest,env)#执行所有结果表达式，返回最后一个
            # END PROBLEM 13
        expressions = expressions.rest
    return None

def do_let_form(expressions, env):
    """Evaluate a let form.

    >>> env = create_global_frame()
    >>> do_let_form(read_line("(((x 2) (y 3)) (+ x y))"), env)
    5
    """
    validate_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.rest, let_env)

def make_let_frame(bindings, env):
    """Create a child frame of Frame ENV that contains the definitions given in
    BINDINGS. The Scheme list BINDINGS must have the form of a proper bindings
    list in a let expression: each item must be a list containing a symbol
    and a Scheme expression."""
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    names = vals = nil
    # BEGIN PROBLEM 14
    "*** YOUR CODE HERE ***"
    #检查name是否重复
    #检查bindings
    #需要将bindings中的symbol以及expr在当前环境下求值，并绑定
    #首先得分离bindings中的symbol以及expr
    #对expr求值（在env下）
    #在当前帧下绑定
    name = val = nil
    current = bindings
    while current is not nil:

        binding = current.first
        validate_form(binding,2,2)    
        name = Pair(current.first.first ,name)
        val = Pair(scheme_eval(current.first.rest.first,env),val)
        current = current.rest
    validate_formals(name)
    def reverse(lst):
        reversed_lst = nil
        while lst is not nil:
            reversed_lst = Pair(lst.first, reversed_lst)
            lst = lst.rest
        return reversed_lst
    
    names = reverse(name)
    vals = reverse(val)
    # END PROBLEM 14
    return env.make_child_frame(names,vals)



def do_quasiquote_form(expressions, env):
    """Evaluate a quasiquote form with parameters EXPRESSIONS in
    Frame ENV."""
    def quasiquote_item(val, env, level):
        """Evaluate Scheme expression VAL that is nested at depth LEVEL in
        a quasiquote form in Frame ENV."""
        if not scheme_pairp(val):
            return val
        if val.first == 'unquote':
            level -= 1
            if level == 0:
                expressions = val.rest
                validate_form(expressions, 1, 1)
                return scheme_eval(expressions.first, env)
        elif val.first == 'quasiquote':
            level += 1

        return val.map(lambda elem: quasiquote_item(elem, env, level))

    validate_form(expressions, 1, 1)
    return quasiquote_item(expressions.first, env, 1)

def do_unquote(expressions, env):
    raise SchemeError('unquote outside of quasiquote')


#################
# Dynamic Scope #
#################

def do_mu_form(expressions, env):
    """Evaluate a mu form."""
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 11
    "*** YOUR CODE HERE ***"
    body = expressions.rest
    return  MuProcedure(formals,body)

    # END PROBLEM 11



SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'let': do_let_form,
    'or': do_or_form,
    'quote': do_quote_form,
    'quasiquote': do_quasiquote_form,
    'unquote': do_unquote,
    'mu': do_mu_form,
}