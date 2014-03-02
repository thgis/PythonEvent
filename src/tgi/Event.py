'''
Created on 02/03/2014

@author: thomas
'''
import weakref
class Event(object):
    '''
    Class that enables an event implementation in python.
    '''
    

    def __init__(self,requiredNoOfArgs=0,eventName='UnknownEvent',eventDescription="UnknownEvent"):
        '''
        Constructor
        '''
        self._listeners=[]
        self.eventName=eventName
        self.eventDescription=eventDescription
        self.reqNoArgs=requiredNoOfArgs
        
    def add(self,callback):
        # TODO handle the situation where methods or functions have default values for arguments
        # and thereby the function arg count need not match the required arg count
        # TODO handle the case where the provided callback is neither a function or a method
        # TODO consider implementing some callback mechanism to be passed when weakref.refs are created
        # to enable self management of the _listeners list
        try:
            # assuming methods
            # callback function argument count should be self.reqNoArgs+1
            if callback.im_func.func_code.co_argcount is not self.reqNoArgs+1:
                raise EventError('The event requires that the listener function takes %d arguments but the provided listener function takes %d arguments'%(self.reqNoArgs+1,callback.im_func.func_code.co_argcount))            
            callback_ref = weakref.ref(callback.__func__), weakref.ref(callback.__self__)
        except AttributeError:
            # assuming function
            if callback.func_code.co_argcount is not self.reqNoArgs:
                    raise EventError('The event requires that the listener function takes %d arguments but the provided listener function takes %d arguments'%(self.reqNoArgs,callback.func_code.co_argcount))            
            callback_ref = weakref.ref(callback), None
        self._listeners.append(callback_ref)
    def remove(self,callback):
        try:
            # assuming methods
            # callback function argument count should be self.reqNoArgs+1
            callback_t = callback.__func__, callback.__self__
        except AttributeError:
            # assuming function
            callback_t = callback, None
        for listener in self._listeners:
            compCallback_t=listener[0](),listener[1]() # here all listeners are assumed to exists!
            if callback_t == compCallback_t:
                self._listeners.remove(listener)
    def signal(self,*args):
        # check that supplied num of args equals self.reqNoArgs
        
        def identifyDeadObjectAndCallOthers(listener):
            callback, arg = listener[0](), listener[1]
            if arg is not None:
                # method
                arg = arg()
                if arg is None:
                    # instance is gone. Do cleanup
                    return False 
                callback(arg, *args)
                
            else:
                if callback is None:
                    # callback has been deleted already
                    return False
                callback(args)
            return True
        
        if self.reqNoArgs is not len(args):
            raise EventError('Supplied number of arguments to signal (%d) was different that required (%d)'%(len(args),self.reqNoArgs))
        self._listeners[:] =[x for x in self._listeners if identifyDeadObjectAndCallOthers(x)]
        
        
class EventError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        
        