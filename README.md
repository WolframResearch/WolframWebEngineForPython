# Wolfram Engine for Python

Wolfram Engine for Python allows you to use a Wolfram Kernel during a web request.

## Standalone version

Make sure the library is in your PATH then run

```
>>> python3 -m wolframengine simpleserver 'Now'
======== Running on http://0.0.0.0:18000 ========
(Press CTRL+C to quit)
```

That should be it!

### Options

optional arguments:
  -h, --help           show this help message and exit
  --get GET            Insert the string to Get.
  --port PORT          Insert the port.
  --kernel KERNEL      Insert the kernel path.
  --poolsize POOLSIZE  Insert the kernel pool size.
  --autoreload         Insert the server should autoreload the WL input
                       expression.
  --preload            Insert the server should should start the kernels
                       immediately.
  --folder FOLDER      Adding a folder root to serve wolfram language content

#### --get
Used --get to specify a path to a .m file which contains the code to run.

Write a file on your current folder:

```
>>> echo 'ExportForm[{"hello", "from", "Kernel", UnixTime[]}, "JSON"]' >> code.m
```

then from CLI Run

```
>>> python3 -m wolframengine simpleserver --get 'code.m'
======== Running on http://0.0.0.0:18000 ========
(Press CTRL+C to quit)
```

#### --autoreload

If --autoreload is present then every request will run the source code again.

```
>>> python3 -m wolframengine simpleserver --get 'code.m' --autoreload
======== Running on http://0.0.0.0:18000 ========
(Press CTRL+C to quit)
```

Visit the browser and refresh the page.

Only works with --get and --folder.

#### --folder

Starts a server that is first checking if code is present on a local folder.


```
>>> python3 -m wolframengine simpleserver --folder 'path/to/folder' --autoreload
======== Running on http://0.0.0.0:18000 ========
(Press CTRL+C to quit)
```

to document

#### --port PORT

Allows you to specify the PORT of the webserver. Defaults to 18000.

```
>>> python3 -m wolframengine simpleserver --port 8080
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)
```

#### --kernel KERNEL

Allows you to specify the Kernel path

```
>>> python3 -m wolframengine simpleserver --kernel '/Applications/Mathematica.app/Contents/MacOS/WolframKernel'
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)
```

#### --poolsize SIZE

Allows you to change the default pool size for kernels. Defaults to 1.

```
>>> python3 -m wolframengine simpleserver --poolsize 4
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)
```


#### --preload 

Whatever the server should immediatly spawn kernels instead of waiting for the first request

## Embedded Version

Wolfram Engine for Python provides bindings for popular frameworks and allows you to write a new one easily.

### Bindings for AIOHTTP

A simple example of how to integrate a Wolfram Kernel in your application can be found here:

[aiohttp_application.py](https://stash.wolfram.com/projects/LCL/repos/wolframengineforpython/browse/wolframengine/docs/examples/python/aiohttp_application.py)

You can run the app by doing:

```
>>> python3 path/to/wolframengineforpython/wolframengine/docs/examples/python/aiohttp_application.py
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)
```