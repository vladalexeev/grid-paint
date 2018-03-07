$(function() {
	$('.thumbnail').click(function() {
		var href = $(this).find('a').attr('href');
		document.location = href;	
	});
});
