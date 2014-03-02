'''
Created on 02/03/2014

@author: thomas
'''
import Event

class A(object):
    def listener(self,testvar):
        print('class A method listener called with argument {}'.format(testvar))
        
    def __del__(self):
        print('object {} is being deleted'.format(self))
        
        


if __name__ == '__main__':
    print('testing Event class')
    
    e=Event.Event(1,'Test event','Just a test event')
    a=A()
    print('adding a.listener')
    e.add(a.listener)
    
    print('envoking signalling')
    e.signal('Event message')
    
    a2=A()
    
    print('adding a2.listener')
    e.add(a2.listener)
    
    print('envoking signalling')
    e.signal('Event message')
    
    print('deleting a')
    del a
    
    print('envoking signalling')
    e.signal('Event message')
    
    
    