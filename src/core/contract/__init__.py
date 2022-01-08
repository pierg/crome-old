from __future__ import annotations

from copy import deepcopy

from core.contract.exceptions import (
    IncompatibleContracts,
    InconsistentContracts,
    Set,
    UnfeasibleContracts,
)
from core.controller.synthesisinfo import SynthesisInfo
from core.specification import Specification
from core.specification.exceptions import NotSatisfiableException
from core.specification.lformula import LTL
from core.typeset import Typeset


class Contract:
    def __init__(
        self,
        assumptions: Specification = None,
        guarantees: Specification = None,
        saturate: bool = True,
    ):

        self.__assumptions = None
        self.__guarantees = None

        self.__setassumptions(assumptions)
        self.__setguarantees(guarantees, saturate)
        self.__checkfeasibility()

        self.composed_by = {self}
        self.merged_by = {self}
        self.conjoined_by = {self}
        self.disjoined_by = {self}

    @property
    def assumptions(self) -> Specification:
        return self.__assumptions

    @assumptions.setter
    def assumptions(self, value: Specification):
        self.__setassumptions(value)
        self.__checkfeasibility()

    @property
    def guarantees(self) -> Specification:
        """Returning saturated guarantee."""
        return self.__guarantees

    @guarantees.setter
    def guarantees(self, value: Specification):
        self.__setguarantees(value)
        self.__checkfeasibility()

    @property
    def typeset(self) -> Typeset:
        return self.__guarantees.typeset | self.__assumptions.typeset

    def __setassumptions(self, value: Specification):
        """Setting Assumptions."""
        if value is None:
            self.__assumptions = LTL("TRUE")
        else:
            if not isinstance(value, Specification):
                raise AttributeError
            """Every contracts assigns a **copy** of A and G"""
            self.__assumptions = deepcopy(value)

    def __setguarantees(self, value: Specification, saturate=True):
        if value is None:
            self.__guarantees = LTL()
        else:
            if not isinstance(value, Specification):
                raise AttributeError
            """Every contracts assigns a **copy** of A and G"""
            self.__guarantees = deepcopy(value)
        """Saturate the guarantees"""
        if saturate:
            self.__guarantees.saturate(self.__assumptions)

    def __checkfeasibility(self):
        """Check Feasibility."""
        if self.assumptions is not None or not self.assumptions.is_true():
            try:
                self.__assumptions & self.__guarantees
            except NotSatisfiableException as e:
                raise UnfeasibleContracts(self, e)

    def __str__(self):
        ret = "\n--ASSUMPTIONS--\n"
        ret += str(self.assumptions)
        ret += "\n--GUARANTEES--\n"
        ret += str(self.guarantees)
        return ret

    """Refinement"""

    def __le__(self: Contract, other: Contract):
        """self <= other.

        True if self is a refinement of other
        """
        cond_a = self.assumptions >= other.assumptions
        cond_g = self.guarantees <= other.guarantees
        return cond_a and cond_g

    def __eq__(self: Contract, other: Contract):
        """self == other.

        True if self is a refinement of other and viceversa
        """
        cond_a = self <= other
        cond_g = other <= self
        return cond_a and cond_g

    def __hash__(self):
        return hash(f"{str(self.assumptions)} -> {str(self.guarantees)}")

    def get_controller_info(self, world_ts: Typeset = None) -> SynthesisInfo:
        """Extract All Info Needed to Build a Controller from the Contract."""

        """Assumptions"""
        assumptions = []
        a_mutex = []
        a_liveness = []

        """Guarantees"""
        guarantees = []
        g_mutex = []
        g_adjacency = []

        a_typeset = Typeset()
        g_typeset = Typeset()

        list, typeset = self.assumptions.formula(SpecificationOutput.ListCNF)
        assumptions.extend(list)
        a_typeset |= typeset

        list, typeset = self.guarantees.formula(SpecificationOutput.ListCNF)
        guarantees.extend(list)
        g_typeset |= typeset

        if world_ts is not None:
            instance_ts = Typeset.get_instance_ts((a_typeset | g_typeset), world_ts)
        else:
            instance_ts = a_typeset | g_typeset

        """Extracting Inputs and Outputs Including the variables"""
        i_set, o_set = instance_ts.extract_inputs_outputs()

        i_typeset = Typeset(i_set)
        o_typeset = Typeset(o_set)

        """Mutex Rules"""
        ret = Atom.extract_mutex_rules(i_typeset, output=SpecificationOutput.ListCNF)
        if ret is not None:
            rules, typeset = ret
            a_mutex.extend(rules)

        ret = Atom.extract_mutex_rules(o_typeset, output=SpecificationOutput.ListCNF)
        if ret is not None:
            rules, typeset = ret
            g_mutex.extend(rules)

        """Adjacecy Rules"""
        ret = Atom.extract_adjacency_rules(
            o_typeset, output=SpecificationOutput.ListCNF
        )
        if ret is not None:
            rules, typeset = ret
            g_adjacency.extend(rules)

        """Adding Liveness To Sensors (input)"""
        ret = Atom.extract_liveness_rules(i_typeset, output=SpecificationOutput.ListCNF)
        if ret is not None:
            rules, typeset = ret
            a_liveness.extend(rules)

        """Adding context and active signal rules"""
        ret = Atom.context_active_rules(i_typeset, output=SpecificationOutput.ListCNF)
        if ret is not None:
            rules, typeset = ret
            assumptions.extend(rules)

        """Extract Inputs and Outputs"""
        inputs = [t.name for t in i_set]
        outputs = [t.name for t in o_set]

        return SynthesisInfo(
            assumptions=assumptions,
            a_liveness=a_liveness,
            a_mutex=a_mutex,
            guarantees=guarantees,
            g_mutex=g_mutex,
            g_adjacency=g_adjacency,
            inputs=inputs,
            outputs=outputs,
        )

    @staticmethod
    def composition(contracts: Set[Contract]) -> Contract:
        if len(contracts) == 1:
            return next(iter(contracts))
        if len(contracts) == 0:
            raise Exception("No contract specified in the composition")

        contract_list = list(contracts)
        new_assumptions = deepcopy(contract_list[0].assumptions)
        new_guarantees = deepcopy(contract_list[0].guarantees)

        """Populate the data structure while checking for compatibility and consistency"""
        for contract in contract_list[1:]:

            try:
                new_assumptions &= contract.assumptions
            except NotSatisfiableException as e:
                raise IncompatibleContracts(contract, e)

            try:
                new_guarantees &= contract.guarantees
            except NotSatisfiableException as e:
                raise InconsistentContracts(contract, e)

        """Assumptions relaxation"""
        new_assumptions |= ~new_guarantees

        """New contracts without saturation cause it was already saturated"""
        new_contract = Contract(
            assumptions=new_assumptions, guarantees=new_guarantees, saturate=False
        )

        new_contract.composed_by = contracts

        return new_contract

    @staticmethod
    def conjunction(contracts: Set[Contract]) -> Contract:
        if len(contracts) == 1:
            return next(iter(contracts))
        if len(contracts) == 0:
            raise Exception("No contract specified in the conjunction")

        contract_list = list(contracts)
        new_assumptions = deepcopy(contract_list[0].assumptions)
        new_guarantees = deepcopy(contract_list[0].guarantees)

        """Populate the data structure while checking for compatibility and consistency"""
        for contract in contract_list[1:]:

            new_assumptions |= contract.assumptions

            try:
                new_guarantees &= contract.guarantees
            except NotSatisfiableException as e:
                raise InconsistentContracts(contract, e)

        print("The conjunction is compatible and consistent")

        """New contracts without saturation cause it was already saturated"""
        new_contract = Contract(
            assumptions=new_assumptions, guarantees=new_guarantees, saturate=False
        )

        new_contract.conjoined_by = contracts

        return new_contract

    @staticmethod
    def disjunction(contracts: Set[Contract]) -> Contract:
        if len(contracts) == 1:
            return next(iter(contracts))
        if len(contracts) == 0:
            raise Exception("No contract specified in the disjunction")

        contract_list = list(contracts)
        new_assumptions = deepcopy(contract_list[0].assumptions)
        new_guarantees = deepcopy(contract_list[0].guarantees)

        """Populate the data structure while checking for compatibility and consistency"""
        for contract in contract_list[1:]:

            new_assumptions &= contract.assumptions

            try:
                new_guarantees |= contract.guarantees
            except NotSatisfiableException as e:
                raise InconsistentContracts(contract, e)

        """New contracts without saturation cause it was already saturated"""
        new_contract = Contract(
            assumptions=new_assumptions, guarantees=new_guarantees, saturate=False
        )

        new_contract.disjoined_by = contracts

        return new_contract

    @staticmethod
    def quotient(dividend: Contract, divisor: Contract) -> Contract:
        if dividend is None:
            raise Exception("No dividend specified in the quotient")
        if divisor is None:
            raise Exception("No divisor specified in the quotient")

        c = dividend
        a = c.assumptions
        g = c.guarantees

        c1 = divisor
        a1 = c1.assumptions
        g1 = c1.guarantees

        try:
            a2 = a & g1
        except NotSatisfiableException as e:
            raise IncompatibleContracts(c, e)

        try:
            g2 = g & a1 | ~(a & g1)
        except NotSatisfiableException as e:
            raise InconsistentContracts(c, e)

        quotient = Contract(assumptions=a2, guarantees=g2)

        return quotient

    @staticmethod
    def merging(contracts: Set[Contract]) -> Contract:
        if len(contracts) == 1:
            return next(iter(contracts))
        if len(contracts) == 0:
            raise Exception("No contract specified in the merging")

        contract_list = list(contracts)
        new_assumptions = deepcopy(contract_list[0].assumptions)
        new_guarantees = deepcopy(contract_list[0].guarantees)

        """Populate the data structure while checking for compatibility and consistency"""
        for contract in contract_list[1:]:

            try:
                new_assumptions &= contract.assumptions
            except NotSatisfiableException as e:
                raise IncompatibleContracts(contract, e)

            try:
                new_guarantees &= contract.guarantees
            except NotSatisfiableException as e:
                raise InconsistentContracts(contract, e)

        """Guarantees relaxation"""
        new_guarantees = new_guarantees | ~new_assumptions

        """New contracts without saturation cause it was already saturated"""
        new_contract = Contract(
            assumptions=new_assumptions, guarantees=new_guarantees, saturate=False
        )

        new_contract.merged_by = contracts

        return new_contract

    @staticmethod
    def separation(dividend: Contract, divisor: Contract) -> Contract:
        if dividend is None:
            raise Exception("No dividend specified in the separation")
        if divisor is None:
            raise Exception("No divisor specified in the separation")

        c = dividend
        a = c.assumptions
        g = c.guarantees

        c1 = divisor
        a1 = c1.assumptions
        g1 = c1.guarantees

        print(c.guarantees)
        print(c1.guarantees)

        try:
            a2 = a & g1 | ~(g & a1)
        except NotSatisfiableException as e:
            raise IncompatibleContracts(c, e)

        try:
            g2 = g & a1
        except NotSatisfiableException as e:
            raise InconsistentContracts(c, e)

        separation = Contract(assumptions=a2, guarantees=g2)

        print(g2)

        return separation
