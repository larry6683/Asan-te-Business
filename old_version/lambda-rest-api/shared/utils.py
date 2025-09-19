# I ordinally don't like utils files but i'm not sure where to group some of this stuff

# DO NOT use anything more complicated than a class, dict, or list!!
# To get fancy, implement a to_dict method on the class
class Utils:
    @staticmethod
    def obj_to_dict(obj) -> dict:
        if isinstance(obj, dict):   
            for prop in obj: 
                obj[prop] = Utils.obj_to_dict(obj[prop])
        elif hasattr(obj, 'to_dict') and callable(obj.to_dict):
            return obj.to_dict()
        elif hasattr(obj, '__dict__'): 
            return Utils.obj_to_dict(vars(obj))
        elif isinstance(obj, list):
            return [Utils.obj_to_dict(entry) for entry in obj]
        elif isinstance(obj, (str, int, bool, type(None))):  # Handle primitive types
            return obj
        else:
            raise Exception('obj cannot be converted to dictionary!')

        return obj