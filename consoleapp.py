import os

class ConsoleApp:
    '''The ConsoleApp class provides basic functionality for user
       interaction using the console 
    '''

    '''constructor
    '''
    def __init__(self):
        pass

    '''prints a title to the console

       @param title the title to be printed
    '''
    def print_title(self, title):
        print '-' * 80
        print '- %s' % title
        print '-' * 80

    '''lets the user select from a number of options

       @param question the question to be asked
       @param choices a list of strings with the options

       @return a tuple containing the selected index and the selected string
    '''
    def read_choice(self, question, choices):
        choice = -1
        while choice < 1 or choice > len(choices):
            print question
            for i in range(1, len(choices)+1):
                print '\t(%d)\t%s' % (i, choices[i-1])

            choice = raw_input('Please enter your choice: ')
            try:
                choice = int(choice)
            except:
                pass

        print
        return ((choice-1), choices[choice-1])

    '''asks the user to enter a path

       @param question the question to be asked
       @param default the default path
       @must_exist true if the returned path must exist (defaults to True)

       @return the entered path
    '''
    def read_path(self, question, default=None, must_exist=True):
        path = '/non/existing/path/'
        default_path = ''
        if default != None:
            default_path = ' (%s)' % default

        while (must_exist == True and not os.path.exists(path)) or (must_exist == False and not os.path.exists(os.path.dirname(path))):
            path = raw_input('%s%s: ' % (question, default_path)).strip()

            if len(path) == 0 and default != None:
                path = default

        print 
        return path

    '''asks the user to enter a number

       @param question the question to be asked
       @param default the default number to be used
       @param minimum the minimum number allowed (defaults to 0)
       @param maximum the maximum number allowed (defaults to None)

       @return the selected number
    '''
    def read_number(self, question, default=None, minimum=0, maximum=None):
        number = None
        default_string = ''
        if default != None:
            default_string=' (%d)' % default
        while number == None or (minimum != None and number < minimum) or (maximum != None and number > maximum):
            string = raw_input('%s%s: ' % (question, default_string)).strip()
            if len(string) == 0 and default != None:
                number = default
            else:
                try:
                    number = int(string)
                except:
                    pass

        print
        return number

    '''asks the user a yes/no question

       @param question the question to be asked

       @return True if the user selected yes, False otherwise
    '''
    def read_yes_no(self, question):
        answer = ''
        while answer != 'y' and answer != 'n' and answer != 'yes' and answer != 'no':
            answer = raw_input('%s (y/n): ' % question).strip()

        print
        return answer[0] == 'y'

    '''creates a 'tmp' directory if it does not yet exist
    '''
    def create_tmp_if_not_exists(self):
        if not os.path.exists('./tmp'):
            os.mkdir('./tmp')