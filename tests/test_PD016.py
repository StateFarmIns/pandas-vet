# stdlib
import ast

from pandas_vet import VetPlugin
from pandas_vet import PD016
from textwrap import dedent


def test_PD016_pass_for_loops():
    """
    Test that normal operations in for loops do not result in an error.
    """
    # Check that normal assignments do not raise.
    statement = dedent(
        """
    for i in [0, 1, 2]:
        j = j + 1
        s = str(s)
    """
    )
    tree = ast.parse(statement)
    actual = list(VetPlugin(tree).run())
    expected = []
    assert actual == expected

    # Check that list appending does not raise
    # Check that normal indexing does not raise
    statement = dedent(
        """
    l = []
    for i in [0, 1, 2]:
        l.append(i)
        l[0] = 10
    """
    )
    tree = ast.parse(statement)
    actual = list(VetPlugin(tree).run())
    expected = []
    assert actual == expected


def test_PD016_pass_while_loops():
    """
    Test that normal operations in wile loops do not result in an error.
    """
    # Check that normal assignments do not raise.
    statement = dedent(
        """
    j = 1
    f = 1
    while True:
        j = j + 1
        s = str(f)
    """
    )
    tree = ast.parse(statement)
    actual = list(VetPlugin(tree).run())
    expected = []
    assert actual == expected

    # Check that list appending does not raise
    # Check that normal indexing does not raise
    statement = dedent(
        """
    l = []
    while True:
        l.append(i)
        l[0] = 10
    """
    )
    tree = ast.parse(statement)
    actual = list(VetPlugin(tree).run())
    expected = []
    assert actual == expected


def test_PD016_fail_for_loops():
    """
    Test that assignment to .loc and .loc fail in for loops.
    """
    # Check .loc[].
    statement = dedent(
        """
        for i in [0, 1, 2]:
            df.loc[i] = j + 1
        """
    )
    tree = ast.parse(statement)
    actual = list(VetPlugin(tree).run())
    expected = [PD016(3, 4)]
    assert actual == expected

    # Check .iloc[].
    statement = dedent(
        """
        for i in [0, 1, 2]:
            df.iloc[i] = j + 1
        """
    )
    tree = ast.parse(statement)
    actual = list(VetPlugin(tree).run())
    expected = [PD016(3, 4)]
    assert actual == expected


def test_PD016_fail_while_loops():
    """
    Test that assignment to .loc and .loc fail in while loops.
    """
    # Check .loc[].
    statement = dedent(
        """
       while True:
            df.loc[i] = j + 1
        """
    )
    tree = ast.parse(statement)
    actual = list(VetPlugin(tree).run())
    expected = [PD016(3, 5)]
    assert actual == expected

    # Check .iloc[].
    statement = dedent(
        """
        while True:
            df.iloc[i] = j + 1
        """
    )
    tree = ast.parse(statement)
    actual = list(VetPlugin(tree).run())
    expected = [PD016(3, 4)]
    assert actual == expected
