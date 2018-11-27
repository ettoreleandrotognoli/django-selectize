import * as $ from "jquery";
import "selectize";

enum SelectizeType {
  Remote = "remote",
  Eager = "eager"
}

enum CreateStrategyType {
  Modal = "modal",
  Inline = "inline"
}

interface SelectizeRemoteOptions {
  type: SelectizeType.Remote
  createUrl: string
  createStrategy: CreateStrategyType
  searchUrl: string,
  options: Array<any>,
  items: Array<any>
}

interface SelectizeEagerOptions {
  type: SelectizeType.Eager
  options: Array<any>,
  items: Array<any>
}

type SelectizeOptions = SelectizeRemoteOptions | SelectizeEagerOptions;

interface SelectizeCreateStrategy {
  create(input: string, callback: (_: any) => void): void;

}

interface SelectizeSearchStrategy {
  search(query: string, callback: (_: Array<any>) => void): void;
}

export class AjaxSearchStrategy implements SelectizeSearchStrategy {

  constructor(
    protected el: HTMLElement
  ) { }

  get searchUrl(): string {
    return this.el.getAttribute("selectize-search-url");
  }

  getSearchUrl(query: string) {
    const [path, querystring] = this.searchUrl.split("?", 2)
    return path + `?q=${encodeURI(query)}&${querystring || ""}`;
  }

  search(query: string, callback: (_: Array<any>) => void): void {
    $.ajax({
      url: this.getSearchUrl(query),
      type: "GET",
      error: (error) => {
        console.log(error);
        callback([]);
      },
      success: callback
    })
  }
}

export class InlineCreateStrategy implements SelectizeCreateStrategy {
  constructor(
    protected el: HTMLElement
  ) { }

  get createUrl(): string {
    return this.el.getAttribute("selectize-create-url");
  }

  getCreateUrl(query: string) {
    const [path, querystring] = this.createUrl.split("?", 2)
    return path + `?q=${encodeURI(query)}&${querystring || ""}`;
  }


  create(input: string, callback: (_: any) => void): void {
    $.ajax({
      url: this.getCreateUrl(input),
      type: "POST",
      data: {q : input},
      error: (error) => {
        console.log(error);
        callback([]);
      },
      success: callback
    })
  }

}

/*
export class ModalCreateStrategy implements SelectizeCreateStrategy {

}
*/

export class Selectize {

  static buidFrom(el: HTMLElement): Selectize {
    return new Selectize(el, new AjaxSearchStrategy(el));
  }

  static extractData(el: HTMLElement): SelectizeOptions {
    const data = Array.from(el.attributes)
      .filter(it => it.name.startsWith("selectize-"))
      .reduce((acc, it) => Object.assign(acc, { [it.name]: it.value }), {});
    return { ...data, type: el.getAttribute("selectize") } as SelectizeOptions;
  }

  constructor(
    protected el: HTMLElement,
    protected searchStrategy: SelectizeSearchStrategy,
    protected createStrategy?: SelectizeCreateStrategy
  ) {

    const data = Selectize.extractData(el);

    const loadFunction = (query, callback) => {
      this.searchStrategy.search(query, callback)
    }

    const createFunction = this.createStrategy ? (input, callback) => {
      this.createStrategy.create(input, callback);
    } : false;

    $(el).selectize({
      load: loadFunction,
      create: createFunction,
      options: data.options,
      items: data.items,
      valueField: "id",
      labelField: "__item__",
      searchField: "__option__",
      render: {
        item: (item, escape) => {
          return item.__item__;
        },
        option: (item, escape) => {
          return item.__option__;
        }
      }
    });
  }


}

export function prepareDocument(document) {
  $(document)
    .find("[selectize]")
    .each(function () {
      const data = Selectize.extractData(this);
      console.log(data);
      const selectize = new Selectize(this, new AjaxSearchStrategy(this), new InlineCreateStrategy(this));
      console.log(selectize);
    });
}

$(() => {
  prepareDocument(document);
});

$(() => {
  $(function () {
    function renderTemplate(template, data) {
      let render = decodeURI(template);
      Object.entries(data).forEach(function ([k, v]) {
        let regex = RegExp("<" + k + ">", "g");
        render = render.replace(regex, v as string);
      });
      console.log(template, render);
      return encodeURI(render);
    }

    function prepareListener(listener, properties) {
      properties.forEach(function (property) {
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
      properties.forEach(function (property) {
        let template = listener.attr("template-" + property);
        let newContent = renderTemplate(template, newValue);
        listener.attr(property, newContent);
      });
    }

    function updateListeners(name, value) {
      let attr = "listen-" + name;
      let listeners = $("[" + attr + "]");
      listeners.each(function (index, element) {
        let listener = $(element);
        let properties = listener.attr(attr).split(" ");
        prepareListener(listener, properties);
        updateListener(listener, properties, { [name]: value });
        console.log(listener, properties, { [name]: value });
      });
    }

    $("[model]").each(function (index, element) {
      let self = $(element);
      let model = self.attr("model");
      $(element).on("change", function () {
        updateListeners(model, self.val());
      });
      updateListeners(model, self.val());
    });
  });
});
