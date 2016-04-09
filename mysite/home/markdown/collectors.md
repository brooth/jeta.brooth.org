<div class="page-header">
    <h2>Jeta Collectors</h2>
</div>

`Jeta Collectors` allow you, well, to collect scattered types in your project. Let's get through with an example. Assume we have an `EventManager` that receives events outside and invokes appropriate handler:

    :::java
    interface EventHandler {
        void handle(Event event);
    }

    enum EventType {
        EVENT_ONE,
        EVENT_TWO
    }

    class EventManager {
        Map<EventType, EventHandler> handlers;
    }

Commonly used practice, is to create an xml file and register all the handlers in it. In the event manager we must parse the xml and load these handlers through `Class.forName()`:

    :::java
    class HandlerOne implements EventHandler {
        void handle(Event event) {
        }
    }

    class HandlerTwo implements EventHandler {
        void handle(Event event) {
        }
    }

<span/>

    :::xml
    <handlers>
        <handler type="EVENT_ONE" class="com.example.collector.abc.HandlerOne"/>
        <handler type="EVENT_TWO" class="com.example.collector.bcd.abc.HandlerTwo"/>
    </handlers>

<span/>

    :::java
    class EventManager {
        void collectHandlers() {
            // parse XML, Class.forName(), etc
        }
    }

Besides that this approach has no validation, and fails at runtime in case of misspelling, it's frequently forgotten to amend the xml file each time you add new handler into your project.

###TypeCollector

`TypeCollector` searches for types that use given annotation and collect them during compilation stage. Let's modify the example above to illustrate the potential:


    :::java
    @interface Handler {
        EventType[] value();
    }

    @Handler(EVENT_ONE)
    class HandlerOne implements EventHandler {
        void handle(Event event) {
        }
    }

    @Handler(EVENT_TWO)
    class HandlerTwo implements EventHandler {
        void handle(Event event) {
        }
    }

    @TypeCollector(Handler.class)
    class EventManager {
        void collectHandlers() {
             Collection<? extends Class> types =
                MetaHelper.collectTypes(EventManager.class, Handler.class);
            // transform types -> handlers
        }
    }

As you expect, `MetaHelper.collectTypes` will return a collection of `HandlerOne` and `HandlerTwo`. So, if you add new handler and put `@Handler` on, `TypeCollector` will return it as well, without any amendments.

 <span class="label label-info">Note</span> It's allowed to use one `TypeCollector` for searching many annotations. Just pass these annotations into `@TypeCollector`'s value. This is why you must specify annotation class in `collectTypes` parameters.

###ObjectCollector

`ObjectCollector` does the same as `TypeCollector`, unlike it returns not the types but providers of these types. So if you need to create the instances, you should use `ObjectCollector` instead of `TypeCollector`:

    :::java
    @ObjectCollector(Handler.class)
    class EventManager {
        Map<EventType, Provider<EventHandler>> handlers;

        void collectHandlers() {
                List<Provider<?>> objects =
                    MetaHelper.collectObjects(EventManager.class, Handler.class);
            // transform objects -> handlers
        }
    }

###MetaHelper

Add the following methods into `MetaHelper` in order to use these features.

    :::java
    public static List<Class<?>> collectTypes(Class<?> masterClass, Class<? extends Annotation> annotationClass) {
        return new TypeCollectorController(metasitory, masterClass).getTypes(annotationClass);
    }

    public static List<Provider<?>> collectObjects(Class<?> masterClass, Class<? extends Annotation> annotationClass) {
        return new ObjectCollectorController(metasitory, masterClass).getObjects(annotationClass);
    }
