/**
 * jquery.steps-0.1,js - Steps plugin for jQuery
 * ================================================
 * (C) 2011 José Ramón Díaz - jrdiazweb@gmail.com
 * 
 * Instantiation: $('.stepsDiv').steps()
 * 
 * Functions:
 *     $('.stepsDiv').steps('getStep') - Returns current step for stepDiv
 *     $('.stepsDiv').steps('start')   - Resets state to initial step
 *     $('.stepsDiv').steps('finish')  - Sets state to completed
 *     $('.stepsDiv').steps('next')    - Sets state to next state
 *     $('.stepsDiv').steps('prev')    - Sets state to previous state
 *     
 * Classes needed and meaning
 *     N/A              - Uncompleted step. Greyed by default
 *     end              - Last uncompleted step. Greyed and no "arrow"
 *     last             - Boundary class. Marks last completed step and last step
 *     current          - Current step
 *     completed        - Completed step
 *     completedLast    - Last completed step
 *     completedLastEnd - Last step when all steps are completed
 * 
 * Extending steps with representation
 *     You can also use the steps CSS. You can find it at
 *     http://3nibbles.blogspot.com/2011/06/pasos-de-wizard.html
 *     
 * Legal stuff
 *     You are free to use this CSS, but you must give credit or keep header intact.
 *     Please, tell me if you find it useful. An email will be enough.
 *     If you enhance this code or correct a bug, please, tell me.
 * 
 */
//stack init
/*
function InitStack(stack){
	if (stack) return stack;
	stack=new Array();
	return stack;
}

function Empty(stack){
	var returnValue=false;
	if(stack.length ==0) returnValue=true;
	return returnValue;
}

function Push(stack,x){
	var returnValue=0;
	var stackLength=stack.length;
	stack.length=stack.length+1;
	stack[stackLength]=x;
	return stack.length
}

function Pop(stack){
	var returnValue=NULL;
	var stackLength=stack.length;
	if (stackLength>=1)
	{
		returnValue=stack[stackLength-1]
		stack.length=stackLength-1
	}
	return returnValue
}

function Get(stack){
	var returnValue=NULL;
	var stackLength=stack.length;
	returnValue=stack[stackLength]; //直接返回顶部元素即可
	return returnValue;
}


function Clear(stack){ //清空堆栈
	stack.length=0; //将元素的个数清零即可
	return true;
}

function Current_size(stack){ //获得线性堆栈的当前大小
	return stack.length;
}
// Demo methods

*/
(function( $ ){

    $.fn.steps = function( options ) {  
        
        var self = this;
        
        
        //////////////////////////////////////////////////////////////////////////////////
        // DEFAULT VALUES
        var defaults = {};
		var p_data={'minute':'','hour':'','day':'','month':'','week':''}
        //////////////////////////////////////////////////////////////////////////////////
        // PRIVATE FUNCTIONS
        var init = function( options ) {
            
            // If options exist, merge them with default settings
            if ( options ) $.extend( defaults, options );
        
            var $this = $(this);
            var data = $this.data('steps');
            
            return this.each(function() {
                
                var $this = $(this);
                data      = $this.data('steps');
                
                // The plugin hasn't been initialized yet
                if ( ! data ) {
                    
                    // Initializes the plugin data
                    $(this).data('steps', { 
                        target : $this,
                        step   : 0
                    });
    
                };
            });            
            
        };
        
        var destroy = function( ) { 
            return this.each(function() { self.removeData('steps'); })
        };

		//////////////////////////////////////////////////////////////////////////////////
		// POST Data FUNCTIONS
		var post_datas = {
				JqGetValue: function(controlID, controltype) {  
					var objValue = "";  
					switch (controltype) {  
						case 'text': //文本输入框  
							objValue = $.trim($("#" + controlID + "").attr("value")); //取值去左右空格  
							break;  
						case 'radio': //单选框  
							objValue = $("input[name='" + controlID + "']:checked").attr("value");  
							break;  
						case 'select': //下拉列表  
						//alert($("#selectMinuteFrom").val()+'selecttest')
							objValue = $("#" + controlID + "").val();  
							break;  
						case 'checkbox': //多选框  
							$("input[name='" + controlID + "']:checked").each(function () {  
								objValue += $(this).val() + ",";  
							});  
							break;  
						default:  
							break;
						}
					
					return objValue; 
					},  
				post_minute : function(){
					if (post_datas.JqGetValue('optionsRadiosMinute','radio')==1)
					{	
						return post_datas.JqGetValue('selectMinuteFrom','select')+'/'+post_datas.JqGetValue('selectMinuteEvery','select');
					}else{
						return post_datas.JqGetValue('minutecheckbox','checkbox');
					}
				},
				post_hour : function(){
					return (post_datas.JqGetValue('optionsRadiosHours','radio')==1)?('*'):post_datas.JqGetValue('hourcheckbox','checkbox')
				},
				post_month :	function(){
					return (post_datas.JqGetValue('optionsRadiosMonth','radio')==1)?('*'):post_datas.JqGetValue('monthcheckbox','checkbox')
				},	
				post_day : function(){
					return (post_datas.JqGetValue('optionsRadiosDay','radio')==1)?('*'):post_datas.JqGetValue('daycheckbox','checkbox')	
				},
				post_week : function(){
					if (post_datas.JqGetValue('weekcheckbox','checkbox'))
					{
					return (post_datas.JqGetValue('optionsRadiosWeek','radio')==1)?('*'):post_datas.JqGetValue('weekcheckbox','checkbox')
					}else{
					return '?'
					}
				},
				post_step1 :function(){
					p_data['minute']= post_datas.post_minute()
					p_data['hour']= post_datas.post_hour()
					p_data['month']= post_datas.post_month()
					p_data['day']= post_datas.post_day()
					if (post_datas.post_week()!='?')
					{
						p_data['day'] = '?'
					}
					p_data['week']= post_datas.post_week()
					return p_data
				},
				post_step2 :function(){},
				post_step3 :function(){},

				obj2Str : function(obj){  
					switch(typeof(obj)){  
						case 'object':  
							var ret = [];  
							if (obj instanceof Array){  
							for (var i = 0, len = obj.length; i < len; i++){  
								ret.push(obj2Str(obj[i]));  
							}  
							return '[' + ret.join(',') + ']';  
							}  
							else if (obj instanceof RegExp){  
							return obj.toString();  
							}  
							else{  
							for (var a in obj){  
								ret.push(a + ':' + post_datas.obj2Str(obj[a]));  
							}  
							return '{' + ret.join(',') + '}';  
							}  
						case 'function':  
							return 'function() {}';  
						case 'number':  
							return obj.toString();  
						case 'string':  
							return "\"" + obj.replace(/(\\|\")/g, "\\$1").replace(/\n|\r|\t/g, function(a) {return ("\n"==a)?"\\n":("\r"==a)?"\\r":("\t"==a)?"\\t":"";}) + "\"";  
						case 'boolean':  
							return obj.toString();  
						default:  
							return obj.toString();  
						}  
				}  
				
		};
        //////////////////////////////////////////////////////////////////////////////////
        // PUBLIC FUNCTIONS
        var methods = {
				getData: function() { 
									var datavar = "";
									alert(3+methods.getStep());
									switch(methods.getStep()){
										case 0:
											
											datavar = post_datas.post_step1();
											break;
										case 1:
											datavar = post_datas.post_step2();
											break;
										case 2:
											datavar = post_datas.post_step3();
											break;
										default:
											break;
									}
									return datavar;
				},
                getStep: function( ) { return self.data('steps')['step']; },
                start:   function( ) { 
					alert($("#prev").val());
					$("#prev").attr("disabled","disabled");
					htmlobj=$.ajax({url:stack[0],async:false});
					 $("#ajax_page").html(htmlobj.responseText);
					return methods.setStep(0); },
                finish:  function( ) { 
                    var l = self.find('ul li').length;
                    methods.setStep(l);
                    self.data('steps')['step'] = l; 
                    return l;
                },
                prev:    function( ) {
					$("#next").removeAttr("disabled")
					if ( methods.getStep() == 0 )
					{
						$("#prev").attr("disabled","disabled");
						return methods.getStep();
					}else{
                    var step = methods.getStep();
                    var l    = self.find('ul li').length;
                    if(step == l) step = step-1;
					//alert(stack[methods.getStep()]);

					  htmlobj=$.ajax({type: 'POST',url:stack[methods.getStep()-1],data:methods.getData(),async:false});
					  $("#ajax_page").html(htmlobj.responseText);
                    return methods.setStep(step - 1);
					}
                },
                next:    function() {
					$("#prev").removeAttr("disabled");
					/**
					$.post(stack[methods.getStep()+1],function(data, status){
						$("#ajax_page").html(data);
						return false; 
					});
					**/
					
					//alert(stack.size);
					if ( methods.getStep() == 2)
					{
						$("#next").attr("disabled","disabled");
						return methods.getStep();
					}else{
					  //alert(stack[methods.getStep()+1]);
					  //alert(post_datas.obj2Str(methods.getData()))
					  htmlobj=$.ajax({type: 'POST',url:stack[methods.getStep()+1],data:{methods.getData()},async:false});
					  $("#ajax_page").html(htmlobj.responseText);
                    return methods.setStep(methods.getStep() + 1);
					}
                },
                setStep: function( stepNumber ) {  
                    // Sets the step number
                    var l = self.find('ul li').length;
                    if(stepNumber < 0) stepNumber = 0;
                    if(stepNumber > l) stepNumber = l;
                    
                    // Resets styles
                    self.find('ul li').removeClass('current completed completedLast last end completedLastEnd');

                    // Styles for intermediate steps
                    self.find('ul li:lt(' + ((stepNumber < l) ? stepNumber : l-1) + ')').addClass('completed');

                    if(stepNumber > 0 && stepNumber < l) 
                        self.find('ul li:nth(' + (stepNumber-1) + ')').addClass('completedLast');
                    if(stepNumber < l)
                        self.find('ul li:nth(' + stepNumber + ')').addClass('current');

                    // Last step style
                    if(stepNumber == l)  
                        self.find('ul li:last').addClass('completedLastEnd');
                    //if(stepNumber == l-1)  
                    //    self.find('ul li:last').addClass('currentEnd');
                    else 
                        self.find('ul li:last').addClass('end');
                    
                    self.data('steps')['step'] = stepNumber; 
                    return stepNumber;
                }
                
        };
        /////////////////////////////////////////////////////////////////////////////////////
        // Decides what to do
        if ( methods[options] ) {
            return methods[options].apply( self, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof options === 'object' || ! options ) {
            return init.apply( self, arguments );
        } else {
            //$.error( 'Method ' +  options + ' does not exist on jQuery.tooltip' );
            return init.apply( self, {} );
        }    
                
    };
})( jQuery );

var stack={0:'step1/',1:'step2/',2:'step3/'}

$(document).ready(function() {
    $('.steps').steps();
});


$(document).ready(function() { $('.steps').steps('start') });
$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});