(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['download_description'] = template({"compiler":[8,">= 4.3.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, lookupProperty = container.lookupProperty || function(parent, propertyName) {
        if (Object.prototype.hasOwnProperty.call(parent, propertyName)) {
          return parent[propertyName];
        }
        return undefined
    };

  return "  "
    + ((stack1 = ((helper = (helper = lookupProperty(helpers,"dl_file_text") || (depth0 != null ? lookupProperty(depth0,"dl_file_text") : depth0)) != null ? helper : container.hooks.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : (container.nullContext || {}),{"name":"dl_file_text","hash":{},"data":data,"loc":{"start":{"line":1,"column":2},"end":{"line":1,"column":20}}}) : helper))) != null ? stack1 : "");
},"useData":true});
})();