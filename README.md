# Wolfram Web Engine for Python

Wolfram Web Engine for Python uses the Python AIOHTTP web server to handle requests for a Wolfram Engine.
Web pages are specified on the server with standard Wolfram Language functions such as [APIFunction](https://reference.wolfram.com/language/ref/APIFunction.html), [FormFunction](https://reference.wolfram.com/language/ref/FormFunction.html), [FormPage](https://reference.wolfram.com/language/ref/FormPage.html),
[URLDispatcher](https://reference.wolfram.com/language/ref/URLDispatcher.html), [AskFunction](https://reference.wolfram.com/language/ref/AskFunction.html), [HTTPResponse](https://reference.wolfram.com/language/ref/HTTPResponse.html), [HTTPRedirect](https://reference.wolfram.com/language/ref/HTTPRedirect.html), etc. This allows you to integrate Wolfram Language 
functionality seamlessly with existing Python web applications like Django and AIOHTTP.

## Getting Started

### Prerequisites

1. Python 3.5 or higher
2. Wolfram Language 11.3 or higher (Mathematica, Wolfram Desktop, or Wolfram Engine)
3. [WolframClientForPython](!https://github.com/WolframResearch/WolframClientForPython)

### Install Using pip (Recommended)
Recommended for most users. It installs the latest stable version released by Wolfram Research.

Evaluate the following command in a terminal:

```
>>> pip3 install wolframwebengine
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

The following method is not installing the library globally, therefore all the example commands needs to run from the cloned directory.

### Start a demo server

Start a demo server by doing:

```
python3 -m wolframwebengine --demo
----------------------------------------------------------------------
Address         http://localhost:18000/
Folder          /Users/rdv/Desktop/wolframengineforpython/wolframwebengine/examples/demoapp
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

Now you can open your web browser at the address http://localhost:18000/

![image](https://raw.githubusercontent.com/WolframResearch/WolframWebEngineForPython/master/docs/assets/image1.png)

## Two different ways of structuring an application:

1. Use a single file with URLDispatcher
2. Use multiple files in a directory layout

### Single file with URLDispatcher

One way to run your server is to direct all requests to a single file
that runs a Wolfram Language [URLDispatcher](https://reference.wolfram.com/language/ref/URLDispatcher.html) function.

Write the following content in a file called `dispatcher.m`:

```
URLDispatcher[{
    "/api" -> APIFunction["x" -> "String"], 
    "/form" -> FormFunction["x" -> "String"], 
    "/" -> "hello world!"
}]
```

From the same location run:

```
>>> python3 -m wolframwebengine dispatcher.m
----------------------------------------------------------------------
Address         http://localhost:18000/
File            /Users/rdv/Desktop/dispatcher.m
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

All incoming requests will now be routed to the `URLDispatcher` function in `dispatcher.m`.
You can now open the following urls in your browser:

```
http://localhost:18000/
http://localhost:18000/form
http://localhost:18000/api
```

For more information about `URLDispatcher` please refer to the [online documentation](https://reference.wolfram.com/language/ref/URLDispatcher.html).

### Multiple files in a directory layout

Another way to write an application is to create a directory structure that is served by the server. The url for each file will match the file's directory path.

The server will serve content with the following rules:

1. All files with extensions '.m', '.mx', '.wxf', '.wl' will be evaluated in the Kernel using [GenerateHTTPResponse](https://reference.wolfram.com/language/ref/GenerateHTTPResponse.html) on the content of the file.
2. Any other file will be served as static content.
3. If the request path corresponds to a directory on disk, the server will search for a file named index.wl in that directory. This convention can be changed with the --index option.

Create an application by running the following code in your current location:

```
mkdir testapp
mkdir testapp/form
mkdir testapp/api
echo 'ExportForm[{"hello", UnixTime[]}, "JSON"]' >  testapp/index.wl
echo 'FormFunction["x" -> "String"]'             >  testapp/form/index.wl
echo 'APIFunction["x" -> "Number", #x! &]'       >  testapp/api/index.wl
echo 'HTTPResponse["hello world"]'               >  testapp/response.wl
echo '["some", "static", "JSON"]'                >  testapp/static.json
```

Start the application by running:

```
>>> python3 -m wolframwebengine testapp
----------------------------------------------------------------------
Address         http://localhost:18000/
Folder          /Users/rdv/Desktop/testapp
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

Then open the browser at the following locations:

```
http://localhost:18000/
http://localhost:18000/form
http://localhost:18000/api?x=4
http://localhost:18000/response.wl
http://localhost:18000/static.json
```

One advantage of a multi-file application structure is that is very easy to extend the application. You can simply place new files into the appropriate location in your application directory and they will automatically be served.


## Using Docker

Wolfram Web Engine for Python is available as [a container image from Docker Hub](https://hub.docker.com/r/wolframresearch/wolframwebengineforpython) for use in containerized environments.

This image is based on the [official Wolfram Engine Docker image](https://hub.docker.com/r/wolframresearch/wolframengine); information on product activation and license terms
is available on the [Docker Hub page](https://hub.docker.com/r/wolframresearch/wolframengine) for the latter image.

```
# exposes the server on port 8080 of the host machine
>>> docker run -ti -p 8080:18000 wolframresearch/wolframwebengineforpython --demo

# serve files from the /srv directory
>>> docker run -ti -p 8080:18000 wolframresearch/wolframwebengineforpython /srv
```

The commands above do not include activation/licensing configuration; see the [official Wolfram Engine Docker image](https://hub.docker.com/r/wolframresearch/wolframengine) for information on activating the Wolfram Engine kernel.


Note regarding on-demand licensing: As Wolfram Web Engine for Python does not use WolframScript, the `-entitlement` command-line option and the `WOLFRAMSCRIPT_ENTITLEMENTID`
environment variable cannot be used to pass an on-demand license entitlement ID to the Wolfram Engine kernel inside this image.
As a workaround, the `WOLFRAMINIT` environment variable can be set to pass both the entitlement ID and the license server address to the kernel:

```
>>> docker run -ti -p 8080:18000 --env WOLFRAMINIT='-pwfile !cloudlm.wolfram.com -entitlement O-WSTD-DA42-GKX4Z6NR2DSZR' wolframresearch/wolframwebengineforpython --demo
```


## Options

```
>>> python3 -m wolframwebengine --help
usage: __main__.py [-h] [--port PORT] [--domain DOMAIN] [--kernel KERNEL]
                   [--poolsize POOLSIZE] [--cached] [--lazy] [--index INDEX]
                   [--demo [{None,ask,trip,ca,form}]]
                   [path]

positional arguments:
  path

optional arguments:
  -h, --help            show this help message and exit
  --port PORT           Insert the port.
  --domain DOMAIN       Insert the domain.
  --kernel KERNEL       Insert the kernel path.
  --poolsize POOLSIZE   Insert the kernel pool size.
  --startuptimeout SECONDS
                        Startup timeout (in seconds) for kernels in the pool.
  --cached              The server will cache the WL input expression.
  --lazy                The server will start the kernels on the first
                        request.
  --index INDEX         The file name to search for folder index.
  --demo [{None,ask,trip,ca,form}]
                        Run a demo application
```

#### demo

Run a demo application:

 1. __ask__: Marginal Tax rate calculator using AskFunction.
 2. __trip__: Trip calculator using FormFunction and TravelDirections.
 3. __ca__: Cellular Automaton demo gallery using URLDispatcher and GalleryView.
 4. __form__: ImageProcessing demo using FormFunction.

```
>>> python3 -m wolframwebengine --demo ca
----------------------------------------------------------------------
Address         http://localhost:18000/
File            /Users/rdv/Wolfram/git/wolframengineforpython/wolframwebengine/examples/demo/ca.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

#### path

The first argument can be a folder or a single file.

Write a file on your current folder:

```
>>> mkdir testapp
>>> echo 'ExportForm[{"hello", "from", "Kernel", UnixTime[]}, "JSON"]' > testapp/index.wl
```

Then from a command line run:

```
>>> python3 -m wolframwebengine testapp
----------------------------------------------------------------------
Address         http://localhost:18000/
Folder          /Users/rdv/Desktop/testapp
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

If the first argument is a file, requests will be redirected to files in that directory if the url extension is '.m', '.mx', '.wxf', '.wl'. If the extension cannot be handled by a kernel, the file will be served as static content.

If the request path is a folder the server will search for an index.wl in the same folder.

#### --index

Specify the default file name for the folder index.
Defaults to index.wl

```
python3 -m wolframwebengine --index index.wxf
----------------------------------------------------------------------
Address         http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.wxf
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```


#### --cached

If --cached is present the code in each file will be run only once, with subsequent requests retrieving the cached result.

```
>>> python3 -m wolframwebengine --cached
----------------------------------------------------------------------
Address         http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

Visit the browser and refresh the page.


#### --port PORT

Allows you to specify the PORT of the webserver. Defaults to 18000.

```
>>> python3 -m wolframwebengine --port 9090
----------------------------------------------------------------------
Address         http://localhost:9090/
Folder          /Users/rdv/Desktop
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

#### --domain DOMAIN

Allows you to specify the DOMAIN of the webserver. By default the webserver only listens to localhost, use `0.0.0.0` to listen on all network interfaces.

```
>>> python3 -m wolframwebengine --domain 0.0.0.0
----------------------------------------------------------------------
Address         http://0.0.0.0:18000/
Folder          /Users/rdv/Desktop
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

#### --initfile FILE

Allows you to specify a custom file containing code to be run when a new kernel is started

```
>>> python3 -m wolframwebengine --initfile myinit.m
----------------------------------------------------------------------
Address         http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

#### --kernel KERNEL

Allows you to specify the Kernel path

```
>>> python3 -m wolframwebengine --kernel '/Applications/Wolfram Desktop 12.app/Contents/MacOS/WolframKernel'
----------------------------------------------------------------------
Address         http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

#### --poolsize SIZE

Wolfram Web Engine for Python will launch a pool of Wolfram Language kernels to handle incoming requests. Running more than one kernel can improve responsiveness if multiple requests arrive at the same time. The --poolsize option lets you change the number of kernels that will be launched. Defaults to 1.
```
>>> python3 -m wolframwebengine --poolsize 4
----------------------------------------------------------------------
Address         http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit)
```

#### --startuptimeout SECONDS

By default, an attempt to start a kernel will be aborted if the kernel is not ready after 20 seconds. If your application contains long-running initialization code, you may need to raise this timeout.
```
>>> python3 -m wolframwebengine
(...)
Kernel process started with PID: 485
Socket exception: Failed to read any message from socket tcp://127.0.0.1:5106 after 20.0 seconds and 245 retries.
Failed to start.


>>> python3 -m wolframwebengine --startuptimeout 50
(...)
Kernel process started with PID: 511
Connected to logging socket: tcp://127.0.0.1:5447
Kernel 511 is ready. Startup took 35.43 seconds.
```

#### --lazy 

If the option is present the server will wait for the first request to spawn the kernels, instead of spawning them immediately.


#### --client_max_size MB

The maximum amount of megabytes allowed for file upload. Defaults to 10.
```
>>> python3 -m wolframwebengine --client_max_size 150
----------------------------------------------------------------------
Address         http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit)
```

## Integrating an existing application

Wolfram Web Engine for Python can be used to augment an existing python application instead of creating a new one.
We currently support the following frameworks:

### Django

If you have an existing [Django](!https://www.djangoproject.com/) application you can use the `django_wl_view` decorator to evaluate Wolfram Language code during a web request.

```python
from __future__ import absolute_import, print_function, unicode_literals

from django.http import HttpResponse
from django.urls import path

from wolframclient.language import wl
from wolframclient.evaluation import WolframLanguageSession
from wolframwebengine.web import django_wl_view

session = WolframLanguageSession()

def django_view(request):
    return HttpResponse("hello from django")

@django_wl_view(session)
def form_view(request):
    return wl.FormFunction({"x": "String"}, wl.Identity, "JSON")


@django_wl_view(session)
def api_view(request):
    return wl.APIFunction({"x": "String"}, wl.Identity, "JSON")


urlpatterns = [
    path("", django_view, name="home"),
    path("form", form_view, name="form"),
    path("api", api_view, name="api"),
]
```

The decorator can be used with any kind of synchronous evaluator exposed and documented in [WolframClientForPython](!https://github.com/WolframResearch/WolframClientForPython).

### Aiohttp

If you have an existing [Aiohttp](!https://docs.aiohttp.org/en/stable/web_reference.html) server running you can use the `aiohttp_wl_view` decorator to evaluate Wolfram Language code during a web request.

```python
from aiohttp import web

from wolframclient.evaluation import WolframEvaluatorPool
from wolframclient.language import wl
from wolframwebengine.web import aiohttp_wl_view

session = WolframEvaluatorPool(poolsize=4)
routes = web.RouteTableDef()


@routes.get("/")
async def hello(request):
    return web.Response(text="Hello from aiohttp")


@routes.get("/form")
@aiohttp_wl_view(session)
async def form_view(request):
    return wl.FormFunction(
        {"x": "String"}, wl.Identity, AppearanceRules={"Title": "Hello from WL!"}
    )


@routes.get("/api")
@aiohttp_wl_view(session)
async def api_view(request):
    return wl.APIFunction({"x": "String"}, wl.Identity)


@routes.get("/app")
@aiohttp_wl_view(session)
async def app_view(request):
    return wl.Once(wl.Get("path/to/my/complex/wl/app.wl"))


app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app)
```

The decorator can be used with any kind of asynchronous evaluator exposed and documented in [WolframClientForPython](!https://github.com/WolframResearch/WolframClientForPython).

