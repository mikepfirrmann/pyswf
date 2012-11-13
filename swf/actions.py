from __future__ import print_function
from decimal import *
import sys

action_stack = []
action_variable_context = {"_global": {}}
action_constant_pool = []

class Action(object):
    def __init__(self, code, length):
        self._code = code
        self._length = length

    @property
    def code(self):
        return self._code

    @property
    def length(self):
        return self._length;

    @property
    def version(self):
        return 3

    def parse(self, data):
        # Do nothing. Many Actions don't have a payload.
        # For the ones that have one we override this method.
        if self._length > 0:
            print("skipping {} bytes...".format(self._legth), file=sys.stderr)
            data.skip_bytes(self._length)

    def __repr__(self):
        return "[Action] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionUnknown(Action):
    ''' Dummy class to read unknown actions '''
    def __init__(self, code, length):
        super(ActionUnknown, self).__init__(code, length)
        print(self, file=sys.stderr)

    def parse(self, data):
        if self._length > 0:
            print("skipping {} bytes...".format(self._length), file=sys.stderr)
            data.skip_bytes(self._length)

    def __repr__(self):
        action_map={}
        action_map[int('04', 16)]='ActionNextFrame'
        action_map[int('05', 16)]='ActionPreviousFrame'
        action_map[int('06', 16)]='ActionPlay'
        action_map[int('07', 16)]='ActionStop'
        action_map[int('08', 16)]='ActionToggleQuality'
        action_map[int('09', 16)]='ActionStopSounds'
        action_map[int('0a', 16)]='ActionAdd'
        action_map[int('0b', 16)]='ActionSubtract'
        action_map[int('0c', 16)]='ActionMultiply'
        action_map[int('0d', 16)]='ActionDivide'
        action_map[int('0e', 16)]='ActionEquals'
        action_map[int('0f', 16)]='ActionLess'
        action_map[int('10', 16)]='ActionAnd'
        action_map[int('11', 16)]='ActionOr'
        action_map[int('12', 16)]='ActionNot'
        action_map[int('13', 16)]='ActionStringEquals'
        action_map[int('14', 16)]='ActionStringLength'
        action_map[int('15', 16)]='ActionStringExtract'
        action_map[int('17', 16)]='ActionPop'
        action_map[int('18', 16)]='ActionToInteger'
        action_map[int('1c', 16)]='ActionGetVariable'
        action_map[int('1d', 16)]='ActionSetVariable'
        action_map[int('20', 16)]='ActionSetTarget2'
        action_map[int('21', 16)]='ActionStringAdd'
        action_map[int('22', 16)]='ActionGetProperty'
        action_map[int('23', 16)]='ActionSetProperty'
        action_map[int('24', 16)]='ActionCloneSprite'
        action_map[int('25', 16)]='ActionRemoveSprite'
        action_map[int('26', 16)]='ActionTrace'
        action_map[int('27', 16)]='ActionStartDrag'
        action_map[int('28', 16)]='ActionEndDrag'
        action_map[int('29', 16)]='ActionStringLess'
        action_map[int('2a', 16)]='ActionThrow'
        action_map[int('2b', 16)]='ActionCastOp'
        action_map[int('2c', 16)]='ActionImplementsOp'
        action_map[int('30', 16)]='ActionRandomNumber'
        action_map[int('31', 16)]='ActionMBStringLength'
        action_map[int('32', 16)]='ActionCharToAscii'
        action_map[int('33', 16)]='ActionAsciiToChar'
        action_map[int('34', 16)]='ActionGetTime'
        action_map[int('35', 16)]='ActionMBStringExtract'
        action_map[int('36', 16)]='ActionMBCharToAscii'
        action_map[int('37', 16)]='ActionMBAsciiToChar'
        action_map[int('3a', 16)]='ActionDelete'
        action_map[int('3b', 16)]='ActionDelete2'
        action_map[int('3c', 16)]='ActionDefineLocal'
        action_map[int('3d', 16)]='ActionCallFunction'
        action_map[int('3e', 16)]='ActionReturn'
        action_map[int('3f', 16)]='ActionModulo'
        action_map[int('40', 16)]='ActionNewObject'
        action_map[int('41', 16)]='ActionDefineLocal2'
        action_map[int('42', 16)]='ActionInitArray'
        action_map[int('43', 16)]='ActionInitObject'
        action_map[int('44', 16)]='ActionTypeOf'
        action_map[int('45', 16)]='ActionTargetPath'
        action_map[int('46', 16)]='ActionEnumerate'
        action_map[int('47', 16)]='ActionAdd2'
        action_map[int('48', 16)]='ActionLess2'
        action_map[int('49', 16)]='ActionEquals2'
        action_map[int('4a', 16)]='ActionToNumber'
        action_map[int('4b', 16)]='ActionToString'
        action_map[int('4c', 16)]='ActionPushDuplicate'
        action_map[int('4d', 16)]='ActionStackSwap'
        action_map[int('4e', 16)]='ActionGetMember'
        action_map[int('4f', 16)]='ActionSetMember'
        action_map[int('50', 16)]='ActionIncrement'
        action_map[int('51', 16)]='ActionDecrement'
        action_map[int('52', 16)]='ActionCallMethod'
        action_map[int('53', 16)]='ActionNewMethod'
        action_map[int('54', 16)]='ActionInstanceOf'
        action_map[int('55', 16)]='ActionEnumerate2'
        action_map[int('60', 16)]='ActionBitAnd'
        action_map[int('61', 16)]='ActionBitOr'
        action_map[int('62', 16)]='ActionBitXor'
        action_map[int('63', 16)]='ActionBitLShift'
        action_map[int('64', 16)]='ActionBitRShift'
        action_map[int('65', 16)]='ActionBitURShift'
        action_map[int('66', 16)]='ActionStrictEquals'
        action_map[int('67', 16)]='ActionGreater'
        action_map[int('68', 16)]='ActionStringGreater'
        action_map[int('69', 16)]='ActionExtends'
        action_map[int('81', 16)]='ActionGotoFrame'
        action_map[int('83', 16)]='ActionGetURL'
        action_map[int('87', 16)]='ActionStoreRegister'
        action_map[int('88', 16)]='ActionConstantPool'
        action_map[int('8a', 16)]='ActionWaitForFrame'
        action_map[int('8b', 16)]='ActionSetTarget'
        action_map[int('8c', 16)]='ActionGotoLabel'
        action_map[int('8d', 16)]='ActionWaitForFrame2'
        action_map[int('8e', 16)]='ActionDefineFunction2'
        action_map[int('8f', 16)]='ActionTry'
        action_map[int('94', 16)]='ActionWith'
        action_map[int('96', 16)]='ActionPush'
        action_map[int('99', 16)]='ActionJump'
        action_map[int('9a', 16)]='ActionGetURL2'
        action_map[int('9b', 16)]='ActionDefineFunction'
        action_map[int('9d', 16)]='ActionIf'
        action_map[int('9e', 16)]='ActionCall'
        action_map[int('9f', 16)]='ActionGotoFrame2'

        name = "ActionUnknown"
        if self._code in action_map and not (action_map[self._code] is None):
            name = action_map[self._code]
        return "Unknown: [%s], Code: 0x%x, Length: %d" % (name, self._code, self._length)

class Action4(Action):
    ''' Base class for SWF 4 actions '''
    def __init__(self, code, length):
        super(Action4, self).__init__(code, length)

    @property
    def version(self):
        return 4

class Action5(Action):
    ''' Base class for SWF 5 actions '''
    def __init__(self, code, length):
        super(Action5, self).__init__(code, length)

    @property
    def version(self):
        return 5

class Action6(Action):
    ''' Base class for SWF 6 actions '''
    def __init__(self, code, length):
        super(Action6, self).__init__(code, length)

    @property
    def version(self):
        return 6

class Action7(Action):
    ''' Base class for SWF 7 actions '''
    def __init__(self, code, length):
        super(Action7, self).__init__(code, length)

    @property
    def version(self):
        return 7

# =========================================================
# SWF 3 actions
# =========================================================
class ActionGetURL(Action):
    CODE = 0x83
    def __init__(self, code, length):
        self.urlString = None
        self.targetString = None
        super(ActionGetURL, self).__init__(code, length)

    def parse(self, data):
        self.urlString = data.readString()
        self.targetString = data.readString()

    def __repr__(self):
        return "[ActionGetURL] Code: 0x%x, Length: %d, URL: '%s', Target: '%s'" % (self._code, self._length, self.urlString, self.targetString)

class ActionGotoFrame(Action):
    CODE = 0x81
    def __init__(self, code, length):
        self.frame = 0
        super(ActionGotoFrame, self).__init__(code, length)

    def parse(self, data):
        self.frame = data.readUI16()

    def __repr__(self):
        return "[ActionGotoFrame] Code: 0x%x, Length: %d, Frame: '%s'" % (self._code, self._length, self.frame)

class ActionGotoLabel(Action):
    CODE = 0x8c
    def __init__(self, code, length):
        self.label = None
        super(ActionGotoLabel, self).__init__(code, length)

    def parse(self, data):
        self.label = data.readString()

    def __repr__(self):
        return "[ActionGotoLabel] Code: 0x%x, Length: %d, Label: '%s'" % (self._code, self._length, self.label)

# NOOP
class ActionNextFrame(Action):
    CODE = 0x04
    def __init__(self, code, length):
        super(ActionNextFrame, self).__init__(code, length)

class ActionPlay(Action):
    CODE = 0x06
    def __init__(self, code, length):
        super(ActionPlay, self).__init__(code, length)

    def __repr__(self):
        return "[ActionPlay] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionPreviousFrame(Action):
    CODE = 0x05
    def __init__(self, code, length):
        super(ActionPreviousFrame, self).__init__(code, length)

class ActionSetTarget(Action):
    CODE = 0x8b
    def __init__(self, code, length):
        self.targetName = None
        super(ActionSetTarget, self).__init__(code, length)

    def parse(self, data):
        self.targetName = data.readString()

# NOOP
class ActionStop(Action):
    CODE = 0x07
    def __init__(self, code, length):
        super(ActionStop, self).__init__(code, length)

    def __repr__(self):
        return "[ActionStop] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionStopSounds(Action):
    CODE = 0x09
    def __init__(self, code, length):
        super(ActionStopSounds, self).__init__(code, length)

class ActionToggleQuality(Action):
    CODE = 0x08
    def __init__(self, code, length):
        super(ActionToggleQuality, self).__init__(code, length)

class ActionWaitForFrame(Action):
    CODE = 0x8a
    def __init__(self, code, length):
        self.frame = 0
        self.skipCount = 0
        super(ActionWaitForFrame, self).__init__(code, length)

    def parse(self, data):
        self.frame = data.readUI16()
        self.skipCount = data.readUI8()

# =========================================================
# SWF 4 actions
# =========================================================
class ActionAdd(Action4):
    CODE = 0x0a
    def __init__(self, code, length):
        super(ActionAdd, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        try: valueA = Decimal(valueAStr)
        except TypeError:
            valueA = 0
        except InvalidOperation:
            valueA = 0

        try: valueB = Decimal(valueBStr)
        except TypeError:
            valueB = 0
        except InvalidOperation:
            valueB = 0

        action_stack.append(valueA + valueB)

    def __repr__(self):
        return "[ActionAdd] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionAnd(Action4):
    CODE = 0x10
    def __init__(self, code, length):
        super(ActionAnd, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        try: valueA = Decimal(valueAStr)
        except TypeError:
            valueA = 0
        except InvalidOperation:
            valueA = 0

        try: valueB = Decimal(valueBStr)
        except TypeError:
            valueB = 0
        except InvalidOperation:
            valueB = 0

        if self.version >= 5:
            if valueA == 0 and valueB == 0:
                action_stack.append(False)
            else:
                action_stack.append(True)
        else:
            if valueA == 0 and valueB == 0:
                action_stack.append(0)
            else:
                action_stack.append(1)

    def __repr__(self):
        return "[ActionAnd] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionEquals(Action4):
    CODE = 0x0e
    def __init__(self, code, length):
        super(ActionEquals, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        try: valueA = Decimal(valueAStr)
        except TypeError:
            valueA = 0
        except InvalidOperation:
            valueA = 0

        try: valueB = Decimal(valueBStr)
        except TypeError:
            valueB = 0
        except InvalidOperation:
            valueB = 0

        if self.version >= 5:
            if valueA == valueB:
                action_stack.append(True)
            else:
                action_stack.append(False)
        else:
            if valueA == valueB:
                action_stack.append(1)
            else:
                action_stack.append(0)

    def __repr__(self):
        return "[ActionAnd] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionNot(Action4):
    CODE = 0x12
    def __init__(self, code, length):
        super(ActionNot, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        result = 1 == data.readUI8()

        valueStr = action_stack.pop()

        try: value = Decimal(valueStr)
        except TypeError:
            value = 0
        except InvalidOperation:
            value = 0

        # print("ActionNot: version: {}, valueStr: {}, value: {}".format(self.version, valueStr, value), file=sys.stderr)

        # TODO: page 79: argument is to be evaluated as
        # decimal, why convert to boolean in SWF <4?
        #
        # In SWF 5 files, the ActionNot operator converts its argument 
        # to a Boolean value, and pushes a result of type Boolean. In 
        # SWF 4 files, the argument and result are numbers.
        if self.version >= 5:
            if value == 0:
                action_stack.append(True)
            else:
                action_stack.append(False)
        else:
            if value == 0:
                action_stack.append(1)
            else:
                action_stack.append(0)

    def __repr__(self):
        return "[ActionNot] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionPop(Action):
    CODE = 0x17

    def __init__(self, code, length):
        super(ActionPop, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        # ActionPop pops a value from the stack and discards it.
        action_stack.pop()

    def __repr__(self):
        return "[ActionPop] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionDefineFunction2(Action7):
    CODE = 0x8e

    def __init__(self, code, length):
        self.functionName = None
        self.numParams = None
        self.registerCount = None
        self.preloadParentFlag = None
        self.preloadRootFlag = None
        self.suppressSuperFlag = None
        self.preloadSuperFlag = None
        self.suppressArgumentsFlag = None
        self.preloadArgumentsFlag = None
        self.suppressThisFlag = None
        self.preloadThisFlag = None
        self.reserved = None
        self.preloadGlobalFlag = None
        self.parameters = []
        self.codeSize = None
        super(ActionDefineFunction2, self).__init__(code, length)

    def parse(self, data):

        self.functionName = data.readString()
        self.numParams = data.readUI16()
        self.registerCount = data.readUI8()
        self.preloadParentFlag = data.readUB(1)
        self.preloadRootFlag = data.readUB(1)
        self.suppressSuperFlag = data.readUB(1)
        self.preloadSuperFlag = data.readUB(1)
        self.suppressArgumentsFlag = data.readUB(1)
        self.preloadArgumentsFlag = data.readUB(1)
        self.suppressThisFlag = data.readUB(1)
        self.preloadThisFlag = data.readUB(1)
        self.reserved = data.readUB(7)
        self.preloadGlobalFlag = data.readUB(1)

        self.codeSize = data.readUI16()

        codeData  = data.readbits(self.codeSize)
        
        for i in range(self.numParams):
          self.parameters.append(data.readREGISTERPARAM())

    def __repr__(self):
        return "[ActionDefineFunction2] Code: 0x%x, Length: %d" % (self._code, self._length)


# ActionPush pushes one or more values onto the stack. The Type field 
# specifies the type of the value to be pushed.
# 
# If Type = 1, the value to be pushed is specified as a 32-bit IEEE 
# single-precision little-endian floating-point value. PropertyIds 
# are pushed as FLOATs. 
# 
# ActionGetProperty and ActionSetProperty use PropertyIds to access the
# properties of named objects.  
#
# If Type = 4, the value to be pushed is a register number. Flash Player 
# supports up to 4 registers. With the use of ActionDefineFunction2, 
# up to 256 registers can be used.
#
# In the first field of ActionPush, the length in ACTIONRECORD defines 
# the total number of Type and value bytes that follow the ACTIONRECORD 
# itself. More than one set of Type and value fields may follow the 
# first field, depending on the number of bytes that the length in 
# ACTIONRECORD specifies.
class ActionPush(Action):
    CODE = 0x96

    # Types
    STRING = 0
    FLOAT = 1
    NULL = 2
    UNDEFINED = 3
    REGISTER = 4
    BOOLEAN = 5
    DOUBLE = 6
    INTEGER = 7
    CONSTANT_8 = 8
    CONSTANT_16 = 9

    def __init__(self, code, length):
        self.type = None
        self.value = None
        super(ActionPush, self).__init__(code, length)

    def parse(self, data):
        global action_constant_pool

        self.type = data.readUI8()
        if self.STRING == self.type:
            self.value = data.readString()
        elif self.FLOAT == self.type:
            self.value = data.readFLOAT()
        elif self.REGISTER == self.type:
            self.value = data.readUI8()
        elif self.BOOLEAN == self.type:
            self.value = 1 == data.readUI8()
        elif self.DOUBLE == self.type:
            self.value = data.readFLOAT16()
        elif self.INTEGER == self.type:
            self.value = data.readUI32()
        elif self.CONSTANT_8 == self.type:
            constant_pool_index = data.readUI8()
            if len(action_constant_pool) > constant_pool_index:
                self.value = action_constant_pool[constant_pool_index]
        elif self.CONSTANT_16 == self.type:
            contant_pool_index = data.readUI16()
            if len(action_constant_pool) > constant_pool_index:
                self.value = action_constant_pool[constant_pool_index]

        global action_stack
        if not (self.value is None):
            action_stack.append(self.value)

    def __repr__(self):
        return "[ActionPush] Code: 0x%x, Length: %d, Type: %s, Value: %s" % (self._code, self._length, self.type, self.value)

class ActionGetURL2(Action):
    CODE = 0x9a
    def __init__(self, code, length):
        self.methods = [None, "GET", "POST"]

        self.sendVarsMethod = 0
        self.reserved = 0
        self.loadTarget = 0
        self.loadVariables = 0
        self.target = None
        self.url = None

        super(ActionGetURL2, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.sendVarsMethod = data.readUB(2)
        self.reserved = data.readUB(4)
        self.loadTarget = 1 == data.readUB(1)
        self.loadVariables = 1 == data.readUB(1)

        self.target = action_stack.pop()
        self.url = action_stack.pop()

    def __repr__(self):
      return "[ActionGetURL2] Code: 0x%x, Length: %d, SendVarsMethod: %d, Target: %s, URL: %s" % (self._code, self._length, self.methods[self.sendVarsMethod], self.target, self.url)

class ActionIf(Action4):
    CODE = 0x9d
    def __init__(self, code, length):
        self.name = None
        self.value = None
        super(ActionIf, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.branchOffset = data.readSI16()
        conditionNumber = action_stack.pop()

        # If Condition is true, BranchOffset bytes are added to the 
        # instruction pointer in the execution stream.  The offset is 
        # a signed quantity, enabling branches from -32768 bytes to
        # 32767 bytes. An offset of 0 points to the action directly 
        # after the ActionIf action.  When playing a SWF 4 file,
        # Condition is not converted to a Boolean value and is instead 
        # compared to 0, not true.

        if self.version == 4:
            if (bool(conditionNumber) == 0):
                data.seek(self.branchOffset)
        else:
            if (bool(conditionNumber) == True):
                data.seek(self.branchOffset)


    def __repr__(self):
        return "[ActionIf] Code: 0x%x, Length: %d, Name: %s, Value: %s" % (self._code, self._length, self.name, self.value)

class ActionGetVariable(Action):
    CODE = 0x1c
    def __init__(self, code, length):
        self.name = None
        self.value = None
        super(ActionGetVariable, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        global action_variable_context

        self.name = action_stack.pop()
        if self.name in action_variable_context:
            self.value = action_variable_context[self.name]
        else:
            print("[ActionGetVariable]: Variable not found in context: {}".format(self.name), file=sys.stderr)
            pass
        action_stack.append(self.value)

    def __repr__(self):
        return "[ActionGetVariable] Code: 0x%x, Length: %d, Name: %s, Value: %s" % (self._code, self._length, self.name, self.value)

class ActionSetVariable(Action):
    CODE = 0x1d
    def __init__(self, code, length):
        self.name = None
        self.value = None
        super(ActionSetVariable, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        global action_variable_context

        self.value = action_stack.pop()
        self.name = action_stack.pop()
        # print("ActionSetVariable: value: {}, name: {}".format(self.value,self.name), file=sys.stderr)
        action_variable_context[self.name] = self.value

    def __repr__(self):
        return "[ActionSetVariable] Code: 0x%x, Length: %d, Name: %s, Value: %s" % (self._code, self._length, self.name, self.value)

class ActionCallFunction(Action5):
    CODE = 0x3d
    def __init__(self, code, length):
        self.functionName = None
        self.numArgs = None
        super(ActionCallFunction, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.functionName = action_stack.pop()
        self.numArgs = action_stack.pop()
        # print("functionName: {}, numArgs: {}".format(self.functionName, self.numArgs), file=sys.stderr)
        try: self.numArgs = int(self.numArgs)
        except TypeError:
            return
        except ValueError:
            return
        if not (self.numArgs is None):
            for i in range(self.numArgs):
                someArg = action_stack.pop()
                # print("function {}, arg {}".format(self.functionName, someArg), file=sys.stderr) 

        action_stack.append("TODO: {} function output".format(self.__class__.__name__))

    def __repr__(self):
        return "[ActionCallFunction] Code: 0x%x, Length: %d, FunctionName: %s, NumArgs: %d" % (self._code, self._length, self.functionName, self.numArgs)

class ActionNewObject(Action5):
    CODE = 0x40
    def __init__(self, code, length):
        self.objName = None
        self.numArgs = None
        self.args = []
        super(ActionNewObject, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.objName = action_stack.pop()
        self.numArgs = action_stack.pop()

        try: self.numArgs = int(self.numArgs)
        except TypeError:
            return
        except ValueError:
            return
        if not (self.numArgs is None):
            for i in range(self.numArgs):
                someArg = action_stack.pop()
                # print("objName {}, arg {}".format(self.objName, someArg), file=sys.stderr)

        action_stack.append("TODO: {} return value".format(self.__class__.__name__))

    def __repr__(self):
        return "[ActionNewObject] Code: 0x%x, Length: %d, Name: %s, Value: %s" % (self._code, self._length, self.objName, self.numArgs)



# =========================================================
# SWF 5 actions
# =========================================================

class ActionEquals2(Action):
    CODE = 0x49
    def __init__(self, code, length):
        self.arg1 = None
        self.arg2 = None
        super(ActionEquals2, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.arg1 = action_stack.pop()
        self.arg2 = action_stack.pop()

        # The equality comparison algorithm from ECMA-262 Section 11.9.3 is applied.
        # http://www.ecma-international.org/ecma-262/5.1/
        action_stack.append("TODO: {} arg 1:2 equality result".format(self.__class__.__name__))

    def __repr__(self):
        return "[ActionEquals2] Code: 0x%x, Length: %d, Arg1: %s, Arg2: %s" % (self._code, self._length, self.arg1, self.arg2)

class ActionConstantPool(Action):
    CODE = 0x88

    def __init__(self, code, length):
        self.count = 0
        self.constants = []
        super(ActionConstantPool, self).__init__(code, length)

    def parse(self, data):
        global action_constant_pool

        self.count = data.readUI16()

        action_constant_pool = []

        for x in range(self.count):
            constant = data.readString()

            self.constants.append(constant)
            action_constant_pool.append(constant)

    def __repr__(self):
        return "[ActionConstantPool] Code: 0x%x, Length: %d, Count: %d, Constants: %s" % (self._code, self._length, self.count, self.constants)

class ActionGetMember(Action):
    CODE = 0x4e

    def __init__(self, code, length):
        self.memberName = None
        self.obj = None
        super(ActionGetMember, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        memberName = action_stack.pop()
        obj = action_stack.pop()

        if not (obj is None):
          action_stack.append("TODO: {} member value".format(self.__class__.__name__))
          #value = getattr(obj, memberName)
          #action_stack.append(value)
        else:
          action_stack.append(None)

    def __repr__(self):
        return "[ActionGetMember] Code: 0x%x, Length: %d, MemberName: %s, Object: %s" % (self._code, self._length, self.memberName, self.obj)

class ActionSetMember(Action):
    CODE = 0x4f

    def __init__(self, code, length):
        self.newValue = None
        self.objName = None
        self.obj = None
        super(ActionSetMember, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.newValue = action_stack.pop()
        self.objName = action_stack.pop()
        self.obj = action_stack.pop()

        if not (obj is None):
            #  print("ActionSetMember: obj: {}".format(self.obj), file=sys.stderr)
            #  print("ActionSetMember: obj_name: {}".format(self.objName), file=sys.stderr)
            #  print("ActionSetMember: newValue: {}".format(self.newValue), file=sys.stderr)
            setattr(obj, objName, newValue)

    def __repr__(self):
        return "[ActionSetMember] Code: 0x%x, Length: %d, NewValue: %s, ObjName: %s" % (self._code, self._length, self.newValue, self.objName)

class ActionBitRShift(Action):
    CODE = 0x64

    def __init__(self, code, length):
        self.shiftCount = 0
        self.value = None
        super(ActionBitRShift, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        shiftCountStr = action_stack.pop()
        self.shiftCount = int(shiftCountStr)
        self.value = action_stack.pop()
        #value = int(value)
        #s32 = (value + 2**31) % 2**32 - 2**31  # // convert to signed 32-bit
        #s32 = s32 >> shiftCount
        #action_stack.append(s32)
        action_stack.append("TODO: {} computed value".format(self.__class__.__name__))
        #if not (obj is None):

    def __repr__(self):
      return "[ActionBitRShift] Code: 0x%x, Length: %d, ShiftCount: %d, Value: %s" % (self._code, self._length, self.shiftCount, self.value)


# urgh! some 100 to go...

ActionTable = {}
for name, value in dict(locals()).iteritems():
    if type(value) == type and issubclass(value, Action) and hasattr(value, 'CODE'):
        ActionTable[value.CODE] = value

class SWFActionFactory(object):
    @classmethod
    def create(cls, code, length):
        return ActionTable.get(code, ActionUnknown)(code, length)

