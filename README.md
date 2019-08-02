# Akuanduba

<p align="center">
  <img width="460" height="300" src="https://raw.githubusercontent.com/gabriel-milan/Akuanduba/master/img/Akuanduba.jpg">
</p>

Image source: [link](https://my-bestiario.fandom.com/pt-br/wiki/Akuanduba)

Akuanduba is a Python framework that eases manipulation of multiple running threads and shared resources. Its name was inspired by a god of the Brazilian mythology: Akuanduba, the god of order.

This framework's been based on the [Gaugi](https://gitlab.cern.ch/jodafons/gaugi) project, a framework that João, the author of Gaugi, presented to me.

# The paradigm

Using Akuanduba, you'll have three base classes you can use to attend your needs, as they relate to one another through a common class called *Context* (this will be explained really soon). The three classes are:

* *AkuandubaTool*;
* *AkuandubaService*;
* *AkuandubaDataframe*.

**AkuandubaDataframe** is a base class for data models that will be attached to the *Context*. In other words, these *data frames* can store anything you desire and be accessible from any *tool* or *service* running on your main script. **Example:** Use data frames for storing data acquired with a service.

**AkuandubaTool** is a base class for methods that will run once on every call, processing data from any *data frame* attached to the *Context* and appending the results to another *data frame* (or even the same). *Tools* have one main method: the "execute", where all the calculations will occur every time they're called. **Example:** Use tools to process data acquired by a service and store it on a data frame.

**AkuandubaService** is a base class for parallel threads. These *services* have two main methods: "run", which is a loop that will be running parallel to the whole framework and "execute", that's executed once in every call. **Example**: Use services to acquire data.

Besides these base classes, Akuanduba relies on few other main concepts:

* *Context*;
* *DataframeManager*;
* *ToolManager*;
* *ServiceManager*;
* *Trigger*.

The **Context** is an abstraction that holds every single thing attached to the framework: *tools*, *services* and *data frames*. This way, everything is accessible from any other component attached to Akuanduba.

### To be continued... 