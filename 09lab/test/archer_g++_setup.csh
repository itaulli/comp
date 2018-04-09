# Set up a recent version of g++ and a few other programs on archer.ttu.edu
set toplevel = /opt/rh/devtoolset-7/root
setenv LD_LIBRARY_PATH $toplevel/lib64:$toplevel/lib:$LD_LIBRARY_PATH
setenv PATH $toplevel/bin:$PATH
rehash
