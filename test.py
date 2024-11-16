import sys, os

print('sys.argv[0] =', sys.argv[0])             
pathname = os.path.dirname(sys.argv[0])        
print('path =', pathname)
print(os.getcwd())
print(__file__)
print(os.path.dirname(os.path.realpath(__file__)))
print('full path =', os.path.abspath(pathname)) 