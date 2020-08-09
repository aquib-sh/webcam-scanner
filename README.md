Author: Shaikh Aquib
# webcam-scanner
A script which automatically extracts the IP address, port number and location of all the webcams around the world, 
which are connected to the Internet and have default or no credentials required to access them.

This script used Shodan to get the relevant information in order to further perform automation
therefore you must provide your shodan api key in the argument while running the script <br/>
**exampe: python camscanner.py enter_your_api_key_here**

This script will then search through all the webcams and find if there are any default credentials that work on them
or if they are without any authentication.

Finally it saves all this data into a text file named webcamxp5.txt which will be created in the same directory where the script is located.
For now it scans for webcamxp only.
