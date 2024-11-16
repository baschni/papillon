from multipledispatch import dispatch
from json import dumps as j
from init.logics_gui_core.old import init_classes
from init.design import init_design
from init.init import init_logic
from queue import Queue

# https://stackoverflow.com/questions/8024149/is-it-possible-to-get-the-non-enumerable-inherited-property-names-of-an-object
# https://stackoverflow.com/questions/57095521/how-to-iterate-through-the-keys-of-a-event-object
SimplePropertyRetriever = """

var GetDictionaryOfElements = function(obj)
{
    NOT_AVAILABLE = ["composedPath","initEvent","preventDefault","stopImmediatePropagation","stopPropagation","__defineGetter__","__defineSetter__","hasOwnProperty","__lookupGetter__","__lookupSetter__","isPrototypeOf","propertyIsEnumerable","toString","valueOf","toLocaleString"];


    var propd = {};
    elements = SimplePropertyRetriever.getOwnAndPrototypeEnumerablesAndNonenumerables(event);
    for (i in elements)
    {
        property = elements[i];
        property_type = typeof obj[property]
        if (property_type === "number" || property_type === "boolean" || property_type === "string")
        {
            propd[property] = obj[property];
        }
    }
    return propd;
}
var SimplePropertyRetriever = {
  getOwnAndPrototypeEnumerablesAndNonenumerables: function(obj) {
      return this._getPropertyNames(obj, true, true, this._enumerableAndNotEnumerable);
  },
  getOwnAndPrototypeEnumerablesAndNonenumerablesAsDictionary: function(obj) {
      return this._getPropertyDictionary(obj, true, true, this._enumerableAndNotEnumerable);
  },
  _enumerableAndNotEnumerable: function(obj, prop) {
      return true;
  },
  // Inspired by http://stackoverflow.com/a/8024294/271577
  _getPropertyNames: function getAllPropertyNames(obj, iterateSelfBool, iteratePrototypeBool, includePropCb) {
      var props = [];

      do {
          if (iterateSelfBool) {
              Object.getOwnPropertyNames(obj).forEach(function(prop) {
                  if (props.indexOf(prop) === -1 && includePropCb(obj, prop)) {
                      props.push(prop);
                  }
              });
          }
          if (!iteratePrototypeBool) {
              break;
          }
          iterateSelfBool = true;
      } while (obj = Object.getPrototypeOf(obj));

      return props;
  },

    _getPropertyDictionary: function getPropertyDictionary(obj, iterateSelfBool, iteratePrototypeBool, includePropCb) {
      var props = [];
      var propd = {};

      do {
          if (iterateSelfBool) {
              Object.getOwnPropertyNames(obj).forEach(function(prop) {
                  if (props.indexOf(prop) === -1 && includePropCb(obj, prop)) {
                      props.push(prop);
                      //alert(prop);
                      //alert(obj[prop])
                      //propd[prop] = obj[prop];
                  }
              });
          }
          if (!iteratePrototypeBool) {
              break;
          }
          iterateSelfBool = true;
      } while (obj = Object.getPrototypeOf(obj));

      return propd;
  },
};
"""

class Gui():
    def __init__(self, window):
        self.window = window
        #self.api = window._js_api

        self.events = dict()
        self.event_queue = Queue()
        self.working = False

        window.expose(self.trigger_event)

    def init_after_page_loading(self):
        self.js("document.documentElement.id = 'html'")
        self.add(Element, "html")
        self.js("document.body.id = 'body'")
        self.add(Element, "body")
    def add(self, gui_class, html_id):
        # add variable to class object namespace by constructing a new object of type gui_class
        if html_id in self.__dict__.keys():
            raise Exception("HTML-Element mit id #" + html_id + "bereits hinzugefügt!")
        element = self.__dict__[html_id] = gui_class(html_id, self)
        element.parent = self
        return element

    def getElementById(self, id):
        if id in self.__dict__:
            return self.__dict__[id]
        else:
            return None

    def add_global(self, name, value):
        # helper function to be used inside a lambda for assigning a value to a variable
        self.__dict__[name] = value
        return value

    def js(self, script):
        return self.window.evaluate_js(script)

    def scroll_into_view(self, id):
        js = f"document.getElementById('{id}').scrollIntoView()"
        self.js(js)
    def alert(self, message):
        self.js(f"alert({j(message)})")

    def prompt(self, message):
        return self.js(f"prompt({j(message)});")

    def register_event(self, id, element, event, block_main_thread=True):
        # https://stackoverflow.com/questions/57095521/how-to-iterate-through-the-keys-of-a-event-object

        # if new element is not equal to previous element, delete all events registered
        if id not in self.events.keys() or self.events[id][0] != element:
            self.events[id] = (element, [], [])

        if event not in self.events[id][1]:
            self.events[id][1].append(event)
            self.events[id][2].append(block_main_thread)
            # print(SimplePropertyRetriever)
            register_event = SimplePropertyRetriever + f"""
                 document.getElementById({j(id)}).addEventListener(
                 {j(event)},
                 function(event) {{ window.pywebview.api.trigger_event({j(id)}, {j(event)}, GetDictionaryOfElements(event)); }}
                 )
                 """
            self.window.evaluate_js(register_event)

    def trigger_event(self, id, event, event_information):
        # work events with queue so that events do not coincide

        self.event_queue.put((id, event, event_information))
        #print(id, event)
        if self.working == False:
            self.work_events()

    def work_events(self):

        self.working = True
        while True:
            event = self.event_queue.get()
            if event is None:
                break
            # print("1",event[0])
            # print("2",self.events[event[0]])
            # print("3", self.events[event[0]][0])
            element_html_id = event[0]
            event_name = event[1]

            events_for_id = self.events[element_html_id]
            event_element = events_for_id[0]
            event_keywords = events_for_id[1]
            event_threading = events_for_id[2]
            if event_name in event_keywords:
                #print("started element trigger event")
                event_element.trigger_event(event[1], event[2], event_threading[event_keywords.index(event_name)])
        self.working = False

    def unregister_event(self, id, vent):
        pass

    def initialize(self):
        init_classes(self)
        init_design(self)
        init_logic(self)


    @dispatch(str, str, str)
    def load_css(self, identifier, css_attribute, css_value):
        css = f"""
                        {identifier}
                        {{
                        {css_attribute} : {css_value};
                        }}
                        """
        self.window.load_css(css)

    @dispatch(str, str)
    def load_css(self, identifier, css_code):
        css = f"""
                        {identifier}
                        {{
                        {css_code}
                        }}
                        """
        self.window.load_css(css)

    @dispatch(str, dict)
    def load_css(self, identifier, css_dict):
        css = f"""
                    {identifier}
                    {{
                    {"".join(attribute + ": " + value + ";" for attribute, value in css_dict.items())}
                    }}
                    """
        self.window.load_css(css)