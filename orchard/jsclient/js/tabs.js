// Tab loader
function load_tab(id, title, url){
	$.ajax({
	  url: url,
	  success: function(contents){
		display_tab(id, title, contents);
	  }
	});
}

function display_tab(id, title, contents) {
	// Create tab
	$('ul.tabs-main').append('<li id="__tab_'+id+'"><a href="#'+id+'">'+title+'</a></li>');
	// Create content
	tabcontent = '<div class="tab-pane" id="'+id+'">'+contents+'</div>';
	$('.content.toplevel > .tab-content').append(tabcontent);
	// Activate tab
	select_tab(id)
}

function select_tab(id, title, url){
	if ($('#__tab_'+id+" a").length == 0) {
		load_tab(id, title, url);
	} else {
		$('#__tab_'+id+" a").click();
	}
}

prebuilt_tabs = {
	"welcome":['Welcome', '/tab/welcome.html'],
	"console":['Console', '/tab/console.html']
}

function prebuilt_tab(name){
	details = prebuilt_tabs[name];
	select_tab(name, details[0], details[1])
	return false;
}

function close_tab(name){
	if (!name) {
		name = current_tab();
	}
	if (name == "console") console_bcp.stream.disconnect()

	var stab = prev_tab() || next_tab();
	$('#'+name).remove();
	$('#__tab_'+name).remove();
	if (stab){
		select_tab(stab);
	} else {
		prebuilt_tab('welcome');
	}
}

function num_tabs(){
	return $('.tab-content > *').length;
}

function current_tab(){
	return $('.tab-content > .active').attr('id');
}

function next_tab(){
	var c = current_tab();
	var n = name_each_tab();
	var i = n.indexOf(c);
	return n[i+1];
}

function prev_tab(){
	var c = current_tab();
	var n = name_each_tab();
	var i = n.indexOf(c);
	return n[i-1];
}

function name_each_tab(){
	var tabs = $('.tab-content > *');
	var names = new Array();
	for (var i=0; i < tabs.length; i++){
		names.push($(tabs[i]).attr('id'));
	}
	return names;
}
