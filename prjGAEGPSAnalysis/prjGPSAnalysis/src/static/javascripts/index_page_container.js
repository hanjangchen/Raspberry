/*
 * base.js
 * 1. handle base template
 * 2. handle whole front-end templates routing
 * 
 * */
'use strict';
var index_page_app, device;
(function() {
	// Angular.js
	// declare app level module which depends on filters, and services, and
	// modify $interpolateProvider to avoid the conflict with jinja2' symbol
	index_page_app = angular.module('index_page_app', [ 'angular-responsive',
			'ui.router', 'myGpsDataDirective',
			'myIndexAdminImagesUploadDirective' ], function(
			$interpolateProvider) {
		$interpolateProvider.startSymbol('[[');
		$interpolateProvider.endSymbol(']]');
	});

	// global values
	index_page_app.value('GLOBAL_VALUES', {
		EMAIL : 'gogistics@gogistics-tw.com',
		URL_UPLOAD_IMAGE_TO_BLOB : data_backend.upload_url,
	});

	// app-routing configuration
	index_page_app.config(function(responsiveHelperProvider, $stateProvider,
			$urlRouterProvider) {
		// templates dispatcher which redirect visitors to appropriate
		// templates;
		// currently, there are desktop and mobile versions
		device = 'desktop';
		var responsiveHelper = responsiveHelperProvider.$get();
		if (responsiveHelper.isMobile()) {
			device = 'mobile';
		} else if (responsiveHelper.isTablet()) {
			device = 'tablet';
		}

		// nested templates and routing
		$stateProvider.state('home', {
			templateUrl : '/ng_templates/my_ng_template_base.html',
		}).state('index_page', {
			parent : 'home',
			templateUrl : '/ng_templates/' + device + '/index.html',
			controller : 'indexPageDispatchCtrl'
		}).state(
				'index_introduction',
				{
					url : '/index_introduction',
					parent : 'index_page',
					templateUrl : '/ng_templates/' + device
							+ '/index_introduction.html',
				}).state(
				'index_data_analysis',
				{
					url : '/index_data_analysis',
					parent : 'index_page',
					templateUrl : '/ng_templates/' + device
							+ '/index_data_analysis.html',
				});

		$urlRouterProvider.otherwise('/index_introduction'); // for defualt
																// state
																// routing; for
																// current
																// routing
																// mechanism,
																// it's not
																// necessary

	});

	/* controllers */
	// for routing to default content on index page
	var indexPageDispatchController = function($state, $scope, GLOBAL_VALUES) {
		$scope.email = GLOBAL_VALUES.EMAIL;
		console.log($state.current.name);

		if ($state.current.name !== 'index_introduction') {
			$state.transitionTo('index_introduction');
		}
	}
	indexPageDispatchController.$inject = [ '$state', '$scope', 'GLOBAL_VALUES' ];

	// page controllers
	var myIndexController = function($scope, GLOBAL_VALUES) {
		$scope.email = GLOBAL_VALUES.EMAIL;

		$scope.select_topic = function(section) {
			$scope.selected = section;
		}

		$scope.is_selected = function(section) {
			return ($scope.selected === section);
		}

		// init selected topic
		$scope.select_topic('index_introduction');
	}
	myIndexController.$inject = [ '$scope', 'GLOBAL_VALUES' ];

	index_page_app.controller('indexPageDispatchCtrl',
			indexPageDispatchController).controller('myIndexCtrl',
			myIndexController);

	// ng-services of index_data_analysis
	var indexTwoService = function($http, GLOBAL_VALUES) {
		this.upload_imgs = function(arg_data) {
			// upload images
			console.log(arg_data);
		}

		this.dowload_imgs_detail = function() {
			var data = {
				'key' : 'ergr425t45gSVDTtrhrthrethT56h'
			};
			return $http.post('/data_retrieving/download_img', data, {
				withCredentials : true,
				headers : {
					'Content-Type' : undefined
				},
				transformRequest : angular.identity
			})
		};
	}
	indexTwoService.$inject = [ '$http', 'GLOBAL_VALUES' ];
	index_page_app.service('myIndexTwoService', indexTwoService);

	// ng-controllers of index_data_analysis
	var indexTwoController = function(myIndexTwoService, GLOBAL_VALUES, $scope) {
		// images data for uploading to blobstore
		$scope.images_data_to_upload = 'data analysis';

		// upload images
		var upload_img_to_blobstore = function() {
			myIndexTwoService.upload_imgs('hello data analysis');
		};
		this.upload_img_to_blobstore = upload_img_to_blobstore;

	}
	indexTwoController.$inject = [ 'myIndexTwoService', 'GLOBAL_VALUES',
			'$scope' ];
	index_page_app.controller('myIndexTwoCtrl', indexTwoController);

	//
	var indexImagesDetailListController = function(myIndexTwoService,
			GLOBAL_VALUES, $scope) {
		//
		var download_imgs_detail = function() {
			var imgs_detail;
			myIndexTwoService.dowload_imgs_detail().success(function(response) {
				imgs_detail = response.imgs_detail_entities;
				console.log(imgs_detail);
			}).error(function(response) {
				console.log('fail to download images detail');
			});
		}
		this.download_imgs_detail = download_imgs_detail;
		this.download_imgs_detail();
	}
	indexImagesDetailListController.$inject = [ 'myIndexTwoService',
			'GLOBAL_VALUES', '$scope' ];
	index_page_app.controller('indexImagesDetailListCtrl',
			indexImagesDetailListController);

	/* JQuery */

})();