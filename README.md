# Pycharm Remote Debugger

With PyCharm you can debug your application using an interpreter that is located on the other computer, 
for example, on a web server or dedicated test machine.

### Steps
1. Create a deployment configuration for a remote interpreter.
   - Ensure that you have SSH access to the remote machine
2. Deploy your application to a remote host
3. Create a Python Debug Server run/debug configuration
    - Specify the port number, and the IDE host address
    - Map the path on the local machine to the path on the remote machine
4. Make sure you are installing pycharm_remote_debugger on the remote machine/container   
5. Create and entry point file that execute your code and login to the debugger.
```python
from pycharm_remote_debugger import PycharmRemoteDebugger

remote_addr = "10.2.55.1"
port = 1324

debugger = PycharmRemoteDebugger(remote_addr, int(port))
debugger.wait_for_debugger()

main()  # run your software here
``` 
6. Start debugger on pycharm
7. Debug your program :) 

Note: Soon there will be a cli tool for executing any python program (development in progress)