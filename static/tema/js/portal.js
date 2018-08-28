$j = jQuery.noConflict();

function createCookie(name,value,days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}

function eraseCookie(name) {
	createCookie(name,"",-1);
};

function HoverMenu(){
	var item_first = $j('ul#portal-globalnav-top li:eq(0)').hasClass('selected');
	var item_last = $j('ul#portal-globalnav-top li:last').hasClass('selected');
	if (item_first == true) {
		$j('ul#portal-globalnav-top').removeClass('menu-back-left').addClass('menu-back-hover-left');
	};
	if (item_last == true) {
		$j('ul#portal-globalnav-top').parent().removeClass('menu-back-right').addClass('menu-back-hover-right');
	};
};
function lecookie(e){
	var id = e.id;
	eraseCookie('link');
	createCookie('link',id,1);
	
	
};


$j(document).ready(function(){

	//MENU SUPERIOR
	var link = 'li#'+readCookie('link');
	if (link != null){
		$j(link).addClass('selected');
	};
	$j("ul#portal-globalnav-top li").click(function(){
		lecookie(this);
	});
	$j('.cookie').click(function(){
		lecookie(this);
	});

	HoverMenu();
	
	$j('ul#portal-globalnav-top li').mouseenter(function(){
		var selected = $j(this).hasClass('plain');
			if(selected == true){
				$j(this).addClass('selected');
				HoverMenu();
			}
	});
	
	$j('ul#portal-globalnav-top li').mouseleave(function(){
		var selected = $j(this).hasClass('plain');
			if(selected == true){
				$j(this).removeClass('selected').parent().removeClass('menu-back-hover-left').addClass('menu-back-left').parent().removeClass('menu-back-hover-right').addClass('menu-back-right');
				HoverMenu();
			};
	});

});