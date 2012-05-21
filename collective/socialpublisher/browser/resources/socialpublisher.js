$(document).ready(function(){
	// XXX: re-do this using plone base fold/unfold
	$("#socialpublisher-viewlet a.hide").click(function(){
		$(this).closest('.wrapper').find('.content').hide();
		$("#socialpublisher-viewlet a.show").show();
		$("#socialpublisher-viewlet a.hide").hide();
	});
	$("#socialpublisher-viewlet a.show").click(function(){
		$(this).closest('.wrapper').find('.content').show();
		$("#socialpublisher-viewlet a.hide").show();
		$("#socialpublisher-viewlet a.show").hide();
	});
});