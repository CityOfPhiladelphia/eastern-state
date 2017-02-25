from collections import OrderedDict

import yaml
import yaml.constructor

class UnencryptedTag(object):
    yaml_tag = u'!unencrypted'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<UnencryptedTag value={}>'.format(self.value)

    def constructor(loader, node):
        return UnencryptedTag(loader.construct_scalar(node))

class EncryptedTag(object):
    yaml_tag = u'!encrypted'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<EncryptedTag value={}>'.format(self.value)

    def constructor(loader, node):
        return EncryptedTag(loader.construct_scalar(node))

class Loader(yaml.Loader):
    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor(u'tag:yaml.org,2002:map', Loader.construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', Loader.construct_yaml_map)

        # custom tags
        self.add_constructor(UnencryptedTag.yaml_tag, UnencryptedTag.constructor)
        self.add_constructor(EncryptedTag.yaml_tag, EncryptedTag.constructor)

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,
                'expected a mapping node, but found %s' % node.id, node.start_mark)

        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError('while constructing a mapping',
                    node.start_mark, 'found unacceptable key (%s)' % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping

class Dumper(yaml.Dumper):
    def __init__(self, *args, **kwargs):
        yaml.Dumper.__init__(self, *args, **kwargs)

        self.add_representer(OrderedDict, Dumper.represent_ordereddict)

    def represent_ordereddict(self, data):
        value = []

        for item_key, item_value in data.items():
            node_key = self.represent_data(item_key)
            node_value = self.represent_data(item_value)

            value.append((node_key, node_value))

        return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)
