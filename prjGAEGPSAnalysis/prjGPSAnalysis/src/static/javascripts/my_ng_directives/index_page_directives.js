//directives
angular.module('myGpsDataDirective', []).directive('myIndexGpsData', function(){
	return {
		restrict: 'E',
		scope: {},
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
         });
			element.bind('mouseleave', function () {
             element.css({'font-weight': '100'});
         });
			
		}
	};
});