import sys

from properties import Properties




if __name__ == '__main__':

    print "Creating Properties Reader"
    reader = Properties()

    reader['foo'] = 'bar'
    print "----"
    reader.write(sys.stdout)

    reader['foo'] = 'helga'
    reader['bar'] = 'helga'
    reader.setProperty('google', '.com')
    print "----"
    reader.write(sys.stdout)

    reader['google'] = '.org'
    reader.deleteProperty('bar')
    print "----"
    reader.write(sys.stdout)

    print "----"
    print "property 'google' : %s" % (reader['google'])
    print "non-existant prop 'hannibal' : %s" % (reader['hannibal'])




    reader2 = Properties()
    reader2.read('test/sample_1.properties')
    print "Escaped backslash prop: [%s]" % (reader2['windows_path'])
    print "Escaped colon prop: [%s]" % (reader2['escaped_python'])
    print "Escaped equals prop: [%s]" % (reader2['escaped_math'])
    print "Escaped colon key prop: [%s]" % (reader2['C:\\Program Files\\R\\R-2.11.1-x64\\bin\\R.exe'])
    print "Escaped equals key prop: [%s]" % (reader2['3 + 5 = 8'])
 
    print "----"
    reader2.write(sys.stdout)
    print "Done"

