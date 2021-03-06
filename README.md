# File Systen Checker (Operating System)
##Language: Python

## Synopsis

Design a file system checker for our file system.  You should call it csefsck.  It will have to do the following, correcting errors whenever possible, and reporting everything it does to the user:<br>
<br>1.)	The DeviceID is correct (20)<br>
2.)	All times are in the past, nothing in the future<br>
3.)	Validate that the free block list is accurate this includes<br>
  - Making sure the free block list contains ALL of the free blocks<br>
  - Make sure than there are no files/directories stored on items listed in the free block list<br>
  
4.)	Each directory contains . and .. and their block numbers are correct<br>
5.)	If indirect is 1, that the data in the block pointed to by location pointer is an array<br>
6.)	That the size is valid for the number of block pointers in the location array. The three possibilities are:<br>
  - size < blocksize  should have indirect=0 and size>0<br>
  - if indirect!=0, size should be less than (blocksize*length of location array)<br>
  - if indirect!=0, size should be greater than (blocksize*length of location array-1)<br>


## Configuration

  Fork this project in your GitHub account, then clone your repository:

  Run the following query on terminal.
  ```
  git clone http://github.com/vaibhavagg12393/File-System-Checker---Python.git
  ```
   Run the following query in the terminal
   ```
   $ python ./csefsck.py
```

## Additional
Same project have been code using Java. Click ['here'] (https://github.com/vaibhavagg12393/File-System-Checker---Java.git) to open Java code.

