(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['download_description'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper;

  return "  "
    + ((stack1 = ((helper = (helper = helpers.dl_file_text || (depth0 != null ? depth0.dl_file_text : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : (container.nullContext || {}),{"name":"dl_file_text","hash":{},"data":data}) : helper))) != null ? stack1 : "");
},"useData":true});
})();