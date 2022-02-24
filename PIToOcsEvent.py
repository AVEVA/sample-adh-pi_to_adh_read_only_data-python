import inspect
import json
from datetime import datetime


class PIToOcsEvent:
    """Represents a PI event to be injected into Sds Service"""

    def __init__(self):
        self._Timestamp = datetime.utcnow().isoformat()
        self._value = ''
        self._IsQuestionable = False
        self._IsSubstituted = False
        self._IsAnnotated = False
        self._SystemStateCode = ''
        self._DigitalStateName = ''


    @property
    def Timestamp(self):
        return self._Timestamp

    @Timestamp.setter
    def Timestamp(self, Timestamp):
        self._Timestamp = Timestamp

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def IsQuestionable(self):
        return self._IsQuestionable

    @IsQuestionable.setter
    def IsQuestionable(self, IsQuestionable):
        self._IsQuestionable = IsQuestionable

    @property
    def IsSubstituted(self):
        return self._IsSubstituted

    @IsSubstituted.setter
    def IsSubstituted(self, IsSubstituted):
        self._IsSubstituted = IsSubstituted

    @property
    def IsAnnotated(self):
        return self._IsAnnotated

    @IsAnnotated.setter
    def IsAnnotated(self, IsAnnotated):
        self._IsAnnotated = IsAnnotated

    @property
    def SystemStateCode(self):
        return self._SystemStateCode

    @SystemStateCode.setter
    def SystemStateCode(self, SystemStateCode):
        self._SystemStateCode = SystemStateCode

    @property
    def DigitalStateName(self):
        return self._DigitalStateName

    @DigitalStateName.setter
    def DigitalStateName(self, DigitalStateName):
        self._DigitalStateName = DigitalStateName


    def toDictionary(self):
        """Converts the object into a dictionary"""
        dictionary = {}
        for prop in inspect.getmembers(type(self),
                                       lambda v: isinstance(v, property)):
            if hasattr(self, prop[0]):
                dictionary[prop[0]] = prop[1].fget(self)

        return dictionary


    def toJson(self):
        """Converts the object into JSON"""
        return json.dumps(self.toDictionary())
