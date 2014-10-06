'use strict';

// Declare app level module which depends on filters, and services
var my_app = angular.module('my_app', [ 'angular-responsive', 'ui.router' ]);

// routing configuration
my_app.config(function(responsiveHelperProvider, $stateProvider, $urlRouterProvider) {

	// templates dispatcher which redirect visitors to appropriate templates;
	// currently, there are desktop and mobile versions
	var device = 'desktop';
	var responsiveHelper = responsiveHelperProvider.$get();
	if (responsiveHelper.isMobile()) {
		device = 'mobile';
	}
	
	// nested templates and routing
	$urlRouterProvider.otherwise('/');
	
	$stateProvider
	.state('home', {
		templateUrl: '/ng_templates/template_home.html',
	})
	.state('front_page', {
		url: '/',
		parent: 'home',
		templateUrl: '/ng_templates/' + device + '/front_page.html'
	})
	.state('index_page', {
		url: '/index',
		parent: 'home',
		templateUrl: '/ng_templates/' + device + '/index.html',
		controller: 'index_page_ctrl'
	})
	.state('index_1', {
		url: '/index_1',
		parent: 'index_page',
		templateUrl: '/ng_templates/' + device + '/index_1.html',
	})
	.state('index_2', {
		url: '/index_2',
		parent: 'index_page',
		templateUrl: '/ng_templates/' + device + '/index_2.html',
	});
	
});

/* controllers */
//show default front page
my_app.controller('front_page_ctrl', function ($state) {
      $state.transitionTo('front_page');
    });

my_app.controller('index_page_ctrl', function ($state) {
    $state.transitionTo('index_1');
  });




function myController($scope) {
	$scope.email = 'gogistics@gogistics-tw.com';
	
	$scope.select_topic = function(section) {
        $scope.selected = section;
    }

    $scope.is_selected = function(section) {
        return ($scope.selected === section);
    }
	
    // init selected topic
    $scope.select_topic('index_1');
}