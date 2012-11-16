from __future__ import print_function
from decimal import *
import sys
import time

# Fun With Switches
parse_inner_action_records = False
follow_jumps = False
use_bottomless_stack = True

class BottomlessStack(list):
    delegate = []
    def pop(self):
        if len(self.delegate) == 0:
            return 0
        else:
            return self.delegate.pop()
    def append(self, item):
        self.delegate.append(item)

    def __getitem__(self, index):
        if len(self.delegate) == 0:
            return 0
        else:
            return self.delegate.__getitem__(index)

if use_bottomless_stack:
    action_stack = BottomlessStack()
else:
    action_stack = []

action_variable_context = {"_global": {}}
action_constant_pool = []
action_registers = {}


class Action(object):
    def __init__(self, code, length):
        self._code = code
        self._length = length
        self._actionName = self.__class__.__name__
        global action_stack
        print("[{}] Pre-Parse Stack: {}".format(self.actionName, action_stack), file=sys.stderr)

    @property
    def code(self):
        return self._code

    @property
    def length(self):
        return self._length;

    @property
    def version(self):
        return 3

    @property
    def actionName(self):
      return self._actionName

    def parse(self, data):
        # Do nothing. Many Actions don't have a payload.
        # For the ones that have one we override this method.
        if self._length > 0:
            print("skipping {} bytes...".format(self._legth), file=sys.stderr)
            data.skip_bytes(self._length)

    def __repr__(self):
        return "[%s] Code: 0x%x, Length: %d" % (self._actionName, self._code, self._length)

class ActionUnknown(Action):
    ''' Dummy class to read unknown actions '''
    def __init__(self, code, length):
        super(ActionUnknown, self).__init__(code, length)
        #print(self, file=sys.stderr)

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
        self.url = None
        self.target = None
        super(ActionGetURL, self).__init__(code, length)

    def parse(self, data):
        self.url = data.readString()
        self.target = data.readString()

    def __repr__(self):
        return "[ActionGetURL] Code: 0x%x, Length: %d, URL: '%s', Target: '%s'" % (self._code, self._length, self.url, self.target)

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

    def __repr__(self):
        return "[ActionSetTarget] Code: 0x%x, Length: %d, TargetName: %s" % (self._code, self._length, self.targetName)

# NOOP
class ActionStop(Action):
    CODE = 0x07
    def __init__(self, code, length):
        super(ActionStop, self).__init__(code, length)

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
        # TODO skip actions

# =========================================================
# SWF 4 actions
# =========================================================

class ActionAdd(Action4):
    CODE = 0x0a
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionAdd, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        try: self.valueA = Decimal(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to decimal".format(self.actionName, valueAStr), file=sys.stderr)

        try: self.valueB = Decimal(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to decimal".format(self.actionName, valueBStr), file=sys.stderr)

        self.result = self.valueA + self.valueB
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionAdd] Code: 0x%x, Length: %d, ValueA: %d, ValueB: %d, Result: %s" % (self._code, self._length, self.valueA, self.valueB, self.result)

class ActionSubtract(Action4):
    CODE = 0x0b
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionSubtract, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        try: self.valueA = Decimal(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to decimal".format(self.actionName, valueAStr), file=sys.stderr)

        try: self.valueB = Decimal(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to decimal".format(self.actionName, valueBStr), file=sys.stderr)

        self.result = self.valueB - self.valueA
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionSubtract] Code: 0x%x, Length: %d, ValueA: %d, ValueB: %d, Result: %s" % (self._code, self._length, self.valueA, self.valueB, self.result)

class ActionMultiply(Action4):
    CODE = 0x0c
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionMultiply, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        try: self.valueA = Decimal(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to decimal".format(self.actionName, valueAStr), file=sys.stderr)

        try: self.valueB = Decimal(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to decimal".format(self.actionName, valueBStr), file=sys.stderr)

        self.result = self.valueB * self.valueA
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionMultiply] Code: 0x%x, Length: %d, ValueA: %d, ValueB: %d, Result: %s" % (self._code, self._length, self.valueA, self.valueB, self.result)

class ActionAnd(Action4):
    CODE = 0x10
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionAnd, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        try: self.valueA = Decimal(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to decimal".format(self.actionName, valueAStr), file=sys.stderr)

        try: self.valueB = Decimal(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to decimal".format(self.actionName, valueBStr), file=sys.stderr)

        bothNonZero = (self.valueA != 0 and self.valueB != 0)

        if self.version < 5:
            if bothNonZero:
                bothNonZero = 1
            else:
                bothNonZero = 0

        self.result = bothNonZero
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionAnd] Code: 0x%x, Length: %d, ValueA: %d, ValueB: %d, Result: %s" % (self._code, self._length, self.valueA, self.valueB, self.result)

class ActionOr(Action4):
    CODE = 0x11
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionOr, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        try: self.valueA = Decimal(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to decimal".format(self.actionName, valueAStr), file=sys.stderr)

        try: self.valueB = Decimal(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to decimal".format(self.actionName, valueBStr), file=sys.stderr)

        eitherNonZero =  (self.valueA != 0 or self.valueB != 0)

        if self.version < 5:
            if eitherNonZero:
                eitherNonZero = 1
            else:
                eitherNonZero = 0

        self.result = eitherNonZero
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionOr] Code: 0x%x, Length: %d, ValueA: %d, ValueB: %d, Result: %s" % (self._code, self._length, self.valueA, self.valueB, self.result)

class ActionDivide(Action4):
    CODE = 0x0d

    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = 0
        super(ActionDivide, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        try: self.valueA = Decimal(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to decimal".format(self.actionName, valueAStr), file=sys.stderr)

        try: self.valueB = Decimal(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to decimal".format(self.actionName, valueBStr), file=sys.stderr)

        if self.valueB != 0:
            self.result = (self.valueB / self.valueB)

        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionDivide] Code: 0x%x, Length: %d, ValueA: %d, ValueB: %d, Result: %s" % (self._code, self._length, self.valueA, self.valueB, self.result)

class ActionEquals(Action4):
    CODE = 0x0e

    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionEquals, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        try: self.valueA = Decimal(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to decimal".format(self.actionName, valueAStr), file=sys.stderr)

        try: self.valueB = Decimal(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to decimal".format(self.actionName, valueBStr), file=sys.stderr)


        self.result = (self.valueA == self.valueB)
        if self.version >= 5:
            action_stack.append(self.result)
        else:
            if self.result:
                action_stack.append(1)
            else:
                action_stack.append(0)

    def __repr__(self):
        return "[ActionEquals] Code: 0x%x, Length: %d, ValueA: %d, ValueB: %d, Result: %s" % (self._code, self._length, self.valueA, self.valueB, self.result)

class ActionLess(Action4):
    CODE = 0x0f

    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionLess, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        if valueAStr == None:
          valueAStr = '0'
        if valueBStr == None:
          valueBStr = '0'

        try: self.valueA = Decimal(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to integer".format(self.actionName, valueAStr), file=sys.stderr)

        try: self.valueB = Decimal(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to integer".format(self.actionName, valueBStr), file=sys.stderr)

        self.result = self.valueB < self.valueA
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionLess] Code: 0x%x, Length: %d, ValueA: %d, ValueB: %d, Result: %s" % (self._code, self._length, self.valueA, self.valueB, self.result)

class ActionNot(Action4):
    CODE = 0x12
    def __init__(self, code, length):
        self.value = 0
        self.result = None
        super(ActionNot, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        # TODO: why do we need this? P.79 of the spec has poor language.  Seems to break
        # stream if we read it.
        #self.result = data.readBoolean()

        valueStr = action_stack.pop()

        try: self.value = Decimal(valueStr)
        except: 
            print("[{}]: error converting value '{}' to decimal".format(self.actionName, valueStr), file=sys.stderr)
            pass # "Converts the value to floating point; non-numeric values evaluate to 0."

        # TODO: page 79: argument is to be evaluated as
        # decimal, why convert to boolean in SWF <4?
        #
        # In SWF 5 files, the ActionNot operator converts its argument 
        # to a Boolean value, and pushes a result of type Boolean. In 
        # SWF 4 files, the argument and result are numbers.

        self.result = (self.value == 0)

        if self.version >= 5:
             action_stack.append(self.result)
        else:
            if self.result:
                action_stack.append(1)
            else:
                action_stack.append(0)

    def __repr__(self):
      return "[ActionNot] Code: 0x%x, Length: %d, Result: %s, Value: %d" % (self._code, self._length, self.result, self.value)

class ActionStringExtract(Action4):
    CODE = 0x15
    def __init__(self, code, length):
        self.target = None
        self.count = 0
        self.index = 0
        self.substring = ""
        super(ActionStringExtract, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        countString = action_stack.pop()
        indexString = action_stack.pop()
        self.target = action_stack.pop()

        # fugly.  it's late.

        failed = False

        try: self.count = int(countString)
        except:
          failed = True

        try: self.index = int(indexString)
        except:
          failed = True

        if not (self.target is None) and not failed:
            self.substring = self.target[self.index:self.count]

        action_stack.append(self.substring)

    def __repr__(self):
        return "[ActionStringExtract] Code: 0x%x, Length: %d, Target: %s, Count: %d, Index: %d" % (self._code, self._length, self.target, self.count, self.index)

# TODO
class ActionMBStringExtract(ActionStringExtract):
    CODE = 0x35

class ActionStringEquals(Action4):
    CODE = 0x13
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionStringEquals, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.valueA = action_stack.pop()
        self.valueB = action_stack.pop()
        self.result = self.valueA == self.valueB
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionStringEquals] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionStringLength(Action4):
    CODE = 0x14
    def __init__(self, code, length):
        self.target = None
        self.stringLength = 0
        super(ActionStringLength, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.target = action_stack.pop()
        if not (self.target is None):
            self.target = str(self.target)
        # TODO
        self.stringLength = 0
        action_stack.append(self.stringLength)

    def __repr__(self):
        return "[ActionStringLength] Code: 0x%x, Length: %d, Target: %s, StringLength: %d" % (self._code, self._length, self.target, self.stringLength)

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

class ActionToInteger(Action4):
    CODE = 0x18
    def __init__(self, code, length):
        self.integerValue = 0
        super(ActionToInteger, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        sourceValue = action_stack.pop()
        # TODO
        action_stack.append(self.integerValue)

    def __repr__(self):
        return "[ActionToInteger] Code: 0x%x, Length: %d, IntegerValue: %d" % (self._code, self._length, self.integerValue)

class ActionWith(Action5):
    CODE = 0x94
    def __init__(self, code, length):
        self.codeSize = 0
        self.targetObject = None
        self.functionBody = []
        super(ActionWith, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.codeSize = data.readUI16()
        self.targetObject = action_stack.pop()
         
        global parse_inner_action_records
        if parse_inner_action_records:
            bodyEndPosition = data.tell() + self.codeSize
            print("START ACTIONWITH: (codeSize: {}, range: {} -> {})".format(self.codeSize, data.tell(), bodyEndPosition), file=sys.stderr)
            while data.tell() < bodyEndPosition:
                ret = data.readACTIONRECORD()
                self.functionBody.append(ret)
                print("ACTIONWITH: (position after read: {} of {})".format(data.tell(), bodyEndPosition), file=sys.stderr)
    
            if data.tell() !=  bodyEndPosition:
                print("ACTIONWITH: (repositioning after final read: {} -> {})".format(data.tell(), bodyEndPosition), file=sys.stderr)
                data.seek(bodyEndPosition)
    
            print("END ACTIONWITH", file=sys.stderr)
        else:
            data.skip_bytes(self.codeSize)

    def __repr__(self):
        return "[ActionWith] Code: 0x%x, Length: %d, CodeSize: %d, FunctionBody: %s" % (self._code, self._length, self.codeSize, self.functionBody)




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
class ActionPush(Action4):
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
        self.values = []
        super(ActionPush, self).__init__(code, length)

    def parse(self, data):

        global action_stack
        global action_registers
        global action_constant_pool

        currentPosition = data.tell()
        nextPosition = currentPosition + self.length

        print("[{}]: currentPosition: {}, length: {}, nextPosition: {}".format(self.actionName, currentPosition, self.length, nextPosition), file=sys.stderr)

        while (data.tell() < nextPosition):

            validType = True
            value = None

            self.type = data.readUI8()

            if self.STRING == self.type:
                value = data.readString()
            elif self.FLOAT == self.type:
                value = data.readFLOAT()
            elif self.REGISTER == self.type:
                value = data.readUI8()
                #key = data.readUI8()
                #try:value = action_registers[key]
                #except KeyError:
                #    print("[{}]: Register {} not found.  Returning number itself instead.".format(self.actionName, key), file=sys.stderr)
                #    value = "unresolved register key: " + key
            elif self.BOOLEAN == self.type:
                value = data.readBoolean()
            elif self.DOUBLE == self.type:
                #value = data.readFLOAT16()
                value = data.readDOUBLE()
            elif self.INTEGER == self.type:
                value = data.readUI32()
            elif self.CONSTANT_8 == self.type:
                constant_pool_index = data.readUI8()
                print("[{}]: Constant pool index {}".format(self.actionName, constant_pool_index), file=sys.stderr)
                try:    value = action_constant_pool[constant_pool_index]
                except IndexError:
                    print("[{}]: Constant pool index {} larger than pool size {}".format(self.actionName, constant_pool_index, len(action_constant_pool)), file=sys.stderr)
                    value = -1 
            elif self.CONSTANT_16 == self.type:
                constant_pool_index = data.readUI16()
                try:    value = action_constant_pool[constant_pool_index]
                except IndexError:
                    value = -1
            elif self.NULL != self.type and self.UNDEFINED != self.type:
                print("invalid type {}, not pushing to stack".format(self.type), file=sys.stderr)
                validType = False
    
            record = { 'type': self.type, 'isValidType': validType }

            if validType:
                print("[{}]: Pushing value (type {}) value: {}, now at position {} of {}".format(self.actionName, self.type, value, data.tell(), nextPosition), file=sys.stderr)
                action_stack.append(value) 
                record['value'] = value
            else:
                raise TypeError, "invalid type {}".format(self.type)

            # for reporting only
            self.values.append(record)

        if data.tell() != nextPosition:
            print("[{}]: repositioning after final push: {} -> {}".format(self.actionName, data.tell(), nextPosition), file=sys.stderr)
            data.seek(nextPosition)
    
    def __repr__(self):
        return "[ActionPush] Code: 0x%x, Length: %d, Type: %s, Values: %s" % (self._code, self._length, self.type, self.values)

class ActionJump(Action4):
    CODE = 0x99
    def __init__(self, code, length):
        self.branchOffset = 0
        super(ActionJump, self).__init__(code, length)

    def parse(self, data):

        self.branchOffset = data.readSI16()

        global follow_jumps
        if follow_jumps:
            startPos = data.tell()
            if self.branchOffset == 0:
                print("[{}]: IF-JUMP: NOT skipping {} bytes".format(self.actionName, self.branchOffset), file=sys.stderr)
            else:
                newPos = startPos + self.branchOffset
                print("[{}]: JUMP: currentPosition: {}, newPosition: {}, branchOffset: {}".format(self.actionName, startPos, newPos, self.branchOffset), file=sys.stderr)
                data.seek(newPos)

    def __repr__(self):
        return "[ActionJump] Code: 0x%x, Length: %d, BranchOffset: %d" % (self._code, self._length, self.branchOffset)

class ActionGetURL2(Action4):
    CODE = 0x9a
    def __init__(self, code, length):
        self.methods = [None, "GET", "POST"]

        print("length: {}".format(length), file=sys.stderr)
        self.sendVarsMethod = 0
        self.reserved = 0
        self.loadTarget = 0
        self.loadVariables = False
        self.target = None
        self.url = None

        super(ActionGetURL2, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.sendVarsMethod = data.readUB(2)
        self.reserved = data.readUB(4)
        self.loadTarget = data.readUB(1)
        self.loadVariables = data.readBoolean()

        self.target = action_stack.pop()
        self.url = action_stack.pop()

    def __repr__(self):
        return "[ActionGetURL2] Code: 0x%x, Length: %d, SendVarsMethod: %s, Target: %s, URL: %s" % (self._code, self._length, self.methods[self.sendVarsMethod], self.target, self.url)

class ActionDefineFunction(Action5):
    CODE = 0x9b

    def __init__(self, code, length):
        self.functionName = None
        self.numParams = 0
        self.parameters = []
        self.codeSize = 0
        self.functionBody = []
        super(ActionDefineFunction, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        global action_variable_context

        self.functionName = data.readString()
        self.numParams = data.readUI16()
        
        if self.functionName == '':
            self.functionName = None
        
        if self.numParams > 0:
            for i in range(self.numParams):
                self.parameters.append(data.readString())

        self.codeSize = data.readUI16()

        global parse_inner_action_records
        if parse_inner_action_records:
            bodyEndPosition = data.tell() + self.codeSize
            print("START PARSE (codeSize: {}, range: {} -> {})".format(self.codeSize, data.tell(), bodyEndPosition), file=sys.stderr)
            while data.tell() < bodyEndPosition:
                ret = data.readACTIONRECORD()
                self.functionBody.append(ret)
                print("PARSE: (position after read: {} of {})".format(data.tell(), bodyEndPosition), file=sys.stderr)
    
            if data.tell() !=  bodyEndPosition:
                print("PARSE: (repositioning after final read: {} -> {})".format(data.tell(), bodyEndPosition), file=sys.stderr)
                data.seek(bodyEndPosition)
    
            print("END PARSE", file=sys.stderr)
        else:
            data.skip_bytes(self.codeSize)
    
        functionStub = { 'functionName': self.functionName, 'action': self.actionName, 'parameters': self.parameters, 'body': self.functionBody }
        if (self.functionName is None):
            #pass
            action_stack.append(functionStub)
        else: 
            action_variable_context[self.functionName] = functionStub


    def __repr__(self):
        return "[ActionDefineFunction] Code: 0x%x, Length: %d, FunctionName: %s, NumParams: %d" % (self._code, self._length, self.functionName, self.numParams)

class ActionIf(Action4):
    CODE = 0x9d
    def __init__(self, code, length):
        self.branchOffset = 0
        self.conditionNumber = False
        super(ActionIf, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        # If Condition is true, BranchOffset bytes are added to the 
        # instruction pointer in the execution stream.  The offset is 
        # a signed quantity, enabling branches from -32768 bytes to
        # 32767 bytes. An offset of 0 points to the action directly 
        # after the ActionIf action.  When playing a SWF 4 file,
        # Condition is not converted to a Boolean value and is instead 
        # compared to 0, not true.
        #totalOffset = 0

        self.branchOffset = data.readSI16()

        self.conditionNumber = action_stack.pop()

        global follow_jumps
        if follow_jumps:
            startPos = data.tell()
            if (self.version == 4 and self.conditionNumber != 0) or (bool(self.conditionNumber) == True):
                if self.branchOffset == 0:
                    print("[{}]: IF-JUMP: NOT skipping {} bytes".format(self.actionName, self.branchOffset), file=sys.stderr)
                else:
                    newPos = startPos + self.branchOffset
                    print("[{}]: IF-JUMP: currentPosition: {}, newPosition: {}, branchOffset: {}".format(self.actionName, startPos, newPos, self.branchOffset), file=sys.stderr)
                    data.seek(newPos)
    
    def __repr__(self):
        return "[ActionIf] Code: 0x%x, Length: %d, BranchOffset: %s, ConditionNumber: %s" % (self._code, self._length, self.branchOffset, self.conditionNumber)

class ActionGetVariable(Action):
    CODE = 0x1c
    def __init__(self, code, length):
        self.variableName = None
        self.variableValue = None
        super(ActionGetVariable, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        global action_variable_context

        self.variableName = action_stack.pop()
        if hasattr(self.variableName, 'keys'):
            print("[{}]: Hacking Variable of Emulated Object: {}".format(self.actionName, self.variableName), file=sys.stderr)
            self.variableName = self.variableName['emulatedValue']

        if self.variableName in action_variable_context:
            self.variableValue = action_variable_context[self.variableName]
        else:
            print("[{}]: Variable not found in context: {}".format(self.actionName, self.variableName), file=sys.stderr)

        action_stack.append(self.variableValue)

    def __repr__(self):
        return "[ActionGetVariable] Code: 0x%x, Length: %d, VariableName: %s, VariableValue: %s" % (self._code, self._length, self.variableName, self.variableValue)

class ActionSetVariable(Action):
    CODE = 0x1d
    def __init__(self, code, length):
        self.variableName = None
        self.variableValue = None
        super(ActionSetVariable, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        global action_variable_context

        self.variableValue = action_stack.pop()
        self.variableName = action_stack.pop()

        if not (self.variableName is None):
            # HACK
            if hasattr(self.variableName, 'keys'):
              print("[{}]: hack: converting variableName to string so it can be added as dictionary key: {}".format(self.actionName, self.variableName), file=sys.stderr)
              self.variableName = str(self.variableName.keys()[0])

            print("[{}]: Setting variable: {} -> {}".format(self.actionName, self.variableName, self.variableValue), file=sys.stderr)
            action_variable_context[self.variableName] = self.variableValue

    def __repr__(self):
        return "[ActionSetVariable] Code: 0x%x, Length: %d, VariableName: %s, VariableValue: %s" % (self._code, self._length, self.variableName, self.variableValue)

class ActionSetTarget2(Action4):
    CODE = 0x20
    def __init__(self, code, length):
        self.target= None
        super(ActionSetTarget2, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.target = action_stack.pop()

    def __repr__(self):
        return "[ActionSetTarget2] Code: 0x%x, Length: %d, Target: %s" % (self._code, self._length, self.target)

class ActionStringAdd(Action4):
    CODE = 0x21
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionStringAdd, self).__init__(code, length)

    def parse(self, data):

        global action_stack

        self.valueA = action_stack.pop()
        self.valueB = action_stack.pop()

        # TODO
        #self.result =  self.valueA + self.valueB
        self.result =   "CONCAT"
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionStringLess] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionGetProperty(Action):
    CODE = 0x22
    def __init__(self, code, length):
        self.index = None
        self.target = None
        super(ActionGetProperty, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.index = action_stack.pop()
        self.target = action_stack.pop()
        action_stack.append("TODO {}".format(self.actionName))

    def __repr__(self):
        return "[ActionGetProperty] Code: 0x%x, Length: %d, Index: %s, Target: %s" % (self._code, self._length, self.index, self.target)

class ActionCloneSprite(Action):
    CODE = 0x24
    def __init__(self, code, length):
        self.depth = 0
        self.target = None
        self.source = None
        super(ActionCloneSprite, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.depth = action_stack.pop()
        self.target = action_stack.pop()
        self.source = action_stack.pop()

        # TODO: impl

    def __repr__(self):
        return "[ActionCloneSprite] Code: 0x%x, Length: %d, Depth: %s, Target: %s, Source: %s" % (self._code, self._length, self.depth, self.target, self.source)

class ActionSetProperty(Action):
    CODE = 0x23
    def __init__(self, code, length):
        self.propertyValue = None
        self.index = None
        self.target = None
        super(ActionSetProperty, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.propertyValue = action_stack.pop()
        self.index = action_stack.pop()
        self.target = action_stack.pop()

        # TODO: impl

    def __repr__(self):
        return "[ActionSetProperty] Code: 0x%x, Length: %d, PropertyValue: %s, Index: %s, Target: %s" % (self._code, self._length, self.propertyValue, self.index, self.target)

class ActionStringLess(Action4):
    CODE = 0x29
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionStringLess, self).__init__(code, length)

    def parse(self, data):

        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        if valueAStr == None:
          valueAStr = '0'
        if valueBStr == None:
          valueBStr = '0'

        try: self.valueA = int(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to integer".format(self.actionName, valueAStr), file=sys.stderr)
        
        try: self.valueB = int(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to integer".format(self.actionName, valueBStr), file=sys.stderr)
        
        # TODO string byte by byte comparison
        self.result = 1
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionStringLess] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionRemoveSprite(Action4):
    CODE = 0x25
    def __init__(self, code, length):
        self.target = None
        super(ActionRemoveSprite, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.target = action_stack.pop()

    def __repr__(self):
        return "[ActionRemoveSprite] Code: 0x%x, Length: %d, Target: %s" % (self._code, self._length, self.target)

class ActionTrace(Action5):
    CODE = 0x26
    def __init__(self, code, length):
        self.value = None
        super(ActionTrace, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.value = action_stack.pop()
        # NOOP

    def __repr__(self):
        return "[ActionTrace] Code: 0x%x, Length: %d, Value: %s" % (self._code, self._length, self.value)

class ActionStartDrag(Action4):
    CODE = 0x27
    def __init__(self, code, length):
        self.target = None
        self.lockCenter = 0
        self.constraint = 0
        super(ActionStartDrag, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.target = action_stack.pop()
        self.lockCenter = int(action_stack.pop())
        constraintStr = action_stack.pop()
        try:self.constraint = int(constraintStr)
        except: 
            # TODO
            pass

        if self.constraint != 0:
            y2 = action_stack.pop()
            x2 = action_stack.pop()
            y1 = action_stack.pop()
            x1 = action_stack.pop()

    def __repr__(self):
        return "[ActionStartDrag] Code: 0x%x, Length: %d, Target: %s" % (self._code, self._length, self.target)

# NOOP
class ActionEndDrag(Action4):
    CODE = 0x28
    def __init__(self, code, length):
        super(ActionEndDrag, self).__init__(code, length)

class ActionDefineLocal(Action5):
    CODE = 0x3c
    def __init__(self, code, length):
        self.varName = None
        self.varValue = None
        super(ActionDefineLocal, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        global action_variable_context
        self.varValue = action_stack.pop()
        self.varName = action_stack.pop()
        action_variable_context[self.varName] = self.varValue

    def __repr__(self):
        return "[ActionDefineLocal] Code: 0x%x, Length: %d, VarName: %s, VarValue: %s" % (self._code, self._length, self.varName, self.varValue)

class ActionCallFunction(Action5):
    CODE = 0x3d
    def __init__(self, code, length):
        self.functionName = None
        self.numArgs = 0
        self.args = []
        super(ActionCallFunction, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        global action_variable_context

        self.functionName = action_stack.pop()

        numArgsStr = action_stack.pop()
        try: self.numArgs = int(numArgss)
        except:
            print("[{}]: unable to convert numArgs to a int: {}".format(self.actionName, numArgsStr), file=sys.stderr)

        if not (self.numArgs is None) and self.numArgs > 0:
            for i in range(self.numArgs):
                someArg = action_stack.pop()
                print("[{}]: HELLO function {}, i {}, arg {}".format(self.actionName, self.functionName, i, someArg), file=sys.stderr) 
                self.args.append(someArg)

        functionRef = None
        if not (self.functionName is None):
            try: functionRef = action_variable_context[self.functionName]
            except KeyError:
                pass

        try:
            codeData = functionRef['codeData']
            print("[{}]: should we execute this? {}".format(self.actionName, codeData), file=sys.stderr)
        except:
            pass

        functionResult = {'name':'functionResult', 'action':self.actionName, 'functionRef':functionRef, 'functionName': self.functionName, 'args': self.args, 'emulatedValue': 0 }
        action_stack.append(functionResult)

    def __repr__(self):
        return "[ActionCallFunction] Code: 0x%x, Length: %d, FunctionName: %s, NumArgs: %d" % (self._code, self._length, self.functionName, self.numArgs)

class ActionAsciiToChar(Action4):
    CODE = 0x33
    def __init__(self, code, length):
        self.asciiValue = 0
        self.charValue = None
        super(ActionAsciiToChar, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        asciiValueStr = action_stack.pop()
        #print("YOYO: ASCII:{}".format(asciiValueStr), file=sys.stderr)
        #self.asciiValue = int(asciiValueStr)
        #self.charValue = chr(self.asciiValue)
        # TODO
        action_stack.append(chr(65))

    def __repr__(self):
        return "[ActionAsciiToChar] Code: 0x%x, Length: %d, AsciiValue: %d, CharValue: %s" % (self._code, self._length, self.asciiValue, self.charValue)


class ActionRandomNumber(Action5):
    CODE = 0x30
    def __init__(self, code, length):
        self.maxValue = 0
        self.randomValue = 0
        super(ActionRandomNumber, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        maxValueStr = action_stack.pop()
        try: self.maxValue = int(maxValueStr)
        except: 
            # TODO
            pass

        # TODO
        self.randomValue = 0
        action_stack.append(self.randomValue)

    def __repr__(self):
        return "[ActionRandomNumber] Code: 0x%x, Length: %d, MaxValue: %d, RandomValue: %d" % (self._code, self._length, self.maxValue, self.randomValue)

# TODO MB?
class ActionMBStringLength(ActionStringLength):
    CODE = 0x31

class ActionCharToAscii(Action4):
    CODE = 0x32
    def __init__(self, code, length):
        self.charValue = None
        self.asciiValue = 0
        super(ActionCharToAscii, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.charValue = action_stack.pop()
        # TODO
        #self.asciiValue = ord(self.charValue[0])
        self.asciiValue = 20
        action_stack.append(self.asciiValue)

    def __repr__(self):
        return "[ActionCharToAscii] Code: 0x%x, Length: %d, AsciiValue: %d, CharValue: %s" % (self._code, self._length, self.asciiValue, self.charValue)
# TODO
class ActionMBCharToAscii(ActionCharToAscii):
    CODE = 0x36

# TODO: multi byte
class ActionMBAsciiToChar(ActionAsciiToChar):
    CODE = 0x37

    def __repr__(self):
        return "[ActionMBAsciiToChar] Code: 0x%x, Length: %d, AsciiValue: %d, CharValue: %s" % (self._code, self._length, self.asciiValue, self.charValue)

class ActionGetTime(Action5):
    CODE = 0x34

    def __init__(self, code, length):
        super(ActionGetTime, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        action_stack.append(time.time())

class ActionDelete(Action5):
    CODE = 0x3a
    def __init__(self, code, length):
        self.propertyName = None
        self.targetObject = None
        super(ActionDelete, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.propertyName = action_stack.pop()
        self.targetObject = action_stack.pop()
        # remove property
        if (not (self.targetObject is None) and not (self.propertyName is None)):
            try:del self.targetObject[self.propertyName]
            except:
                print("[{}]: cannot delete property name {} becuse it does not exist".format(self.actionName, self.propertyName), file=sys.stderr)

        # https://github.com/mozilla/shumway/blob/master/src/avm1/interpreter.js
        action_stack.append(None) # XXX undocumented ???

    def __repr__(self):
        return "[ActionDelete] Code: 0x%x, Length: %d, PropertyName: %s, TargetObject: %s" % (self._code, self._length, self.propertyName, self.targetObject)

class ActionDelete2(Action5):
    CODE = 0x3b
    def __init__(self, code, length):
        self.propertyName = None
        super(ActionDelete2, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.propertyName = action_stack.pop()
        # TODO
        # https://github.com/mozilla/shumway/blob/master/src/avm1/interpreter.js
        action_stack.append(None) # XXX undocumented ???

    def __repr__(self):
        return "[ActionDelete2] Code: 0x%x, Length: %d, PropertyName: %s" % (self._code, self._length, self.propertyName)

class ActionReturn(Action5):
    CODE = 0x3e
    def __init__(self, code, length):
        self.returnValue = None
        super(ActionReturn, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.returnValue = action_stack.pop()

    def __repr__(self):
        return "[ActionReturn] Code: 0x%x, Length: %d, ReturnValue: %s" % (self._code, self._length, self.returnValue)

class ActionModulo(Action5):
    CODE = 0x3f
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.returnValue = None
        super(ActionModulo, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        if valueAStr == None:
          valueAStr = '0'
        if valueBStr == None:
          valueBStr = '0'

        try: self.valueA = int(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to integer".format(self.actionName, valueAStr), file=sys.stderr)

        try: self.valueB = int(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to integer".format(self.actionName, valueBStr), file=sys.stderr)

        try: self.returnValue = self.valueB % self.valueA
        except: self.returnValue = 0

        if self.returnValue == 0:
            self.returnValue = None

        action_stack.append(self.returnValue)

    def __repr__(self):
        return "[ActionModulo] Code: 0x%x, Length: %d, ValueA: %d, ValueB: %d, ReturnValue: %s" % (self._code, self._length, self.valueA, self.valueB, self.returnValue)

class ActionNewObject(Action5):
    CODE = 0x40
    def __init__(self, code, length):
        self.objName = None
        self.numArgs = 0
        self.args = []
        super(ActionNewObject, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.objName = action_stack.pop()
        numArgsStr = action_stack.pop()

        newObject = { 'name': self.objName }

        try: self.numArgs = int(numArgsStr)
        except:
            print("[{}]: unable to convert numArgs to a int: {}".format(self.actionName, numArgsStr), file=sys.stderr)

        if not (self.numArgs is None) and self.numArgs > 0:
            for i in range(self.numArgs):
                someArg = action_stack.pop()
                print("[{}]: objName {}, arg {}".format(self.actionName, self.objName, someArg), file=sys.stderr)
                self.args.append(someArg)

        newObject['args'] = self.args

        action_stack.append(newObject)

    def __repr__(self):
        return "[ActionNewObject] Code: 0x%x, Length: %d, ObjectName: %s, NumArgs: %s" % (self._code, self._length, self.objName, self.numArgs)

class ActionInitArray(Action5):
    CODE = 0x42
    def __init__(self, code, length):
        self.numArgs = 0
        super(ActionInitArray, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        numArgsStr = action_stack.pop()

        try: self.numArgs = int(numArgsStr)
        except:
            print("[{}]: unable to convert numArgs to a int: {}".format(self.actionName, numArgsStr), file=sys.stderr)

        newArray = []

        if not (self.numArgs is None) and self.numArgs > 0:
            for i in range(self.numArgs):
                item = action_stack.pop()
                newArray.append(item)

        action_stack.append(newArray)

    def __repr__(self):
        return "[ActionInitArray] Code: 0x%x, Length: %d, NumArgs: %s" % (self._code, self._length, self.numArgs)

class ActionInitObject(Action5):
    CODE = 0x43
    def __init__(self, code, length):
        self.numArgs = 0
        super(ActionInitObject, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        numArgsStr = action_stack.pop()

        try: self.numArgs = int(numArgsStr)
        except:
            print("[{}]: unable to convert numArgs to a int: {}".format(self.actionName, numArgsStr), file=sys.stderr)

        newObject = {}

        if not (self.numArgs is None) and self.numArgs > 0:
            for i in range(self.numArgs):
                varValue  = action_stack.pop()
                varName = action_stack.pop()

                # HACK
                if hasattr(varName, 'keys'):
                  print("[{}]: hack: converting varName to string so it can be added as dictionary key: {}".format(self.actionName, varName), file=sys.stderr)
                  varName = str(varName['emulatedValue']) + '-' + str(i)

                print("[{}]: new object params: {} -> {}".format(self.actionName, varName, varValue), file=sys.stderr)
                newObject[varName] = varValue

        action_stack.append(newObject)

    def __repr__(self):
        return "[ActionInitObject] Code: 0x%x, Length: %d, NumArgs: %s" % (self._code, self._length, self.numArgs)

class ActionTypeOf(Action5):
    CODE = 0x44
    def __init__(self, code, length):
        self.value = None
        super(ActionTypeOf, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.value = action_stack.pop()
        action_stack.append(None) # TODO push type of self.value

    def __repr__(self):
        return "[ActionTypeOf] Code: 0x%x, Length: %d, Value: %s" % (self._code, self._length, self.value)

class ActionTargetPath(Action5):
    CODE = 0x45
    def __init__(self, code, length):
        self.targetObject = None
        super(ActionTargetPath, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.targetObject = action_stack.pop()
        action_stack.append(None) # TODO push target path

    def __repr__(self):
        return "[ActionTargetPath] Code: 0x%x, Length: %d, TargetObject: %s" % (self._code, self._length, self.targetObject)

class ActionDefineLocal2(Action5):
    CODE = 0x41
    def __init__(self, code, length):
        self.variableName = None
        super(ActionDefineLocal2, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        global action_variable_context
        self.variableName = action_stack.pop()
        action_variable_context[self.variableName] = None

    def __repr__(self):
        return "[ActionDefineLocal2] Code: 0x%x, Length: %d, VariableName: %s" % (self._code, self._length, self.variableName)


# =========================================================
# SWF 5 actions
# =========================================================

class ActionEquals2(Action):
    CODE = 0x49
    def __init__(self, code, length):
        self.arg1 = None
        self.arg2 = None
        self.result = None
        super(ActionEquals2, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.arg1 = action_stack.pop()
        self.arg2 = action_stack.pop()

        # TODO: The equality comparison algorithm from ECMA-262 Section 11.9.3 is applied.
        # http://www.ecma-international.org/ecma-262/5.1/
        self.result = (self.arg1 == self.arg2)
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionEquals2] Code: 0x%x, Length: %d, Arg1: %s, Arg2: %s, Result: %s" % (self._code, self._length, self.arg1, self.arg2, self.result)

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

class ActionEnumerate(Action5):
    CODE = 0x46
    def __init__(self, code, length):
        self.targetObject = 0
        super(ActionEnumerate, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.targetObject = action_stack.pop()
        action_stack.append(None)

#        # TODO: how to enumerate this?
#        if hasattr(self.targetObject, 'keys'):
#            for key in self.targetObject.keys():
#                print("KEYYYY {}".format(key), file=sys.stderr)
#                action_stack.append(key)

    def __repr__(self):
        return "[ActionEnumerate] Code: 0x%x, Length: %d, TargetObject: %s" % (self._code, self._length, self.targetObject)

class ActionAdd2(ActionAdd):
    CODE = 0x47
    def __init__(self, code, length):
        super(ActionAdd2, self).__init__(code, length)

    def __repr__(self):
        return "[ActionAdd2] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionLess2(Action5):
    CODE = 0x48
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionLess2, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        if valueAStr == None:
          valueAStr = '0'
        if valueBStr == None:
          valueBStr = '0'

        try: self.valueA = Decimal(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to integer".format(self.actionName, valueAStr), file=sys.stderr)

        try: self.valueB = Decimal(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to integer".format(self.actionName, valueBStr), file=sys.stderr)

        self.result = self.valueB < self.valueA
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionLess2] Code: 0x%x, Length: %d, ValueA: %d, ValueB: %d, ResultValue: %s" % (self._code, self._length, self.valueA, self.valueB, self.result)

class ActionToNumber(Action5):
    CODE = 0x4a
    def __init__(self, code, length):
        self.targetObject = None
        super(ActionToNumber, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.targetObject = action_stack.pop()
        # TODO
        action_stack.append(0)

    def __repr__(self):
        return "[ActionToNumber] Code: 0x%x, Length: %d, TargetObject: %s" % (self._code, self._length, self.targetObject)

class ActionToString(Action5):
    CODE = 0x4b
    def __init__(self, code, length):
        self.targetObject = None
        super(ActionToString, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.targetObject = action_stack.pop()
        action_stack.append(self.targetObject.__class__.__name__)

    def __repr__(self):
        return "[ActionToString] Code: 0x%x, Length: %d, TargetObject: %s" % (self._code, self._length, self.targetObject)

class ActionPushDuplicate(Action5):
    CODE = 0x4c
    def __init__(self, code, length):
        self.duplicateValue = None
        super(ActionPushDuplicate, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.duplicateValue = action_stack[-1]
        action_stack.append(self.duplicateValue)

    def __repr__(self):
        return "[ActionPushDuplicate] Code: 0x%x, Length: %d, DuplicateValue: %s" % (self._code, self._length, self.duplicateValue)

class ActionStackSwap(Action5):
    CODE = 0x4d
    def __init__(self, code, length):
        self.valueA = None
        self.valueB = None
        super(ActionStackSwap, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.valueA = action_stack.pop()
        self.valueB = action_stack.pop()
        action_stack.append(self.valueB)
        action_stack.append(self.valueA)

    def __repr__(self):
        return "[ActionStackSwap] Code: 0x%x, Length: %d, DuplicateValue: %s" % (self._code, self._length, self.valueA)

class ActionGetMember(Action):
    CODE = 0x4e
    def __init__(self, code, length):
        self.memberName = None
        self.targetObject = None
        self.value = None
        super(ActionGetMember, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.memberName = action_stack.pop()
        self.targetObject = action_stack.pop()

        #try: self.value = getattr(self.targetObject, self.memberName)
        try: self.value = self.targetObject[self.memberName]
        except:
            print("[{}]: Cannot get value from targetObject {}, member {}".format(self.actionName, self.targetObject, self.memberName), file=sys.stderr)

        action_stack.append(self.value)

    def __repr__(self):
        return "[ActionGetMember] Code: 0x%x, Length: %d, MemberName: %s, Object: %s" % (self._code, self._length, self.memberName, self.targetObject)

class ActionSetMember(Action):
    CODE = 0x4f
    def __init__(self, code, length):
        self.newValue = None
        self.memberName = None
        self.targetObject = None
        super(ActionSetMember, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.newValue = action_stack.pop()
        self.memberName = action_stack.pop()
        self.targetObject = action_stack.pop()

        if (self.targetObject is None) or (self.memberName is None):
            print("[{}]: Missing targetObject or memberName: targetObject: {}, memberName: {}, newValue: {}".format(self.actionName, self.targetObject, self.memberName, self.newValue), file=sys.stderr)
        else:
            #try: setattr(self.targetObject, self.memberName, self.newValue)
            try: self.targetObject[self.memberName] = self.newValue
            except:
                print("[{}]: Could not set attribute: targetObject: {}, memberName: {}, newValue: {}".format(self.actionName, self.targetObject, self.memberName, self.newValue), file=sys.stderr)

    def __repr__(self):
        return "[ActionSetMember] Code: 0x%x, Length: %d, NewValue: %s, MemberName: %s, ObjName: %s" % (self._code, self._length, self.newValue, self.memberName, self.targetObject)

class ActionIncrement(Action5):
    CODE = 0x50
    def __init__(self, code, length):
        self.oldValue = 0
        self.newValue = None
        super(ActionIncrement, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        oldValueStr = action_stack.pop()

        try: self.oldValue = int(oldValueStr)
        except:
            print("[{}]: could not convert oldValueStr to integer: {}".format(self.actionName, oldValueStr), file=sys.stderr)

        self.newValue = self.oldValue + 1
        action_stack.append(self.newValue)

    def __repr__(self):
        return "[ActionIncrement] Code: 0x%x, Length: %d, OldValue: %d, NewValue: %d" % (self._code, self._length, self.oldValue, self.newValue)

class ActionDecrement(Action5):
    CODE = 0x51
    def __init__(self, code, length):
        self.oldValue = 0
        self.newValue = None
        super(ActionDecrement, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        oldValueStr = action_stack.pop()

        try: self.oldValue = int(oldValueStr)
        except:
            print("[{}]: could not convert oldValueStr to integer: {}".format(self.actionName, oldValueStr), file=sys.stderr)


        self.newValue = self.oldValue - 1
        action_stack.append(self.newValue)

    def __repr__(self):
        return "[ActionDecrement] Code: 0x%x, Length: %d, OldValue: %d, NewValue: %d" % (self._code, self._length, self.oldValue, self.newValue)

class ActionCallMethod(Action):
    CODE = 0x52
    def __init__(self, code, length):
        self.methodName = None
        self.targetObject = None
        self.numArgs = 0
        self.args = []
        super(ActionCallMethod, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.methodName = action_stack.pop()
        self.targetObject = action_stack.pop()
        numArgsStr = action_stack.pop()

        try: self.numArgs = int(numArgsStr)
        except:
            print("[{}]: Could not convert numArgs '{}' to integer: method {} in targetObject {}".format(self.actionName, numArgsStr, self.methodName, self.targetObject), file=sys.stderr)

        if self.numArgs > 0:
            for i in range(self.numArgs):
                print("[{}]: i {}".format(self.actionName, i), file=sys.stderr)
                self.args.append(action_stack.pop())

        methodResult = {'name':'methodResult', 'action':self.actionName, 'targetObject':self.targetObject, 'methodName': self.methodName, 'args': self.args, 'emulatedValue': 0 }
        action_stack.append(methodResult)

    def __repr__(self):
        return "[ActionCallMethod] Code: 0x%x, Length: %d, MethodName: %s, TargetObject: %s, NumArgs: %d" % (self._code, self._length, self.methodName, self.targetObject, self.numArgs)

class ActionNewMethod(Action):
    CODE = 0x53
    def __init__(self, code, length):
        self.methodName = None
        self.targetObject = None
        self.numArgs = 0
        self.args = []
        super(ActionNewMethod, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        self.methodName = action_stack.pop()
        self.targetObject = action_stack.pop()
        numArgsStr = action_stack.pop()

        try: self.numArgs = int(numArgsStr)
        except:
            print("[{}]: could not convert numArgs to integer: method {} in targetObject {}: {}".format(self.actionName, self.methodName, self.targetObject, numArgsStr), file=sys.stderr)

        if self.numArgs > 0:
            for i in range(self.numArgs):
                self.args.append(action_stack.pop())

        methodResult = {'name':'methodResult', 'action':self.actionName, 'targetObject':self.targetObject, 'methodName': self.methodName, 'args': self.args, 'emulatedValue': 0 }
        action_stack.append(methodResult)

    def __repr__(self):
        return "[ActionNewMethod] Code: 0x%x, Length: %d, MethodName: %s, TargetObject: %s, NumArgs: %d" % (self._code, self._length, self.methodName, self.targetObject, self.numArgs)

class ActionBitAnd(Action5):
    CODE = 0x60
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionBitAnd, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()
        try: self.valueA = int(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to integer".format(self.actionName, valueAStr), file=sys.stderr)
            raise
        try: self.valueB = int(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to integer".format(self.actionName, valueBStr), file=sys.stderr)
            raise

        self.result = self.valueA & self.valueB
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionBitAnd] Code: 0x%x, Length: %d, ValueA: %d, ValueB: %d, ResultValue: %s" % (self._code, self._length, self.valueA, self.valueB, self.result)

class ActionBitOr(Action):
    CODE = 0x61
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionBitOr, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()
        try: self.valueA = int(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to integer".format(self.actionName, valueAStr), file=sys.stderr)
            #raise
        try: self.valueB = int(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to integer".format(self.actionName, valueBStr), file=sys.stderr)
            #raise

        self.result = self.valueA | self.valueB
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionBitOr] Code: 0x%x, Length: %d, ValueA: %d, ValueB: %d, ResultValue: %s" % (self._code, self._length, self.valueA, self.valueB, self.result)

class ActionBitXor(Action5):
    CODE = 0x62
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionBitXor, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()
        try: self.valueA = int(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to integer".format(self.actionName, valueAStr), file=sys.stderr)
            #raise
        try: self.valueB = int(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to integer".format(self.actionName, valueBStr), file=sys.stderr)
            #raise
        
        self.result = self.valueA ^ self.valueB
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionBitXOr] Code: 0x%x, Length: %d, ValueA: %d, ValueB: %d, ResultValue: %s" % (self._code, self._length, self.valueA, self.valueB, self.result)

class ActionBitLShift(Action5):
    CODE = 0x63

    def __init__(self, code, length):
        self.shiftCount = 0
        self.value = 0
        super(ActionBitLShift, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        shiftCountStr = action_stack.pop()
        try:
            self.shiftCount = int(shiftCountStr)
            valueStr = action_stack.pop()
    
            try: self.value = int(valueStr)
            except:
                print("[{}]: error converting value '{}' to integer".format(self.actionName, self.value), file=sys.stderr)
    
            self.value = (self.value << self.shiftCount)
        except: 
            print("[{}]: Error converting srhiftCount '{}' to integer. Returning 0".format(self.actionName, self.shiftCount), file=sys.stderr)
            self.value = 0

        action_stack.append(self.value)

    def __repr__(self):
        return "[ActionBitLShift] Code: 0x%x, Length: %d, ShiftCount: %d, Value: %s" % (self._code, self._length, self.shiftCount, self.value)

class ActionBitRShift(Action5):
    CODE = 0x64

    def __init__(self, code, length):
        self.shiftCount = 0
        self.value = None
        super(ActionBitRShift, self).__init__(code, length)

    def parse(self, data):
        global action_stack

        shiftCountStr = action_stack.pop()
        try:
            self.shiftCount = int(shiftCountStr)
            self.value = action_stack.pop()
    
            try: self.value = int(self.value)
            except:
                print("[{}]: Error converting value '{}' to integer".format(self.actionName, self.value), file=sys.stderr)
    
            #s32 = (value + 2**31) % 2**32 - 2**31  # // convert to signed 32-bit
            self.value = (self.value >> self.shiftCount)
    
        except: 
            print("[{}]: Error converting srhiftCount '{}' to integer. Returning 0".format(self.actionName, self.shiftCount), file=sys.stderr)
            self.value = 0

        action_stack.append(self.value)

    def __repr__(self):
        return "[ActionBitRShift] Code: 0x%x, Length: %d, ShiftCount: %d, Value: %s" % (self._code, self._length, self.shiftCount, self.value)

# TODO unsigned 
class ActionBitURShift(ActionBitRShift):
    CODE = 0x65

# TODO: implement type checking
class ActionStrictEquals(ActionEquals2):
    CODE = 0x66
    def __repr__(self):
        return "[ActionStrictEquals] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionStoreRegister(Action5):
    CODE = 0x87
    def __init__(self, code, length):
        self.register = None
        self.value = None
        super(ActionStoreRegister, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        global action_registers
        self.register = data.readUI8()
        self.value = action_stack[-1]
        action_registers[self.register] = self.value

    def __repr__(self):
        return "[ActionStoreRegister] Code: 0x%x, Length: %d, Register: '%s', Value: '%s'" % (self._code, self._length, self.register, self.value)

# =========================================================
# SWF 6 actions
# =========================================================

class ActionEnumerate2(Action6):
    CODE = 0x55
    def __init__(self, code, length):
        self.targetObject = 0
        super(ActionEnumerate2, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.targetObject = action_stack.pop()
        action_stack.append(None)

        # TODO: how to enumerate this?
        #if hasattr(self.targetObject, 'keys'):
        #    for key in self.targetObject.keys():
        #        action_stack.append(key)

    def __repr__(self):
        return "[ActionEnumerate2] Code: 0x%x, Length: %d, TargetObject: %s" % (self._code, self._length, self.targetObject)

class ActionGreater(Action6):
    CODE = 0x67
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionGreater, self).__init__(code, length)

    def parse(self, data):

        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        if valueAStr == None:
          valueAStr = '0'
        if valueBStr == None:
          valueBStr = '0'

        try: self.valueA = int(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to integer".format(self.actionName, valueAStr), file=sys.stderr)
        
        try: self.valueB = int(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to integer".format(self.actionName, valueBStr), file=sys.stderr)
        
        self.result = self.valueB > self.valueA
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionGreater] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionInstanceOf(Action6):
    CODE = 0x54
    def __init__(self, code, length):
        self.constraint = None
        self.targetObject = None
        super(ActionInstanceOf, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.constaint = action_stack.pop()
        self.targetObject = action_stack.pop()
        # TODO
        action_stack.append(False)

    def __repr__(self):
        return "[ActionInstanceOf] Code: 0x%x, Length: %d, Constraint: %s, TargetObject: %s" % (self._code, self._length, self.constraint, self.targetObject)

class ActionStringGreater(Action6):
    CODE = 0x68
    def __init__(self, code, length):
        self.valueA = 0
        self.valueB = 0
        self.result = None
        super(ActionStringGreater, self).__init__(code, length)

    def parse(self, data):

        global action_stack

        valueAStr = action_stack.pop()
        valueBStr = action_stack.pop()

        if valueAStr == None:
          valueAStr = '0'
        if valueBStr == None:
          valueBStr = '0'

        try: self.valueA = int(valueAStr)
        except:
            print("[{}]: error converting value A '{}' to integer".format(self.actionName, valueAStr), file=sys.stderr)
        
        try: self.valueB = int(valueBStr)
        except:
            print("[{}]: error converting value B '{}' to integer".format(self.actionName, valueBStr), file=sys.stderr)
        
        # TODO string byte by byte comparison
        self.result = 1
        action_stack.append(self.result)

    def __repr__(self):
        return "[ActionStringGreater] Code: 0x%x, Length: %d" % (self._code, self._length)


# =========================================================
# SWF 7 actions
# =========================================================

class ActionCastOp(Action7):
    CODE = 0x2b
    def __init__(self, code, length):
        self.targetObject = None
        super(ActionCastOp, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.targetObject = action_stack.pop()
        constructor = action_stack.pop()
        # TODO
        action_stack.append(None)

    def __repr__(self):
        return "[ActionCastOp] Code: 0x%x, Length: %d, TargetObject: %s" % (self._code, self._length, self.targetObject)

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
        self.registerAllocation = []
        self.codeSize = 0
        self.functionBody = []
        super(ActionDefineFunction2, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        global action_variable_context

        self.functionName = data.readString()
        self.numParams = data.readUI16()
        self.registerCount = data.readUI8()
        self.preloadParentFlag = data.readBoolean()
        self.preloadRootFlag = data.readBoolean()
        self.suppressSuperFlag = not data.readBoolean()
        self.preloadSuperFlag = data.readBoolean()
        self.suppressArgumentsFlag = not data.readBoolean()
        self.preloadArgumentsFlag = data.readBoolean()
        self.suppressThisFlag = not data.readBoolean()
        self.preloadThisFlag = data.readBoolean()
        self.reserved = data.readUB(7)
        self.preloadGlobalFlag = data.readBoolean()
        
        if self.functionName == '':
          self.functionName = None
          
        for i in range(self.numParams):
            registerParam = data.readREGISTERPARAM(self.version)
            self.parameters.append(registerParam)
            #if not (registerParam.register is None):
            #    self.registerAllocation.append({
            #      'type': 'param',
            #      'name': registerParam.paramName,
            #      'index': i,
            #      })

        # TODO: finish, impl. look at:
        # https://github.com/mozilla/shumway/blob/master/src/avm1/interpreter.js

        self.codeSize = data.readUI16()

        global parse_inner_action_records
        if parse_inner_action_records:
            bodyEndPosition = data.tell() + self.codeSize
            print("START PARSE 2 (codeSize: {}, range: {} -> {})".format(self.codeSize, data.tell(), bodyEndPosition), file=sys.stderr)
            while data.tell() < bodyEndPosition:
                ret = data.readACTIONRECORD()
                self.functionBody.append(ret)
                print("PARSE 2: (position after read: {} of {})".format(data.tell(), bodyEndPosition), file=sys.stderr)
    
            if data.tell() !=  bodyEndPosition:
                print("PARSE 2: (repositioning after final read: {} -> {})".format(data.tell(), bodyEndPosition), file=sys.stderr)
                data.seek(bodyEndPosition)
    
            print("END PARSE 2", file=sys.stderr)
        else:
            data.skip_bytes(self.codeSize)
    
        functionStub = { 'functionName': self.functionName, 'action': self.actionName, 'parameters': self.parameters, 'registerAllocation': self.registerAllocation }
        if (self.functionName is None):
            #pass
            action_stack.append(functionStub)
        else: 
            action_variable_context[self.functionName] = functionStub

        #data.seek(bodyEndPosition)

    def __repr__(self):
        return "[ActionDefineFunction2] Code: 0x%x, Length: %d, FunctionName: %s, NumParams: %d, Params: %s" % (self._code, self._length, self.functionName, self.numParams, self.parameters)

class ActionExtends(Action7):
    CODE = 0x69
    def __init__(self, code, length):
        self.superClass = None
        self.subClass = None
        super(ActionExtends, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.superClass = action_stack.pop()
        self.subClass = action_stack.pop()

    def __repr__(self):
        return "[ActionExtends] Code: 0x%x, Length: %d, SuperClass: '%s', SubClass: '%s'" % (self._code, self._length, self.superClass, self.subClass)

class ActionImplementsOp(Action7):
    CODE = 0x2c
    def __init__(self, code, length):
        self.constructor = None
        self.implInterfaceCount = 0
        self.interfaces = []
        super(ActionImplementsOp, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.constructor = action_stack.pop()
        implInterfaceCountStr = action_stack.pop()

        try: self.implInterfaceCount = int(implInterfaceCountStr)
        except:
            print("[{}]: unable to convert implInterfaceCount to a int: {}".format(self.actionName, implInterfaceCountStr), file=sys.stderr)

        if not (self.implInterfaceCount is None) and self.implInterfaceCount > 0:
            for i in range(self.implInterfaceCount):
                self.interfaces.append(action_stack.pop())

    def __repr__(self):
        return "[ActionImplementsOp] Code: 0x%x, Length: %d, TargetObject: %s" % (self._code, self._length, self.constructor)


class ActionThrow(Action7):
    CODE = 0x2a
    def __init__(self, code, length):
        self.throwValue = None
        super(ActionThrow, self).__init__(code, length)

    def parse(self, data):
        global action_stack
        self.throwValue = action_stack.pop()

    def __repr__(self):
        return "[ActionThrow] Code: 0x%x, Length: %d, ThrowValue: %s" % (self._code, self._length, self.throwValue)



# urgh! some 100 to go...

ActionTable = {}
for name, value in dict(locals()).iteritems():
    if type(value) == type and issubclass(value, Action) and hasattr(value, 'CODE'):
        ActionTable[value.CODE] = value

class SWFActionFactory(object):
    @classmethod
    def create(cls, code, length):
        return ActionTable.get(code, ActionUnknown)(code, length)

