## Closures

#Wikipiedia sya , "A closure is a record storing a function together iwth 
# an environemtn: a mapping associating each free variable of the function 
# with the vaue or storage location to which the name was bound when the 
# closure was created.  A closure, unlike a plain funciton, allows the 
# funciton to access those captured vairables though the closure's 
# reference to them, even when the funciton is invoked outside their 
# scope.

def outer_func(msg):
    def inner_func():
        print(msg)

    return inner_func()

outer_func('hello')
x = outer_func('hi')
x


