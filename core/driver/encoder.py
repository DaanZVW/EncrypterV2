# Libraries
from typing import Dict, Any, Type

# Drivers
from core.driver.basemodel import base

# Global variables
type_registry: Dict[str, Dict[str, Any]] = dict()


def register_encrypter_type(obj_type: Type[base], size: int) -> bool:
    """
    Function that registers an encrypter type for exporting and importing
    :param obj_type: Type of the object
    :param size: Amount of attributes are getting exported and imported (for additional checking)
    :return: If succeeded
    """
    if not issubclass(obj_type, base):
        raise TypeError('Other than base is not supported')

    type_id = obj_type().id.decode('utf-8')
    type_registry[type_id] = {
        'type': obj_type,
        'amount_attrs': size
    }
    return True


def export_model(obj: base):
    if obj is None:
        return None
    elif not issubclass(type(obj), base):
        raise TypeError('given model is not a encrypter model')

    obj_id = obj.id.decode('utf-8')
    try:
        encoder = type_registry[obj_id]['type'].__export__
    except AttributeError:
        raise RuntimeError(f"id '{obj_id}' not found")

    # Here should be a try except clause
    encoded_obj = encoder(obj)

    if not isinstance(encoded_obj, list):
        raise TypeError("encode_fallback didn't return a list")
    return [obj_id] + encoder(obj)


def import_model(attributes: Any):
    if attributes is None:
        return None

    model_id, *attributes = attributes

    try:
        decoder = type_registry[model_id]['type'].__import__
    except KeyError:
        raise TypeError(f"id {model_id} not found")

    # Here should be a try except clause
    decoded_obj = decoder(attributes)

    if not issubclass(type(decoded_obj), base):
        raise TypeError('given model is not a encrypter model')
    return decoded_obj

