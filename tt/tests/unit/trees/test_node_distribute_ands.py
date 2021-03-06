"""Test node transformation for distributing ANDs."""

from tt.definitions import (
    BINARY_OPERATORS,
    TT_AND_OP,
    TT_OR_OP)

from ._helpers import ExpressionTreeAndNodeTestCase


class TestNodeDistributeOrs(ExpressionTreeAndNodeTestCase):

    def test_single_operand(self):
        """Test that no change occurs for a single operand."""
        root = self.get_tree_root_from_expr_str('A')
        dor = root.distribute_ands()
        self.assertTrue(dor is not root)
        self.assertEqual(
            str(dor),
            'A')

    def test_only_unary_operators(self):
        """Test that no change occurs for expression of only unary NOTs."""
        root = self.get_tree_root_from_expr_str('~A')
        dor = root.distribute_ands()
        self.assertTrue(dor is not root)
        self.assertTrue(dor.l_child is not root.l_child)
        self.assertEqual(
            str(dor),
            '\n'.join((
                '~',
                '`----A')))

    def test_binary_op_no_change_expected(self):
        """Test no change occurs for non-applicable scenarios."""
        # test non-AND and non-OR binary operators
        for op in (BINARY_OPERATORS - {TT_AND_OP, TT_OR_OP}):
            op_str = op.default_plain_english_str
            root = self.get_tree_root_from_expr_str('A {} B'.format(op_str))
            dor = root.distribute_ands()
            self.assertTrue(dor is not root)
            self.assertTrue(dor.l_child is not root.l_child)
            self.assertTrue(dor.r_child is not root.r_child)
            self.assertEqual(
                str(dor),
                '\n'.join((
                    op_str,
                    '`----A',
                    '`----B')))

        # test an AND where distribution should not be applied
        root = self.get_tree_root_from_expr_str('A and (B and C and D)')
        dor = root.distribute_ands()
        self.assertTrue(dor is not root)
        self.assertTrue(dor.l_child is not root.l_child)
        self.assertTrue(dor.r_child is not root.r_child)
        self.assertTrue(dor.r_child.l_child is not root.r_child.l_child)
        self.assertTrue(dor.r_child.r_child is not root.r_child.r_child)
        self.assertTrue(dor.r_child.r_child.l_child is not
                        root.r_child.r_child.l_child)
        self.assertTrue(dor.r_child.r_child.r_child is not
                        root.r_child.r_child.r_child)
        self.assertEqual(
            str(dor),
            '\n'.join((
                'and',
                '`----A',
                '`----and',
                '     `----B',
                '     `----and',
                '          `----C',
                '          `----D')))

        # test an OR where distribution should not be applied
        root = self.get_tree_root_from_expr_str('A or (B or C or D)')
        dor = root.distribute_ands()
        self.assertTrue(dor is not root)
        self.assertTrue(dor.l_child is not root.l_child)
        self.assertTrue(dor.r_child is not root.r_child)
        self.assertTrue(dor.r_child.l_child is not root.r_child.l_child)
        self.assertTrue(dor.r_child.r_child is not root.r_child.r_child)
        self.assertTrue(dor.r_child.r_child.l_child is not
                        root.r_child.r_child.l_child)
        self.assertTrue(dor.r_child.r_child.r_child is not
                        root.r_child.r_child.r_child)
        self.assertEqual(
            str(dor),
            '\n'.join((
                'or',
                '`----A',
                '`----or',
                '     `----B',
                '     `----or',
                '          `----C',
                '          `----D')))

    def test_applicable_and_distribute_from_left(self):
        """Test a case where we expect AND to be distributed from the left."""
        root = self.get_tree_root_from_expr_str('A and (B or C or D)')
        dor = root.distribute_ands()
        self.assertTrue(dor is not root)
        self.assertTrue(dor.l_child is not root.l_child)
        self.assertTrue(dor.r_child is not root.r_child)
        self.assertTrue(dor.r_child.l_child is not root.r_child.l_child)
        self.assertTrue(dor.r_child.r_child is not root.r_child.r_child)
        self.assertTrue(dor.r_child.r_child.l_child is not
                        root.r_child.r_child.l_child)
        self.assertTrue(dor.r_child.r_child.r_child is not
                        root.r_child.r_child.r_child)
        self.assertEqual(
            str(dor),
            '\n'.join((
                'or',
                '`----and',
                '|    `----A',
                '|    `----B',
                '`----or',
                '     `----and',
                '     |    `----A',
                '     |    `----C',
                '     `----and',
                '          `----A',
                '          `----D')))

    def test_applicable_and_dsitribute_from_right(self):
        """Test a case where we expect AND to be distributed from the right."""
        root = self.get_tree_root_from_expr_str('(A or B or C) and D')
        dor = root.distribute_ands()
        self.assertTrue(dor is not root)
        self.assertTrue(dor.l_child.l_child is not root.l_child.l_child)
        self.assertTrue(dor.r_child.l_child.l_child is not
                        root.l_child.r_child)
        self.assertTrue(dor.r_child.r_child.l_child is not
                        root.l_child.r_child.r_child)
        root_D_node = root.r_child
        self.assertTrue(dor.l_child.r_child is not root_D_node)
        self.assertTrue(dor.r_child.l_child.r_child is not root_D_node)
        self.assertTrue(dor.r_child.r_child.r_child is not root_D_node)

        self.assertEqual(
            str(dor),
            '\n'.join((
                'or',
                '`----and',
                '|    `----A',
                '|    `----D',
                '`----or',
                '     `----and',
                '     |    `----B',
                '     |    `----D',
                '     `----and',
                '          `----C',
                '          `----D')))
