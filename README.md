# Wolfram Web Engine for Python

Wolfram Web Engine for Python allows you to use a Wolfram Kernel during a web request.

This cli serves files from the current directory and below, directly mapping the directory structure to HTTP requests.

## Getting Started

### Prerequisites

1. Python 3.5 or higher
2. Wolfram Language 11.3 or higher
3. [WolframClientForPython](!https://github.com/WolframResearch/WolframClientForPython)

### Install Using pip (Recommended)
Recommended for most users. It installs the latest stable version released by Wolfram Research.

Evaluate the following command in a terminal:

```
>>> pip3 install wolframengineforpython
```

### Install Using Git

Recommended for developers who want to install the library along with the full source code.
Clone the library’s repository:

```
>>> git clone git://github.com/WolframResearch/WolframWebEngineForPython
```

Install the library in your site-package directory:

```
>>> cd WolframWebEngineForPython
>>> pip3 install .
```

### Start the server

Start the server by doing:

```
python3 -m wolframwebengine --demo
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop/wolframengineforpython/wolframwebengine/examples/demoapp
Index           index.m
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

That should be it!

## Single file applications

Writing an application using a single file.

Create a folder named myapp.
Write the following content on a file by running:

```
>>> echo 'URLDispatcher[{"/api" -> APIFunction["x" -> "String"], "/form" -> FormFunction["x" -> "String"], "/" -> "hello world!"}]' >  index.m
```

From the same location run:

```
>>> python3 -m wolframwebengine index.m
----------------------------------------------------------------------
Address          http://localhost:18000/
File            /Users/rdv/Desktop/index.m
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

Then try to open the following urls in your browser:

```
http://localhost:18000/
http://localhost:18000/form
http://localhost:18000/api
```

For more information about single file applications please read the documentation of [URLDispatcher](https://reference.wolfram.com/language/ref/URLDispatcher.html).

## Multi file applications

WolframWebEngine for python allows you to write an application by creating a folder structure that is served by the server.

The server will serve content with the following rules:

1. All files with extensions '.m', '.mx', '.wxf', '.wl' will be evaluated in the Kernel using [GenerateHTTPResponse](https://reference.wolfram.com/language/ref/GenerateHTTPResponse.html) over the result.
2. Any other file will be served as static content.
3. If the request path corrispond to a folder on disk, the server will search for a file named index.m in the same folder, this convention can be changed with the --index option.

Create an application by running the following code in your current location:

```
mkdir testapp
mkdir testapp/form
mkdir testapp/api
echo 'ExportForm[{"hello", UnixTime[]}, "JSON"]' >  testapp/index.m
echo 'FormFunction["x" -> "String"]'             >  testapp/form/index.m
echo 'APIFunction["x" -> "String"]'              >  testapp/api/index.m
echo '["some", "static", "JSON"]'                >  testapp/static.json
```

Start the app by running:

```
>>> python3 -m wolframwebengine testapp
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop/testapp
Index           index.m
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

Then open the browser at the following locations:
```
http://localhost:18000/
http://localhost:18000/form
http://localhost:18000/api
http://localhost:18000/static.json
```

### Options

```
>>> python3 -m wolframwebengine --help
usage: __main__.py [-h] [--port PORT] [--domain DOMAIN] [--kernel KERNEL]
                   [--poolsize POOLSIZE] [--cached] [--lazy] [--index INDEX]
                   [path]

positional arguments:
  path

optional arguments:
  -h, --help           show this help message and exit
  --port PORT          Insert the port.
  --domain DOMAIN      Insert the domain.
  --kernel KERNEL      Insert the kernel path.
  --poolsize POOLSIZE  Insert the kernel pool size.
  --cached             The server will cache the WL input expression.
  --lazy               The server will start the kernels on the first request.
  --index INDEX        The file name to search for folder index.
```

#### path

The first argument can be a folder or a single file.

Write a file on your current folder:

```
>>> echo 'ExportForm[{"hello", "from", "Kernel", UnixTime[]}, "JSON"]' >  index.m
```

then from CLI Run

```
>>> python3 -m wolframwebengine
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.m
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

If the first argument is a file, all request path will be routed to the same expression.
If the first argument is a folder, requests will be redirected to the kernel if the url extension ends with '.m', '.mx', '.wxf', '.wl'.

If the request path is a folder the server will search for an index.m in the same folder.

#### --index

Specify the default file name for folder index.
Defaults to index.m

```
python3 -m wolframwebengine --index index.wxf
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.wxf
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```


#### --cached

If --cached is present then every request will run the source code once

```
>>> python3 -m wolframwebengine --cached
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.m
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

Visit the browser and refresh the page.


#### --port PORT

Allows you to specify the PORT of the webserver. Defaults to 18000.

```
>>> python3 -m wolframwebengine --port 9090
----------------------------------------------------------------------
Address          http://localhost:9090/
Folder          /Users/rdv/Desktop
Index           index.m
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

#### --kernel KERNEL

Allows you to specify the Kernel path

```
>>> python3 -m wolframwebengine --kernel '/Applications/Mathematica11.3.app/Contents/MacOS/WolframKernel'
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.m
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

#### --poolsize SIZE

Allows you to change the default pool size for kernels. Defaults to 1.

```
>>> python3 -m wolframwebengine --poolsize 4
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.m
----------------------------------------------------------------------
(Press CTRL+C to quit)
```


#### --lazy 

If the option is present the server will wait for the first request to spawn the kernels, instead of spawning them immediately.

## Embedded Version

Wolfram Web Engine for Python provides bindings for popular frameworks and allows you to write a new one easily.

### Bindings for AIOHTTP

A simple example of how to integrate a Wolfram Kernel in your application can be found here:

[aiohttp_application.py](https://stash.wolfram.com/projects/LCL/repos/wolframwebengineforpython/browse/wolframwebengine/docs/examples/python/aiohttp_application.py)

You can run the app by doing:

```
>>> python3 wolframengineforpython/wolframwebengine/examples/aiohttp_application.py 
======== Running on http://localhost:8080 ========
(Press CTRL+C to quit)
```