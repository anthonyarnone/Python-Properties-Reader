import sys

from properties import Properties




if __name__ == '__main__':

    print "Creating Properties Reader"
    reader = Properties()
    reader.read('test.properties')

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
    print "prop 'google' : %s" % (reader['google'])

    print "Done"

