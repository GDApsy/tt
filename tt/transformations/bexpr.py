"""Transformation functions for expressions."""

from tt.errors import InvalidArgumentTypeError
from tt.expressions import BooleanExpression


def _ensure_bexpr(expr):
    """Return a BooleanExpression object or raise an error."""
    if isinstance(expr, str):
        return BooleanExpression(expr)
    elif isinstance(expr, BooleanExpression):
        return expr
    else:
        raise InvalidArgumentTypeError(
            'Transformations accept either a string or BooleanExpression '
            'argument')


def apply_de_morgans(expr):
    """Convert an expression to a form with De Morgan's Law applied.

    :returns: A new expression object, transformed so that De Morgan's Law has
        been applied to negated *ANDs* and *ORs*.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid type.

    Here's a couple of simple examples showing De Morgan's Law being applied
    to a negated AND and a negated OR::

        >>> from tt import apply_de_morgans
        >>> apply_de_morgans('not (A or B)')
        <BooleanExpression "not A and not B">
        >>> apply_de_morgans('not (A and B)')
        <BooleanExpression "not A or not B">

    """
    bexpr = _ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.root.apply_de_morgans())


def coalesce_negations(expr):
    """Convert an expression to a form with all negations condensed.

    :returns: A new expression object, transformed so that all "runs" of
        logical *NOTs* are condensed into the minimal equivalent number.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid type.

    Here's a simple example showing the basic premise of this transformation::

        >>> from tt import coalesce_negations
        >>> coalesce_negations('~~A or ~B or ~~~C or ~~~~D')
        <BooleanExpression "A or ~B or ~C or D">

    This transformation works on expressions, too::

        >>> coalesce_negations('!!(A -> not not B) or ~(~(A xor B))')
        <BooleanExpression "(A -> B) or (A xor B)">

    """
    bexpr = _ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.root.coalesce_negations())


def distribute_ands(expr):
    """Convert an expression to distribute ANDs over ORed clauses.

    :param expr: The expression to transform.
    :type expr: :class:`str <python:str>` or :class:`BooleanExpression \
    <tt.expressions.bexpr.BooleanExpression>`

    :returns: A new expression object, transformed to distribute ANDs over ORed
        clauses.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid type.

    Here's a simple example::

        >>> from tt import distribute_ands
        >>> distribute_ands('A and (B or C or D)')
        <BooleanExpression "(A and B) or (A and C) or (A and D)">

    And an example involving distributing a sub-expression::

        >>> distribute_ands('(A and B) and (C or D or E)')
        <BooleanExpression "(A and B and C) or (A and B and D) or \
(A and B and E)">

    """
    bexpr = _ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.root.distribute_ands())


def distribute_ors(expr):
    """Convert an expression to distribute ORs over ANDed clauses.

    :param expr: The expression to transform.
    :type expr: :class:`str <python:str>` or :class:`BooleanExpression \
    <tt.expressions.bexpr.BooleanExpression>`

    :returns: A new expression object, transformed to distribute ORs over ANDed
        clauses.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid type.

    Here's a simple example::

        >>> from tt import distribute_ors
        >>> distribute_ors('A or (B and C and D and E)')
        <BooleanExpression "(A or B) and (A or C) and (A or D) and (A or E)">

    And an example involving distributing a sub-expression::

        >>> distribute_ors('(A or B) or (C and D)')
        <BooleanExpression "(A or B or C) and (A or B or D)">

    """
    bexpr = _ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.root.distribute_ors())


def to_primitives(expr):
    """Convert an expression to a form with only primitive operators.

    All operators will be transformed equivalent form composed only of the
    logical AND, OR,and NOT operators. Symbolic operators in the passed
    expression will remain symbolic in the transformed expression and the same
    applies for plain English operators.

    :param expr: The expression to transform.
    :type expr: :class:`str <python:str>` or :class:`BooleanExpression \
    <tt.expressions.bexpr.BooleanExpression>`

    :returns: A new expression object, transformed to contain only primitive
        operators.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid type.

    Here's a simple transformation of exclusive-or::

        >>> from tt import to_primitives
        >>> to_primitives('A xor B')
        <BooleanExpression "(A and not B) or (not A and B)">

    And another example of if-and-only-if (using symbolic operators)::

        >>> to_primitives('A <-> B')
        <BooleanExpression "(A /\ B) \/ (~A /\ ~B)">

    """
    bexpr = _ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.root.to_primitives())
