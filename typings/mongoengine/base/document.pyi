"""
This type stub file was generated by pyright.
"""

__all__ = ("BaseDocument", "NON_FIELD_ERRORS")
NON_FIELD_ERRORS = ...
GEOHAYSTACK = ...
class BaseDocument:
    __slots__ = ...
    _dynamic = ...
    _dynamic_lock = ...
    STRICT = ...
    def __init__(self, *args, **values) -> None:
        """
        Initialise a document or an embedded document.

        :param values: A dictionary of keys and values for the document.
            It may contain additional reserved keywords, e.g. "__auto_convert".
        :param __auto_convert: If True, supplied values will be converted
            to Python-type values via each field's `to_python` method.
        :param _created: Indicates whether this is a brand new document
            or whether it's already been persisted before. Defaults to true.
        """
        ...
    
    def __delattr__(self, *args, **kwargs): # -> None:
        """Handle deletions of fields"""
        ...
    
    def __setattr__(self, name, value): # -> None:
        ...
    
    def __getstate__(self): # -> dict[Any, Any]:
        ...
    
    def __setstate__(self, data): # -> None:
        ...
    
    def __iter__(self):
        ...
    
    def __getitem__(self, name): # -> Any:
        """Dictionary-style field access, return a field's value if present."""
        ...
    
    def __setitem__(self, name, value): # -> None:
        """Dictionary-style field access, set a field's value."""
        ...
    
    def __contains__(self, name): # -> bool:
        ...
    
    def __len__(self): # -> int:
        ...
    
    def __repr__(self): # -> Any | str:
        ...
    
    def __str__(self) -> str:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def __ne__(self, other) -> bool:
        ...
    
    def clean(self): # -> None:
        """
        Hook for doing document level data cleaning (usually validation or assignment)
        before validation is run.

        Any ValidationError raised by this method will not be associated with
        a particular field; it will have a special-case association with the
        field defined by NON_FIELD_ERRORS.
        """
        ...
    
    def get_text_score(self):
        """
        Get text score from text query
        """
        ...
    
    def to_mongo(self, use_db_field=..., fields=...): # -> SON[Any, Any]:
        """
        Return as SON data ready for use with MongoDB.
        """
        ...
    
    def validate(self, clean=...): # -> None:
        """Ensure that all fields' values are valid and that required fields
        are present.

        Raises :class:`ValidationError` if any of the fields' values are found
        to be invalid.
        """
        ...
    
    def to_json(self, *args, **kwargs): # -> str:
        """Convert this document to JSON.

        :param use_db_field: Serialize field names as they appear in
            MongoDB (as opposed to attribute names on this document).
            Defaults to True.
        """
        ...
    
    @classmethod
    def from_json(cls, json_data, created=..., **kwargs): # -> Self:
        """Converts json data to a Document instance.

        :param str json_data: The json data to load into the Document.
        :param bool created: Boolean defining whether to consider the newly
            instantiated document as brand new or as persisted already:
            * If True, consider the document as brand new, no matter what data
              it's loaded with (i.e., even if an ID is loaded).
            * If False and an ID is NOT provided, consider the document as
              brand new.
            * If False and an ID is provided, assume that the object has
              already been persisted (this has an impact on the subsequent
              call to .save()).
            * Defaults to ``False``.
        """
        ...
    


