'''
Created on 02/03/2014

@author: thomas
'''
import Event

class A(object):
    def listener(self,testvar):
        print('class A method listener called with argument {}'.format(testvar))
        
    def listenerTwoArgs(self,objectref,message):
        print("passed object reference __str__ attribute: {} and the passed message:{}".format(objectref.__str__(),message))
      
        
    def __del__(self):
        print('object {} is being deleted'.format(self))
        
def freeFunc(argMessage):
    print('function freeFunc called with argument {}'.format(argMessage))     


if __name__ == '__main__':
    print('testing Event class')
    
    e=Event.Event(1,'Test event','Just a test event')
    e2=Event.Event(2,"Another Event","Another event taking two methods")
    a=A()
    print('adding a.listener')
    e.add(a.listener)
    
    
    print('envoking signalling')
    e.signal('Event message')
    
    a2=A()
    
    print('adding a2.listener')
    e.add(a2.listener)
    e2.add(a2.listenerTwoArgs)
    
    print('envoking signalling')
    e.signal('Event message')
    
    print('deleting a')
    del a
    
    print('envoking signalling')
    e.signal('Event message')
    
    print('adding a function')
    e.add(freeFunc)
    
    print("invoking e2 event")
    e2.signal(freeFunc,"Passing a function reference as first arg")
    
    print('envoking signalling')
    e.signal('Event message')
    
    print('deleting freeFund')
    del freeFunc
    
    print('envoking signalling')
    e.signal('Event message')
    
    
    
    