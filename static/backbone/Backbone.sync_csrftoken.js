var oldSync = Backbone.sync;
Backbone.sync = function(method, model, options){
	options.beforeSend = function(xhr){
		xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
	};
	return oldSync(method, model, options);
};