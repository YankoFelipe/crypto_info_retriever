def transform_or_none(transformation_fn, obj):
    return transformation_fn(obj) if bool(obj) else None
