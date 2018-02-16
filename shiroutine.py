# Copyright (C) Eric Mink 2018

# import makeAboveMeme either from subdirectory or from global installation.
# Thus, it would be possible to use the global version if no subdir version is installed.
try:
    from MakeAboveMeme.mAm import makeAboveMeme as mAm
except ImportError:
    import mAm

# A Shiroutine is a function with a state, which can be cleaned from any other function, resetting the Shiroutine to a default state.
class Shiroutine(object):
    # self.state is a dictionary with whatever state the Shiroutine needs
    # self.setNextDefaultRoutine is a function to set the global variable for the next Shiroutine to execute
    # self.counter is the number of times this routine was called in succession (without restarting it by typing the same command again)

    def __init__(self, setNextDefault, initialState={}):
        self.state = initialState
        self.initialState = initialState
        self.setNextDefaultRoutine = setNextDefault
        self._counter = 0

    # reset to a clean state on receival of a new command
    def cleanup(self):
        self.counter = 0
        self.state = self.initialState

    # a function that every Shiroutine needs to provide
    # Called from the next_Default routine setting
    # expects text input
    def run(self, msgtext):
        pass

    # start the shiroutine anew because a new command for it was received.
    # Called from the command-mapping dictionary
    def start(self, msgtext):
        self.cleanup()
        return self.run(msgtext)

    # playing around with the property decorator
    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, value):
        self._counter = value

    # called when an image is sent and this shiroutine is set as default
    def runImg(self, img):
        pass

''' Requirements for the function passed in as setNextDefault:
        must take a function as an argument
        must accept None as a valid input argument => set next routine to default'''


# Make Above Meme
class MamShiroutine(Shiroutine):
    # INHERITED:
    # dict self.state
    # dict self.initialState
    # func self.setNextDefaultRoutine
    # int  self.counter

    userSent = {
                '/mam':0, 'title':1, 'text':2, 'image':3,
            }

    mamList = [
        "Please choose a title",
        "Please enter some text.",
        "Please choose an image",
        "Thanks!",
            ]

    def __init__(self, setNextDefault, initialState={}):
        super(MamShiroutine, self).__init__(setNextDefault, initialState)

    def cleanup(self):
        # super resets the counter
        super(MamShiroutine, self)

    def run(self, msgtext):
        super(MamShiroutine, self).run(msgtext)
        # TODO: store inputs in self.state and reset them in cleanup
        # TODO: actually use them to call makeAboveMeme
        i = self.counter # will later return the string in mamList that is at that position
        args = self.state # python treats these like pointers. it's an alias.

        if  i == MamShiroutine.userSent['/mam'] :     # user sent '/mam'
            pass
        elif i == MamShiroutine.userSent['title'] :     # user sent a title
            args['--title'] = msgtext
        elif i == MamShiroutine.userSent['text'] :     # user sent some text
            args['--text'] = msgtext # TODO: Does it work if the user sends no text?
        elif i == MamShiroutine.userSent['image'] :
            args['--image'] = msgtext
            MamShiroutine.mamList[i] = "Thx! You chose the title {0} and the text {1}. We will load the image from {2}".format(args['--title'], args['--text'], args['--image'])
        else:
            pass # TODO: send the user the resulting image

        self.counter += 1
        # if the next message would be out of bounds, reset the default choice. Otherwise make sure that we are called again.
        if self.counter < len(MamShiroutine.mamList):
            self.setNextDefaultRoutine(self.run) # We want to be called again on the next message
        else:
            self.setNextDefaultRoutine(None)
            self.cleanup() # reset counter and state
        return MamShiroutine.mamList[i]

    def runImg(self, img):
        # if I expeced an image, I take it. otherwise, I ignore it.
        if not self.counter == MamShiroutine.userSent['image']:
            return "mAm was not expecting an image. I'll just ignore that you sent that."
        else:
            self.state['--image'] = img
            self.counter += 1
            # if the next message would be out of bounds, reset the default choice. otherwise make sure that we are called again.
            if self.counter < len(MamShiroutine.mamList):
               self.setNextDefaultRoutine(self.run)
            else:
               self.setNextDefaultRoutine(None)
               self.cleanup()
            return MamShiroutine.mamList[self.counter -1]
            

    def callMam():
        # TODO: temporary output file
        # TODO: actually use this function, pass it some params
        arguments = {
            '--comments': None,
            '--help': False,
            '--image': None,
            '--link': None,
            '--out': './aboveMeme.png',
            '--points': None,
            '--tag': [],
            '--text': None,
            '--title': None,
            '--version': False,
            '-C': None,
            '-X': False
        }
        mAm.main(arguments)


# Testroutine
class TestShiroutine(Shiroutine):
    def run(self, msgtext):
        super(TestShiroutine, self).run(msgtext)
        # DEBUG: setting next routine to be the defaultShiroutine
        defaultSR = DefaultShiroutine(setNextDefault = self.setNextDefaultRoutine)
        self.setNextDefaultRoutine(defaultSR.run)
        return "testroutine works! {0}".format(msgtext)

class DefaultShiroutine(Shiroutine):
    def run(self, msgtext):
        super(DefaultShiroutine, self).run(msgtext)
        return "I didn't study for this 0.o"

    def runImg(self, msg):
        super(DefaultShiroutine, self).runImg(msg)
        return "I didn't expect pics today ;)"

