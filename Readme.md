# Requirement 
On your local machine have python 3 install 

### Create your vitual env
open your terminal or command prompt.
Navigate to the directory where you want to create the virtual environment.
Run the following command to create a virtual environment named myenv:
```bash
Copy code
python3 -m venv myenv
```
Replace myenv with the name you want to give to your virtual environment.
Once the command completes, you'll have a new directory named myenv (or whatever name you chose) in your current directory. This directory contains the virtual environment.
To activate the virtual environment, use the appropriate command based on your operating system:
On Windows:
```bash 
Copy code
myenv\Scripts\activate
```
On macOS and Linux:
```bash
Copy code
source myenv/bin/activate
```
To deactivate the virtual environment and return to the global Python environment, simply type:
 ```bash
Copy code
 deactivate
```

#### To Install 
Run the command on your shell or terminal 
```bash 
Copy code
pip3 install -r requirement.txt
```

### Add install packages to requirement.txt
```bash
pip3 freeze > requirement.txt
```
