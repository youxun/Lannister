

$(document).ready(function(){
	$("li#link_li").click(function(){
		$clicked = $(this);
		//alert($clicked.attr('class'));
		if (typeof($clicked.attr("class")) === "undefined")
		{
			$clicked.attr("class","active")
		}
		//alert($("li.active").tagName);
		$(this).addClass("active");
	});
});