from enum import Enum
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper

class EnumUtils:
    @staticmethod
    def get_enum_name(enum: Enum | EnumTypeWrapper, enum_value=None):
        if enum is None: return ""
        try:
            if type(enum) == Enum:
                return enum.name
            elif type(enum) == EnumTypeWrapper:
                return enum.Name(enum_value)
        except Exception as e:
            return ""