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
