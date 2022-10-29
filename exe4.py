# interface for Variable
class Variable:
    def get_name(self):
        return self.variable_name


# interface for Assignment
class Assignment:
    def get_var(self) -> Variable:
        return self.v

    def get_value(self) -> float:
        return self.value

    def set_value(self, f: float):
        self.value = f


# interface for Assignments
class Assignments:
    def __getitem__(self, v: Variable) -> float:
        pass

    def __iadd__(self, ass: Assignment):
        pass


# interface for Expression
class Expression:
    def evaluate(self, assgms: Assignments) -> float:
        pass

    def derivative(self, v: Variable):
        pass

    def __repr__(self) -> str:
        pass

    def __eq__(self, other):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __pow__(self, power: float):
        pass


# return an implementation of Assignment
class ValueAssignment(Assignment):
    def __init__(self, v: Variable, value: float):
        self.v = v
        self.value = value

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __repr__(self) -> str:
        return "{}={}".format(self.v, self.value)

    def get_var(self) -> Variable:
        return self.v

    def get_value(self) -> float:
        return self.value

    def set_value(self, f: float):
        self.value = f


# return an implementation of assignments
class SimpleDictionaryAssignments(Assignments):
    def __init__(self):
        self.assgmnts = {}

    def __getitem__(self, v: Variable) -> float:
        return self.assgmnts[v.get_name()]

    def __iadd__(self, ass: Assignment):
        self.assgmnts[ass.get_var().get_name()] = ass.get_value()
        return self


# return a Constant Object
class Constant(Expression):
    def __init__(self, value: float = 0.0):
        self.value = value

    def evaluate(self, assgms: Assignments) -> float:
        return self.value

    def derivative(self, v: Variable):
        return Constant(0.0)

    def __repr__(self) -> str:
        return str(float(self.value))

    def __eq__(self, other):
        return self.value == other.value and isinstance(other, Constant)

    def __add__(self, other):
        return Constant(self.value + other.value)

    def __sub__(self, other):
        return Constant(self.value - other.value)

    def __mul__(self, other):
        return Constant(self.value * other.value)

    def __pow__(self, power: float):
        return Constant(self.value ** power)


# return a VariableExpression Object
class VariableExpression(Variable, Expression):
    def get_name(self):
        return self.variable_name

    def __init__(self, variable_name):
        self.variable_name = variable_name

    def __repr__(self):
        return self.variable_name

    def derivative(self, v: Variable):
        return Constant(1.0) if self == v else Constant(0.0)

    def __eq__(self, other):
        if not isinstance(other, VariableExpression):
            return False
        return self.variable_name == other.variable_name and isinstance(other, VariableExpression)

    def evaluate(self, assgms: Assignments) -> float:
        return assgms[self]

    def __add__(self, other):
        return Addition(self, other)

    def __sub__(self, other):
        return Subtraction(self, other)

    def __mul__(self, other):
        return Multiplication(self, other)

    def __pow__(self, power: float):
        return Power(self, power)


# return an Addition Object
class Addition(Expression):
    def __init__(self, A: Expression, B: Expression) -> Expression:
        self.A = A
        self.B = B

    def evaluate(self, assgms: Assignments) -> float:
        return self.A.evaluate(assgms) + self.B.evaluate(assgms)

    def derivative(self, v: Variable):
        return Addition(self.A.derivative(v), self.B.derivative(v))

    def __repr__(self) -> str:
        return "(" + str(self.A) + "+" + str(self.B) + ")"

    def __eq__(self, other):
        if not isinstance(other, Addition):
            return False
        return self.A == other.A and self.B == other.B and isinstance(other, Addition)

    def __add__(self, other):
        return Addition(self, other)

    def __sub__(self, other):
        return Subtraction(self, other)

    def __mul__(self, other):
        return Multiplication(self, other)

    def __pow__(self, power: float, modulo=None):
        return Power(self, power)


# return a Substraction Object
class Subtraction(Expression):
    def __init__(self, A: Expression, B: Expression) -> Expression:
        self.A = A
        self.B = B

    def evaluate(self, assgms: Assignments) -> float:
        return self.A.evaluate(assgms) - self.B.evaluate(assgms)

    def derivative(self, v: Variable):
        return Subtraction(self.A.derivative(v), self.B.derivative(v))

    def __repr__(self) -> str:
        return "(" + str(self.A) + "-" + str(self.B) + ")"

    def __eq__(self, other):
        if not isinstance(other, Subtraction):
            return False
        return self.A == other.A and self.B == other.B

    def __add__(self, other):
        return Addition(self, other)

    def __sub__(self, other):
        return Subtraction(self, other)

    def __mul__(self, other):
        return Multiplication(self, other)

    def __pow__(self, power: float):
        return Power(self, power)


# return a Multiplication Object
class Multiplication(Expression):
    def __init__(self, A: Expression, B: Expression) -> Expression:
        self.A = A
        self.B = B

    def evaluate(self, assgms: Assignments) -> float:
        return self.A.evaluate(assgms) * self.B.evaluate(assgms)

    def derivative(self, v: Variable):
        return Addition(Multiplication(self.A.derivative(v), self.B), Multiplication(self.A, self.B.derivative(v)))

    def __repr__(self) -> str:
        return "(" + str(self.A) + "*" + str(self.B) + ")"

    def __eq__(self, other):
        if not isinstance(other, Multiplication):
            return False
        return self.A == other.A and self.B == other.B

    def __add__(self, other):
        return Addition(self, other)

    def __sub__(self, other):
        return Subtraction(self, other)

    def __mul__(self, other):
        return Multiplication(self, other)

    def __pow__(self, power: float):
        return Power(self, power)


# return a Power Object
class Power(Expression):
    def __init__(self, exp: Expression, p: float) -> Expression:
        self.exp = exp
        self.p = Constant(p)

    def evaluate(self, assgms: Assignments) -> float:
        return self.exp.evaluate(assgms) ** self.p.value

    def derivative(self, v: Variable):
        return Multiplication(
            Multiplication(self.p, Power(self.exp, self.p.value - 1)), self.exp.derivative(v))

    def __repr__(self) -> str:
        return "(" + str(self.exp) + "^" + str(self.p) + ")"

    def __eq__(self, other):
        if not isinstance(other, Power):
            return False
        return self.exp == other.exp and self.p == other.p

    def __add__(self, other):
        return Addition(self, other)

    def __sub__(self, other):
        return Subtraction(self, other)

    def __mul__(self, other):
        return Multiplication(self, other)

    def __pow__(self, power: float):
        return Power(self, power)


# return a Polynomial Object
class Polynomial(Expression):
    def __init__(self, v: Variable, coefs: list) -> Expression:
        self.v = v
        self.coefs = coefs
        self.degree = len(self.coefs) - 1

    def NR_evaluate(self, assgms: Assignments, epsilon: int = 0.0001, times: int = 100):
        newvar = VariableExpression('newvar')
        # initial guess
        assgms += ValueAssignment(newvar, 1)
        f = Polynomial(newvar, self.coefs)
        ftag = Polynomial(newvar, self.coefs).derivative(newvar)
        for _ in range(times):
            fx = f.evaluate(assgms)
            ftagx = ftag.evaluate(assgms)
            assgms += ValueAssignment(newvar, newvar.evaluate(assgms) - fx/ftagx)
        if abs(f.evaluate(assgms)) <= epsilon:
            return assgms[newvar]
        else:
            raise Exception("Root not found")

    def evaluate(self, assgms: Assignments) -> float:
        return sum([co * assgms[self.v] ** (indx - 1) for indx, co in enumerate(self.coefs)])

    def derivative(self, v: Variable):
        newcoefs = []
        for indx, co in enumerate(self.coefs[1:]):
            newco = co * (indx + 1)
            newcoefs.append(newco)
        return Polynomial(self.v, newcoefs)

    def __repr__(self) -> str:
        toreturn = ""
        for idx, co in enumerate(self.coefs):
            power = idx
            costring = "+" + str(co) if idx != self.degree and co > 0 else str(co)
            costring = costring if co != 0 else ""
            powerstring = "^" + str(power) if power > 1 and co != 0 else ""
            varstring = self.v.get_name() if power > 0 and co != 0 else ""
            toreturn = costring + varstring + powerstring + toreturn
        return "(" + toreturn + ")"

    def __eq__(self, other):
        if not isinstance(other, Polynomial):
            return False
        return self.coefs == other.coefs

    def __add__(self, other):
        return Addition(self, other)

    def __sub__(self, other):
        return Subtraction(self, other)

    def __mul__(self, other):
        return Multiplication(self, other)

    def __pow__(self, power: float):
        return Power(self, power)
