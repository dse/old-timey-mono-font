import json

class NoIndent:
    """A wrapper class to signal that an object should not be indented."""
    def __init__(self, value):
        self.value = value

class NoIndentEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._unique_id = "___NO_INDENT_PLACEHOLDER___"
        self._items = {}

    def default(self, obj):
        # Catch the special wrapper
        if isinstance(obj, NoIndent):
            key = f"{self._unique_id}{len(self._items)}"
            # Serialize the wrapped value immediately with NO indentation
            self._items[key] = json.dumps(obj.value, separators=(',', ':'))
            return key
        return super().default(obj)

    def encode(self, obj, *args, **kwargs):
        raw_json = super().encode(obj, *args, **kwargs)
        pattern = r'"___NO_INDENT_PLACEHOLDER___\d+"'
        def replace_match(match):
            key = match.group(0).strip('"')
            return placeholder_map.get(key, match.group(0))
        for key, val in self._items.items():
            raw_json = raw_json.replace(f'"{key}"', val)
        return raw_json
