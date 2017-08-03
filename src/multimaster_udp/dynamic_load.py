# Idea coming from rosserial_python

import sys
import imp
import roslib

def get_class(msg_class):
    def load_pkg_module(package, directory):
        #check if its in the python path
        path = sys.path
        try:
            imp.find_module(package)
        except:
            roslib.load_manifest(package)
        try:
            m = __import__( package + '.' + directory )
        except:
            rospy.logerr( "Cannot import package : %s"% package )
            rospy.logerr( "sys.path was " + str(path) )
            return None
        return m

    def load_message(package, message):
        m = load_pkg_module(package, 'msg')
        m2 = getattr(m, 'msg')
        return getattr(m2, message)

    try:
        loaded_class = load_message(*msg_class.split('/'))
    except:
        loaded_class = None
    finally:
        return loaded_class