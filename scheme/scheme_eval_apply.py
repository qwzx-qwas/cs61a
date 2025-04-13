import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############

def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):#如果表达式是符号
        return env.lookup(expr)#从环境env中查找符号对应的值
    elif self_evaluating(expr):#如果表达式是自求值（数字）
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):#验证表达式是否为合法的Scheme列表结构
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:#检查是否为特殊形式
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"
        #Evaluate the operator
        
        #调用scheme_apply来处理procedure和参数值（将procedure应用于参数值），返回结果
        #递归调用operator，来求值检查
        operator = scheme_eval(expr.first,env)#他会返回一个先前的代码的判断（是符号，还是数字，又或是特殊形式）
        #看operator是不是一个正确的procedure
        if not isinstance(operator,Procedure):
            raise SchemeError(f"Operator is not a procedure:{operator}")
        #对所有操作对象进行求值，将结果（参数值）收集到scheme列表中
        operands = expr.rest

        evaluated_operands = operands.map(lambda x: scheme_eval(x,env))

        return scheme_apply(operator,evaluated_operands,env)        
        

        # END PROBLEM 3

def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        py_args = []
        while args is not nil:
            py_args.append(args.first)
            args = args.rest
        if procedure.need_env is True:
            py_args.append(env)
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            "*** YOUR CODE HERE ***"
            result = procedure.py_func(*py_args)
            return result
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        "*** YOUR CODE HERE ***"
        #procedure 变量代表一个 ​​LambdaProcedure 类的实例对象​​
        #procedure.env来创建子框架，并且绑定实参和形参

        new_frame = procedure.env.make_child_frame(procedure.formals,args)

        #body is a Scheme list of expressions; the body of the procedure.
        #env应该使用当前框架

        result = eval_all(procedure.body,new_frame)
        return result
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        #当前调用帧的父环境指向env（仅有这点与定义lambda时不同（lambda是静态的scope),其他按照上面的写）
        new_frame = Frame(env).make_child_frame(procedure.formals,args)
        
        return eval_all(procedure.body,new_frame)
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    if expressions is nil:
        return None
    current = scheme_eval(expressions.first,env)#envaluate expressions.first （对每个元素进行求值）
    if expressions.rest is not nil:#表明未到最后一个元素
        return eval_all(expressions.rest,env)#递归调用函数，走向下一个元素
    else:
        return current#返回最后一个元素

    # replace this with lines of your own code
    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 1
        "*** YOUR CODE HERE ***"
        # END OPTIONAL PROBLEM 1
    return optimized_eval














################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
