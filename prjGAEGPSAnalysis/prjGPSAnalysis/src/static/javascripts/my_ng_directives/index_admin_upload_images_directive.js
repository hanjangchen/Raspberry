//directives
angular.module('myIndexAdminImagesUploadDirective', []).directive('myIndexAdminImagesUpload', function(){
	return {
		restrict: 'E',
		scope: {},
		transclude: true,
		templateUrl: '/ng_templates/' + device + '/admin_images_upload.html',
		controller: function($scope){
		},
		link: function(scope, element, attrs){
			 scope.gpsData = 'Under Construction...';
		}
	};
});