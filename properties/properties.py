import os


class PropertiesException(Exception):
    pass

class Properties():

    _input_separators = ['=', ':']
    _comment_starter = ['#', '!']
    _unescape_vals = {'escaped' : ["\\=", "\\:", "\\ ", "\\\\"], 'bare' : ["=", ":", " ", "\\"]}

    class PropertyLine():

        _output_separator = ' = '
        # since we only output with a real separator ('='), we don't have to unescape spaces
        _escape_vals = {'escaped' : ["\\\\", "\\=", "\\:"], 'bare' : ["\\", "=", ":"]}

        class LineType():
            UNKNOWN = 0
            COMMENT = 1
            PROPERTY = 2

        class Property():
            def __init__(self, key, value):
                self._key = key
                self._value = value

        def __init__(self, line_type, line_value):
            if line_type is self.LineType.COMMENT and isinstance(line_value, str):
                self._line_value = line_value
            elif line_type is self.LineType.PROPERTY and isinstance(line_value, tuple):
                self._line_value = self.Property(line_value[0], line_value[1])
            else:
                self._line_type = self.LineType.UNKNOWN
                raise PropertiesException("Invalid line type: %s" % (line_value))
            self._line_type = line_type

        def setValue(self, value):
            if self._line_type is self.LineType.COMMENT:
                self._line_value._value = value
            elif self._line_type is self.LineType.PROPERTY:
                self._line_value._value = value

        def getValue(self):
            if self._line_type is self.LineType.COMMENT:
                return self._line_value._value
            elif self._line_type is self.LineType.PROPERTY:
                return self._line_value._value

        def getPrintableLine(self):
            if self._line_type is self.LineType.COMMENT:
                return self._line_value
            elif self._line_type is self.LineType.PROPERTY:
                return "%s%s%s" % (self._escapeString(self._line_value._key), self._output_separator,
                        self._escapeString(self._line_value._value))

        def _escapeString(self, string):
            for i in range(len(self._escape_vals['bare'])):
                string = string.replace(self._escape_vals['bare'][i], self._escape_vals['escaped'][i])
            return string


    def __init__(self):
        self._reset()

    def _reset(self):
        self._lines = []      # ordered set of properties lines (either comments or properties) for output
        self._properties = {} # a dict of pointers to PropertyLine objects for fast lookup

    def setProperty(self, key, value):
        if type(key) is not str or type(value) is not str:
            raise PropertiesException("Property key and value must be a string [key : value] = [%s : %s]" % (type(key), type(value)))

        if self._properties.has_key(key):
            self._properties[key].setValue(value)
        else:
            new_line = self.PropertyLine(self.PropertyLine.LineType.PROPERTY, (key, value))
            self._lines.append(new_line)
            self._properties[key] = new_line

    def getProperty(self, key):
        if self._properties.has_key(key):
            return self._properties[key].getValue()

    def __getitem__(self, key):
        return self.getProperty(key)

    def __setitem__(self, key, value):
        self.setProperty(key, value)

    def keys(self):
        return self._properties.keys()

    def deleteProperty(self, key):
        if self._properties.has_key(key):
            for i in range(len(self._lines)):
                if self._lines[i]._line_type is self.PropertyLine.LineType.PROPERTY and self._lines[i] is self._properties[key]:
                    del self._lines[i]
                    del self._properties[key]
                    break

    def deletePropertiesByKeyPrefix(self, prefix):
        # since we're going to be deleting lines, we need to go backwards
        # through the array so we don't go out of bounds
        for i in range(len(self._lines)-1, -1, -1):
            if self._lines[i]._line_type is self.PropertyLine.LineType.PROPERTY:
                current_key = self._lines[i]._line_value._key
                if current_key.startswith(prefix):
                    del self._lines[i]
                    # also, since the file might be malformed and contain two identical keys (values may or may
                    #  not be the same), this properties key may already be gone. Make sure it's still there
                    if self._properties.has_key(current_key):
                        del self._properties[current_key]

    def writeToStream(self, out):
        if out.mode[0] != 'w':
            raise PropertiesException("Out stream [%s] is not writable" % (out))
        for line in self._lines:
            out.write("%s\n" % (line.getPrintableLine()))

    def write(self, file_name):
        f = open(file_name, 'w')
        self.writeToStream(f)

    def read(self, file_name):
        self._reset()

        f = open(file_name, 'r')
        lines = f.readlines()
        f.close()

        for i in range(len(lines)):
            current_line = lines[i].rstrip("\n")  # TODO  support multiline properties

            stripped_line = current_line.strip()
            if len(stripped_line) == 0 or stripped_line[0] in self._comment_starter:
                new_line = self.PropertyLine(self.PropertyLine.LineType.COMMENT, current_line)
                self._lines.append(new_line)
            else:
                (key, value) = self._keyValFromLine(stripped_line)

                if len(key) == 0:
                    raise PropertiesException("Zero-length property on line: [%s]. (raw = [%s])" % (stripped_line, current_line))

                new_line = self.PropertyLine(self.PropertyLine.LineType.PROPERTY, (key, value))
                self._lines.append(new_line)
                self._properties[key] = new_line

    def _keyValFromLine(self, line):
        sep_found = False
        for i in range(len(line)):
            if line[i] in self._input_separators and (i == 0 or line[i-1] != '\\'):
                sep_found = True
                key = line[0:i].strip()
                value = line[i+1:len(line)].strip()
                break
        if not sep_found:
            space_pos = len(line)
            for i in range(len(line)):
                if line[i] == ' ' and (i == 0 or line[i-1] != '\\'):
                    space_pos = i
                    break
            key = line[0:space_pos].strip()
            value = line[space_pos+1:len(line)].strip()

        key = self._unescapeString(key)
        value = self._unescapeString(value)

        return (key, value)

    def _unescapeString(self, string):
        for i in range(len(self._unescape_vals['bare'])):
            string = string.replace(self._unescape_vals['escaped'][i], self._unescape_vals['bare'][i])
        return string



