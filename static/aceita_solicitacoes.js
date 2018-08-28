//Aceita ou nega a solicitacão dos produtos
$j = jQuery.noConflict();

$j(document).ready(function () {
	
		$j("#aceitar").click(function(){
			$j("#status").attr({checked:'checked'});
			$j(".form-status").submit();			

		});

		$j("#negar").click(function(){
			$j(".negacao").css('display','block');
			$j(".nega-botao").css('display','none');	
	
		});	
});
