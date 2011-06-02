import os


class PropertiesException(Exception):
    pass

class Properties():

    class PropertyLine():
        class LineType():
            UNKNOWN = 0
            COMMENT = 1
            PROPERTY = 2

        class Property():
            separator = ' = '
            def __init__(self, key, value):
                self._key = key
                self._value = value

        def __init__(self, line_type, line_value, line_pos):
            if line_type is self.LineType.COMMENT and isinstance(line_value, str):
                self._line_value = line_value
            elif line_type is self.LineType.PROPERTY and isinstance(line_value, tuple):
                self._line_value = self.Property(line_value[0], line_value[1])
            else:
                self._line_type = self.LineType.UNKNOWN 
                raise PropertiesException("Invalid line type: %s" % (line_value))
            self._line_type = line_type 
            self._line_pos = line_pos

        def setValue(self, value):
            if self._line_type is self.LineType.COMMENT:
                line_value = value
            elif self._line_type is self.LineType.PROPERTY:
                self._line_value._value = value

        def getValue(self):
            if self._line_type is self.LineType.COMMENT:
                return line_value
            elif self._line_type is self.LineType.PROPERTY:
                return self._line_value._value

        def getLine(self):
            if self._line_type is self.LineType.COMMENT:
                return line_value
            elif self._line_type is self.LineType.PROPERTY:
                return "%s%s%s" % (self._line_value._key, self.Property.separator, self._line_value._value)

    def __init__(self):
        self._reset()

    def _reset(self):
        self._lines = []      # ordered set of properties lines (either comments or properties) for output
        self._properties = {} # a dict of pointers to PropertyLine objects for fast lookup

    def setProperty(self, key, value):
        if self._properties.has_key(key):
            self._properties[key].setValue(value)
        else:
            new_line = self.PropertyLine(self.PropertyLine.LineType.PROPERTY, (key, value), len(self._lines))
            self._lines.append(new_line)
            self._properties[key] = new_line

    def getProperty(self, key):
        if self._properties.has_key(key):
            return self._properties[key].getValue()

    def __getitem__(self, key):
        return self.getProperty(key)

    def __setitem__(self, key, value):
        self.setProperty(key, value)

    def deleteProperty(self, key):
        if self._properties.has_key(key):
            for i in range(len(self._lines)):
                if self._lines[i]._line_type is self.PropertyLine.LineType.PROPERTY and self._lines[i] is self._properties[key]:
                    del self._lines[i]
                    del self._properties[key]
                    break

    def write(self, out):
        if out.mode[0] != 'w':
            raise PropertiesException("Out stream [%s] is not writable" % (out))
        for line in self._lines:
            out.write("%s\n" % (line.getLine()))

    def read(self, file_name):
        self._reset()
        if not os.path.exists(file_name):
            return


