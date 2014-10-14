/*
 * base.js
 * 1. handle base template
 * 2. handle whole front-end templates routing
 * 
 * */
'use strict';

// Declare app level module which depends on filters, and services, and modify $interpolateProvider to avoid the conflict with jinja2' symbol
var my_app = angular.module('my_app', [ 'angular-responsive', 'ui.router', 'myGpsDataDirective' ], function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
});

// global values
my_app.value('GLOBAL_VALUES',{
	EMAIL : 'gogistics@gogistics-tw.com'
});

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
		controller: 'indexPageDispatchCtrl'
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
// ng-functions mapper
my_app
.controller('frontPageDispatchCtrl', frontPageDispatcheController)
.controller('indexPageDispatchCtrl', indexPageDispatcheController)
.controller('myIndexCtrl', myIndexController);

// functions
frontPageDispatcheController.$injector = ['$state', '$scope', 'GLOBAL_VALUES'];
function frontPageDispatcheController($state, $scope, GLOBAL_VALUES) {
	$scope.email = GLOBAL_VALUES.EMAIL;
    $state.transitionTo('front_page');
}

indexPageDispatcheController.$injector = ['$state'];
function indexPageDispatcheController($state) {
    $state.transitionTo('index_1');
}

myIndexController.$injector = ['$scope', 'GLOBAL_VALUES'];
function myIndexController($scope, GLOBAL_VALUES) {
	$scope.email = GLOBAL_VALUES.EMAIL;
	
	$scope.select_topic = function(section) {
        $scope.selected = section;
    }

    $scope.is_selected = function(section) {
        return ($scope.selected === section);
    }
	
    // init selected topic
    $scope.select_topic('index_1');
}