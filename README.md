# Wolfram Engine for Python

Wolfram Engine for Python allows you to use a Wolfram Kernel during a web request.

## Standalone version

Make sure the library is in your PATH then run.

```
>>> python3 -m wolframengine simpleserver
======== Running on http://0.0.0.0:18000 ========
(Press CTRL+C to quit)
```

That should be it!

### Options

```
>>> python3 -m wolframengine simpleserver --help
usage: wolframengine.cli.commands.simpleserver.Command [-h] [--port PORT]
                                                       [--kernel KERNEL]
                                                       [--poolsize POOLSIZE]
                                                       [--cached] [--lazy]
                                                       [path]

positional arguments:
  path

optional arguments:
  -h, --help           show this help message and exit
  --port PORT          Insert the port.
  --kernel KERNEL      Insert the kernel path.
  --poolsize POOLSIZE  Insert the kernel pool size.
  --cached             The server will cache the WL input expression.
  --lazy               The server will start the kernels on the first request.
  --index              The file name to search for folder index.
```

#### path

The first argument can be a folder or a single file.

Write a file on your current folder:

```
>>> echo 'ExportForm[{"hello", "from", "Kernel", UnixTime[]}, "JSON"]' >> index.m
```

then from CLI Run

```
>>> python3 -m wolframengine simpleserver
======== Running on http://0.0.0.0:18000 ========
(Press CTRL+C to quit)
```

If the first argument is a file, all request path will be routed to the same expression.
If the first argument is a folder, requests will be redirected to the kernel if the url extension ends with '.m', '.mx', '.wxf', '.wl'.

If the request path is a folder the server will search for an index.m in the same folder.

#### --index

Specify the default file name for folder index.
Defaults to index.m

```
>>> python3 -m wolframengine simpleserver --index index.wxf
======== Running on http://0.0.0.0:18000 ========
(Press CTRL+C to quit)
```


#### --cached

If --cached is present then every request will run the source code once

```
>>> python3 -m wolframengine simpleserver 'index.m' --cached
======== Running on http://0.0.0.0:18000 ========
(Press CTRL+C to quit)
```

Visit the browser and refresh the page.


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


#### --lazy 

If the option is present the server will wait for the first request to spawn the kernels, instead of spawning them immediately.

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