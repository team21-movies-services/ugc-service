from typing import Annotated, Any, Callable

from bson import ObjectId
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


def to_lower_camel(string: str) -> str:
    camel_string = ''.join(word.capitalize() for word in string.split('_'))
    return string[0].lower() + camel_string[1:]


class _ObjectIdPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(id_: str) -> ObjectId:
            return ObjectId(id_)

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ],
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(ObjectId),
                    from_str_schema,
                ],
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance),
                when_used='json',
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `str`
        return handler(core_schema.str_schema())


PyObjectId = Annotated[ObjectId, _ObjectIdPydanticAnnotation]
