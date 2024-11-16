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


class Api():

    def __init__(self):
        pass

    def print(self, value):
        print(value)

    def set_gui(self, gui):
        pass
        self.gui = gui
        #self.window = gui.window



    # def initialize(self):
    #     init_classes(self.gui)
    #     init_design(self.gui)
    #     init_logic(self.gui)

































    # def prompt_function(self, message):
    #     pass
    #
    # def set_prompt_function(self, receiving_function):
    #     print("setting prompt function")
    #     def prompt_function(message):
    #         print("api prompt function triggered: " + message)
    #         receiving_function(message)
    #
    #         def empty_function(message):
    #             pass
    #
    #         self.prompt_function = empty_function
    #
    #     self.prompt_function = prompt_function
    # self.prompt_function("test")

    # def set_prompt_function(self, function):
    #     pass
    # def prompt_function(message):
    #     pass
    # function(message)
    # self.prompt_function = None

    # self.prompt_function = prompt_function