(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['latest_co2_readings'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function";

  return ((stack1 = ((helper = (helper = helpers.line1 || (depth0 != null ? depth0.line1 : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"line1","hash":{},"data":data}) : helper))) != null ? stack1 : "")
    + "<br>"
    + ((stack1 = ((helper = (helper = helpers.line2 || (depth0 != null ? depth0.line2 : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"line2","hash":{},"data":data}) : helper))) != null ? stack1 : "")
    + "<br>"
    + ((stack1 = ((helper = (helper = helpers.line3 || (depth0 != null ? depth0.line3 : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"line3","hash":{},"data":data}) : helper))) != null ? stack1 : "")
    + "<br>";
},"useData":true});
})();