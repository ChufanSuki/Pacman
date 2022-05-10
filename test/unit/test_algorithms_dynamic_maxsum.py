
import types
import unittest
from unittest.mock import MagicMock

from pacman.algorithms.maxsum_dynamic import DynamicFunctionFactorComputation
from pacman.dcop.objects import Variable
from pacman.dcop.relations import AsNAryFunctionRelation
from pacman.infrastructure.communication import InProcessCommunicationLayer, Messaging

#
class DynamicFunctionFactorComputationTest(unittest.TestCase):
    def test_init(self):

        domain = list(range(10))
        x1 = Variable("x1", domain)
        x2 = Variable("x2", domain)

        @AsNAryFunctionRelation(x1, x2)
        def phi(x1_, x2_):
            return x1_ + x2_

        comp_def = MagicMock()
        comp_def.algo.algo = "amaxsum"
        comp_def.algo.mode = "min"
        comp_def.node.factor = phi
        f = DynamicFunctionFactorComputation(comp_def=comp_def)

        self.assertEqual(f.name, "phi")

    def test_change_function_name(self):
        domain = list(range(10))
        x1 = Variable("x1", domain)
        x2 = Variable("x2", domain)

        @AsNAryFunctionRelation(x1, x2)
        def phi(x1_, x2_):
            return x1_ + x2_

        @AsNAryFunctionRelation(x1, x2)
        def phi2(x1_, x2_):
            return x1_ - x2_

        comp_def = MagicMock()
        comp_def.algo.algo = "amaxsum"
        comp_def.algo.mode = "min"
        comp_def.node.factor = phi
        f = DynamicFunctionFactorComputation(comp_def=comp_def)
        f.message_sender = MagicMock()
        f.change_factor_function(phi2)

        self.assertEqual(f.name, "phi")

    def test_change_function_different_order(self):
        domain = list(range(10))
        x1 = Variable("x1", domain)
        x2 = Variable("x2", domain)

        @AsNAryFunctionRelation(x1, x2)
        def phi(x1_, x2_):
            return x1_ + x2_

        @AsNAryFunctionRelation(x2, x1)
        def phi2(x2_, x1_):
            return x1_ - x2_

        comp_def = MagicMock()
        comp_def.algo.algo = "amaxsum"
        comp_def.algo.mode = "min"
        comp_def.node.factor = phi
        f = DynamicFunctionFactorComputation(comp_def=comp_def)
        f.message_sender = MagicMock()
        f.change_factor_function(phi2)

        self.assertEqual(f.name, "phi")

    def test_change_function_wrong_dimensions_len(self):

        domain = list(range(10))
        x1 = Variable("x1", domain)
        x2 = Variable("x2", domain)
        x3 = Variable("x3", domain)

        @AsNAryFunctionRelation(x1, x2)
        def phi(x1_, x2_):
            return x1_ + x2_

        @AsNAryFunctionRelation(x1, x2, x3)
        def phi2(x1_, x2_, x3_):
            return x1_ - x2_ + x3_

        comp_def = MagicMock()
        comp_def.algo.algo = "amaxsum"
        comp_def.algo.mode = "min"
        comp_def.node.factor = phi

        f = DynamicFunctionFactorComputation(comp_def=comp_def)
        # Monkey patch post_msg method with dummy mock to avoid error:
        f.post_msg = types.MethodType(lambda w, x, y, z: None, f)

        self.assertRaises(ValueError, f.change_factor_function, phi2)

    def test_change_function_wrong_dimensions_var(self):
        domain = list(range(10))
        x1 = Variable("x1", domain)
        x2 = Variable("x2", domain)
        x3 = Variable("x3", domain)

        @AsNAryFunctionRelation(x1, x2)
        def phi(x1_, x2_):
            return x1_ + x2_

        @AsNAryFunctionRelation(x1, x3)
        def phi2(x1_, x3_):
            return x1_ + x3_

        comp_def = MagicMock()
        comp_def.algo.algo = "amaxsum"
        comp_def.algo.mode = "min"
        comp_def.node.factor = phi

        f = DynamicFunctionFactorComputation(comp_def=comp_def)

        # Monkey patch post_msg method with dummy mock to avoid error:
        f.post_msg = types.MethodType(lambda w, x, y, z: None, f)

        self.assertRaises(ValueError, f.change_factor_function, phi2)
