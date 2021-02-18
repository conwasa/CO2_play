(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['latest_co2_readings'] = template({"compiler":[8,">= 4.3.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=container.hooks.helperMissing, alias3="function", lookupProperty = container.lookupProperty || function(parent, propertyName) {
        if (Object.prototype.hasOwnProperty.call(parent, propertyName)) {
          return parent[propertyName];
        }
        return undefined
    };

  return ((stack1 = ((helper = (helper = lookupProperty(helpers,"line1") || (depth0 != null ? lookupProperty(depth0,"line1") : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"line1","hash":{},"data":data,"loc":{"start":{"line":1,"column":0},"end":{"line":1,"column":11}}}) : helper))) != null ? stack1 : "")
    + "<br>"
    + ((stack1 = ((helper = (helper = lookupProperty(helpers,"line2") || (depth0 != null ? lookupProperty(depth0,"line2") : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"line2","hash":{},"data":data,"loc":{"start":{"line":1,"column":15},"end":{"line":1,"column":26}}}) : helper))) != null ? stack1 : "")
    + "<br>"
    + ((stack1 = ((helper = (helper = lookupProperty(helpers,"line3") || (depth0 != null ? lookupProperty(depth0,"line3") : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"line3","hash":{},"data":data,"loc":{"start":{"line":1,"column":30},"end":{"line":1,"column":41}}}) : helper))) != null ? stack1 : "")
    + "<br>";
},"useData":true});
})();