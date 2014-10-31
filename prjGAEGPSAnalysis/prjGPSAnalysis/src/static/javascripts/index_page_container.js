/*
 * base.js
 * 1. handle base template
 * 2. handle whole front-end templates routing
 * 
 * */
'use strict';

(function(){
	// Angular.js
	// declare app level module which depends on filters, and services, and modify $interpolateProvider to avoid the conflict with jinja2' symbol
	var index_page_app = angular.module('index_page_app', [ 'angular-responsive', 'ui.router', 'myGpsDataDirective' ], function($interpolateProvider) {
		$interpolateProvider.startSymbol('[[');
		$interpolateProvider.endSymbol(']]');
	});

	// global values
	index_page_app.value('GLOBAL_VALUES',{
		EMAIL : 'gogistics@gogistics-tw.com'
	});

	// app-routing configuration
	index_page_app.config(function(responsiveHelperProvider, $stateProvider, $urlRouterProvider) {
		// templates dispatcher which redirect visitors to appropriate templates;
		// currently, there are desktop and mobile versions
		var device = 'desktop';
		var responsiveHelper = responsiveHelperProvider.$get();
		if (responsiveHelper.isMobile()) {
			device = 'mobile';
		}
		else if(responsiveHelper.isTablet()){
			device = 'tablet';
		}
		
		// nested templates and routing
		$stateProvider
		.state('home', {
			templateUrl: '/ng_templates/template_home.html',
		})
		.state('index_page', {
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

		$urlRouterProvider.otherwise('/index_1'); // for defualt state routing; for current routing mechanism, it's not necessary
		
	});

	/* controllers */
	// for routing to default content on index page
	var indexPageDispatchController = function ($state, $scope, GLOBAL_VALUES) {
		$scope.email = GLOBAL_VALUES.EMAIL;
		console.log($state.current.name);
		
		if($state.current.name !== 'index_1'){
		    $state.transitionTo('index_1');
		}
	}
	indexPageDispatchController.$injector = ['$state', '$scope', 'GLOBAL_VALUES'];

	// page controllers
	var myIndexController = function ($scope, GLOBAL_VALUES) {
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
	myIndexController.$injector = ['$scope', 'GLOBAL_VALUES'];

	// ng-functions mapper
	index_page_app
	.controller('indexPageDispatchCtrl', indexPageDispatchController)
	.controller('myIndexCtrl', myIndexController);
	
	/* JQuery */
	
})();