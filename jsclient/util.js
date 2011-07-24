// util.js :: Utilities

// dependencies: A BCP object must be available to handle md5 requests

function arrayfill(array, value, count) {
	for (var i=0;i<count;i++) {array.push(value(i))}
}

function af_obj(id) {
	return {};
}

function isArray(obj){
	return JSON.stringify(obj)[0]=="["
}

function range(start, end) {
	result = [];
	for (var i=start; i<end; i++) result.push(i);
	return result;
}

function get_url_variable(name, def){
	query = window.location.href.split('?')[1];
	if (query==undefined) return def;
	params = query.split("&");
	for (i in params) {
		split = params[i].split("=");
		if (split[0] == name) return split[1];
	}
	return def;
}

function isJSON(str){
	try {
		JSON.parse(str)
		return true;
	} catch(exception){
		return false;
	}
}

md5table = {};

function md5(text, bcp) {
	if (md5table[text] != undefined) {
		return md5table[text];
	} else {
		bcp.send({"type":"hash", "value":text})
		return undefined;
	}
}

function unmd5(hash){
	for (var key in md5table) {
		if (md5table[key]==hash) return key;
	}
}

function address_js(addr){
	// convert a BCP address into a JS address
	var parts = addr.split("/")
	result = []
	for (i in parts){
		var targets = parts[i].split(":");
		var index = targets[0];
		var hash = targets[1];
		var value = unmd5(hash);
		if (value==undefined) return undefined;
		result.push([index, value]);
	}
	return result;
}

function address_bcp(addr){
	// convert a JS address into a BCP address
	result = [];
	for (i in addr){
		var part = addr[i];
		var hash = md5(part[1]);
		if (hash==undefined) return undefined;
		result.push(""+part[0]+":"+hash)
	}
	return result.join("/");
}
