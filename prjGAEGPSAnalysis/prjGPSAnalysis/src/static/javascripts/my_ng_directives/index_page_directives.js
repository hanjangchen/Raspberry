//directives
angular.module('myGpsDataDirective', []).directive('myIndexGpsData', function(){
	return {
		restrict: 'EA',
		scope: {
			my_data: '='
		},
		transclude: true,
		templateUrl: '/ng_templates/shared/gps_data.html',
		controller: function($scope){
			
		},
		link: function(scope, element, attrs){
			 scope.gpsData = 'gpsData';
			element.bind('click', function () {
             element.html('You clicked me!');
         });
			element.bind('mouseenter', function () {
             element.css({'font-weight': 'bold'});
 			 alert(scope.my_data);
         });
			element.bind('mouseleave', function () {
             element.css({'font-weight': '100'});
         });
			
		}
	};
});