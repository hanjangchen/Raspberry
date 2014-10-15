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
	// $urlRouterProvider.otherwise('/front_page'); // for defualt state routing; for current routing mechanism, it's not necessary
	
	$stateProvider
	.state('home', {
		templateUrl: '/ng_templates/template_home.html',
	})
	.state('front_page', {
		url: '/front_page',
		parent: 'home',
		templateUrl: '/ng_templates/' + device + '/front_page.html'
	})
	.state('index_page', {
		url: '/index_page',
		parent: 'home',
		templateUrl: '/ng_templates/' + device + '/index.html'
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
.controller('frontPageDispatchCtrl', frontPageDispatchController)
.controller('indexPageDispatchCtrl', indexPageDispatchController)
.controller('myIndexCtrl', myIndexController);

// functions
// dispatch controllers are used for building the connection between jinja templates and ng templates
frontPageDispatchController.$injector = ['$state', '$scope', 'GLOBAL_VALUES'];
function frontPageDispatchController($state, $scope, GLOBAL_VALUES) {
	$scope.email = GLOBAL_VALUES.EMAIL;
    $state.transitionTo('front_page');
}

indexPageDispatchController.$injector = ['$state', '$scope', 'GLOBAL_VALUES'];
function indexPageDispatchController($state, $scope, GLOBAL_VALUES) {
	$scope.email = GLOBAL_VALUES.EMAIL;
    $state.transitionTo('index_1');
}

// page controllers
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