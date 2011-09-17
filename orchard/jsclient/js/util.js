// util.js :: Utilities

// dependencies: A BCP object must be available to handle md5 requests

function arrayfill(array, value, count) {
	for (var i=0;i<count;i++) {array.push(value(i));}
}

function af_obj(id) {
	return {};
}


// Really. REALLY. Hacky. JavaScript, why you no have type() function?

function isArray(obj){
	//return JSON.stringify(obj)[0]==="[";
    if (typeof obj === "object") {
        return Object.prototype.toString.call(obj) === "[object Array]";
    }
    else {
        return false;
    }

}

function isObject(obj){
	//return JSON.stringify(obj)[0]==="{";
    return typeof obj === "object";
}

function isString(obj){
	//return JSON.stringify(obj)[0]==='"';
    return typeof obj === "string";
}

function isInt(obj){
	//return obj === int(obj);
    return typeof obj === "number";
}

function isBoolean(obj){
    return typeof obj === "boolean";
}

function int(num){
	return (num-1+1);
}

function range(start, end) {
	result = [];
	for (var i=start; i<end; i++) result.push(i);
	return result;
}

function get_url_variable(name, def){
	query = window.location.href.split('?')[1];
	if (query===undefined) return def;
	params = query.split("&");
	for (var i in params) {
		split = params[i].split("=");
		if (split[0] == name) return split[1];
	}
	return def;
}

function isJSON(str){
	try {
		JSON.parse(str);
		return true;
	} catch(exception){
		return false;
	}
}

serial = {
	"key": function(str){
		if (str.length>10){
			return str.slice(0,10)+serial.sum(str.slice(10));
		}else{
			return str;
		}
	},
	"modulo":65536, // 2^8
	"sum": function(str){
		var s = 0;
		for (var i=0; i<str.length;i++){
			s = (s*s + str.charCodeAt(i)) % serial.modulo;
		}
		return s;
	},
	"strict": function(obj){
	}
};

function assert(condition, message){
	if (message){
		message = "Assertion error: \""+message+"\"";
	} else {
		message = "Assertion error";
	}
	if (!condition) throw message;
}