import * as $ from "jquery";
import "selectize";

export class RemoteSelectize {
  constructor(protected el: HTMLElement) {
    $(el).selectize({});
    console.log(this,el);
  }
}

export function prepareDocument(document) {
  $(document)
    .find("[selectize=remote]")
    .each(function(){
      new RemoteSelectize(this);
    });
}

$(() => {
  prepareDocument(document);
});

$(() => {
  $(function() {
    function renderTemplate(template, data) {
      let render = decodeURI(template);
      Object.entries(data).forEach(function([k, v]) {
        let regex = RegExp("<" + k + ">", "g");
        render = render.replace(regex, v as string);
      });
      console.log(template, render);
      return encodeURI(render);
    }

    function prepareListener(listener, properties) {
      properties.forEach(function(property) {
        let template = listener.attr("template-" + property);
        if (template) {
          return;
        }
        template = listener.attr(property);
        listener.attr("template-" + property, template);
      });
    }

    function updateListener(listener, properties, value) {
      let oldValue = listener.attr("listened");
      try {
        oldValue = JSON.parse(oldValue);
      } catch (ex) {
        oldValue = {};
      }
      let newValue = $.extend(oldValue, value);
      listener.attr("listened", JSON.stringify(newValue));
      properties.forEach(function(property) {
        let template = listener.attr("template-" + property);
        let newContent = renderTemplate(template, newValue);
        listener.attr(property, newContent);
      });
    }

    function updateListeners(name, value) {
      let attr = "listen-" + name;
      let listeners = $("[" + attr + "]");
      listeners.each(function(index, element) {
        let listener = $(element);
        let properties = listener.attr(attr).split(" ");
        prepareListener(listener, properties);
        updateListener(listener, properties, { [name]: value });
        console.log(listener, properties, { [name]: value });
      });
    }

    $("[model]").each(function(index, element) {
      let self = $(element);
      let model = self.attr("model");
      $(element).on("change", function() {
        updateListeners(model, self.val());
      });
      updateListeners(model, self.val());
    });
  });
});
