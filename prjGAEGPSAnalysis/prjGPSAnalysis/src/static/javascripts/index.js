(function(){
	/* Angular.js */
	
	/* JQuery */
	var $list_icon = $('#list_icon');
	$('.navbar-collapse a').click(function() {
		if ($list_icon.is(":visible")) {
			$(".navbar-collapse").collapse('hide');
		}
	});
})();