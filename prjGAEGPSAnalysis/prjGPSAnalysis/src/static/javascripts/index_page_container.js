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
	var injected_module = [];
	if (is_admin) {
		injected_module = [ 'angular-responsive', 'ui.router',
				'myGpsDataDirective', 'myIndexAdminImagesUploadDirective','ngAnimate' ];
	} else {
		injected_module = [ 'angular-responsive', 'ui.router',
				'myGpsDataDirective', 'ngAnimate' ];
	}
	
	// modify interpolateProvide to avoid the interpolating collision to jinja
	index_page_app = angular.module('index_page_app', injected_module,
			function($interpolateProvider) {
				$interpolateProvider.startSymbol('[[');
				$interpolateProvider.endSymbol(']]');
			});

	// global values
	index_page_app.value('GLOBAL_VALUES', {
		EMAIL : 'gogistics@gogistics-tw.com',
		URL_UPLOAD_IMAGE_TO_BLOB : hubOfIndexPageContainer.upload_url,
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

		// nested templates routing
		$stateProvider.state('home', {
			templateUrl : '/ng_templates/my_ng_template_base.html',
		}).state('index_page', {
			parent : 'home',
			templateUrl : '/ng_templates/' + device + '/index/index.html',
			controller : 'indexPageDispatchCtrl'
		}).state(
				'index_introduction',
				{
					url : '/index_introduction',
					parent : 'index_page',
					templateUrl : '/ng_templates/' + device
							+ '/index/index_introduction.html',
				}).state(
				'index_data_analysis',
				{
					url : '/index_data_analysis',
					parent : 'index_page',
					templateUrl : '/ng_templates/' + device
							+ '/data_analysis/data_analysis.html',
				}).state(
						'particle_swarm_optimization',
						{
							url : '/particle_swarm_optimization',
							parent : 'index_page',
							templateUrl : '/ng_templates/' + device
									+ '/tutorials/particle_swarm_optimization_animation.html',
						});

	});

	
	/* controllers */
	// for routing to default content on index page
	var indexPageDispatchController = function($state, $scope, GLOBAL_VALUES) {
		// set values
		$scope.email = GLOBAL_VALUES.EMAIL;
		$scope.topics_keywords = ["Plans",
		                          "Project Calendar",
		                          "Github Repositories",
		                          "Contributors Profile",
		                          "Raspberry PI",
		                          "Arduino",
		                          "Google App Engine",
		                          "Google Compute Engine",
		                          "Google Container Engine",
		                          "Google Datastore",
		                          "Google Blobstore",
		                          "Google Drive",
		                          "MongoDB",
		                          "Python",
		                          "Javascript",
		                          "OpenStreetMap",
		                          "Google Map",
		                          "Angularjs",
		                          "jQuery",
		                          "Bootstrap",
		                          "Leaflet.js",
		                          "Numeric.js",
		                          "D3.js",
		                          "Particle Swarm Optimization",
		                          "Neural Network"];
		
		$scope.dict_topics_keywords = {"Plans" : "plans",
				                       "Project Calendar" : "project_calendar",
									   "Github Repositories" : "github_repositories",
									   "Contributors Profile" : "contributors_profile",
									   "Raspberry PI" : "raspberry_pi",
									   "Arduino" : "arduino",
									   "Google App Engine" : "google_app_engine",
									   "Google Compute Engine" : "google_compute_engine",
									   "Google Container Engine" : "google_container_engine",
									   "Google Datastore" : "google_datastore",
									   "Google Blobstore" : "google_blobstore",
									   "Google Drive" : "google_drive",
									   "MongoDB" : "mongodb",
									   "Python" : "python",
									   "Javascript" : "javascript",
									   "OpenStreetMap" : "openstreetmap",
									   "Google Map" : "google_map",
									   "Angularjs" : "angular",
									   "jQuery" : "jquery",
									   "Bootstrap" : "bootstrap",
									   "Leaflet.js" : "leaflet",
									   "Numeric.js" : "numeric",
									   "D3.js" : "d3",
									   "Particle Swarm Optimization" : "particle_swarm_optimization",
									   "Neural Network" : "neural_network"};
		
		
		// init page
		var selected_template = $state.current.name;
		if($state.current.name !== ''){
			$state.transitionTo(selected_template);
		}
		else{
		    $state.transitionTo('index_introduction');
		};
		$scope.selected = selected_template; // highlight selected topic
		
		// scroll to search field
		$scope.scroll_to_top = function(){
			$("body, html").animate({
						scrollTop : $("#search_field").offset().top - 300}, 1500);
		};
	}
	indexPageDispatchController.$inject = [ '$state', '$scope', 'GLOBAL_VALUES' ];
	index_page_app.controller('indexPageDispatchCtrl', indexPageDispatchController);
	// end of indexDispatchController
	

	// index page controllers
	var myIndexController = function($state, $scope, $timeout, GLOBAL_VALUES) {
		$scope.email = GLOBAL_VALUES.EMAIL;
		
		// select topic
		var selected_template = $state.current.name, isVisited = false;

		// selected topic
		$scope.select_topic = function(section) {
			$scope.selected = section;
			if ($('#list_icon').is(":visible")) {
				
				//
				if(!isVisited){
					isVisited = true;
				}else{
					$(".navbar-collapse").collapse('hide');
				}
				
				// toggle topic content
				$timeout(function(){
					$state.transitionTo(section);
				}, 1000);
			}
		}

		//
		$scope.is_selected = function(section) {
			return ($scope.selected === section);
		}
		
		//
		$scope.toggle_topic_list = function(){
			if ($('#list_icon').is(":visible")) {
				$(".navbar-collapse").collapse('hide');
			}
		}
	}
	myIndexController.$inject = ['$state', '$scope', '$timeout', 'GLOBAL_VALUES' ];
	index_page_app.controller('myIndexCtrl', myIndexController);
	// end of index page controllers
	
	// auto-complete field
	index_page_app.directive('autoComplete', function($timeout) {
	    return function(scope, iElement, iAttrs) {
	            iElement.autocomplete({
	                source: scope[iAttrs.uiItems],
	                select: function() {
	                    $timeout(function() {
	                      iElement.trigger('input');
	                      
	                      // keyword searching mechanism
	                      try {
								var elemId = scope.dict_topics_keywords[scope.searched_keyword];
								$('html, body').animate(
												{
													scrollTop : $("#" + elemId).offset().top - 200
												}, 800);
							} catch (e) {
								console.log('Error: ' + e);
							}
	                    }, 0);
	                }
	            });
	    };
	});
	// end of auto-complete field

	
	// ng-services of index_data_analysis
	var indexDataAnalysisService = function($http, GLOBAL_VALUES) {
		// upload imgs
		this.upload_imgs = function(arg_data) {
			console.log(arg_data);
		}

		// download imgs
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
			});
		};
	}
	indexDataAnalysisService.$inject = [ '$http', 'GLOBAL_VALUES' ];
	index_page_app.service('myIndexDataAnalysisService',
			indexDataAnalysisService);
	// end of ng-services of index_data_analysis

	
	// index (not done)
	var indexImagesInformationUploadController = function() {

	}

	
	/* index page images list controller; better to categorize lists */
	var indexImagesDetailListController = function(myIndexDataAnalysisService,
			GLOBAL_VALUES, $scope) {
		// upload images information
		$scope.images_data_to_upload = 'data analysis';

		// upload images
		var upload_img_to_blobstore = function() {
			myIndexDataAnalysisService.upload_imgs('hello data analysis');
		};
		this.upload_img_to_blobstore = upload_img_to_blobstore;

		// download images details
		var current_obj = this;
		current_obj.imgs_detail = [];

		var download_imgs_detail = function() {
			myIndexDataAnalysisService
					.dowload_imgs_detail()
					.success(
							function(response) {
								console.log(JSON.stringify(response, 2, 2));
								current_obj.imgs_detail = response.imgs_detail_entities;
							}).error(function(response) {
						console.log('fail to download images detail');
					});
		}
		download_imgs_detail();
		console.log(JSON.stringify(current_obj.imgs_detail, 2, 2));

		// ng-pagination
		$scope.currentPage = 1;
		$scope.pageSize = 1;
		// end of ng-pagination
	}
	indexImagesDetailListController.$inject = [ 'myIndexDataAnalysisService',
			'GLOBAL_VALUES', '$scope' ];
	index_page_app.controller('indexImagesDetailListCtrl',
			indexImagesDetailListController);

	// pagination controller for images list
	var indexImagesDetailListPaginationController = function($scope) {
		$scope.pageChangeHandler = function(num) {
			console.log('page changed to ' + num);
		};
	}
	indexImagesDetailListPaginationController.$inject = [ '$scope' ];
	index_page_app.controller('indexImagesDetailListPaginationCtrl',
			indexImagesDetailListPaginationController);
	/* end of index page images list controller */

	
	/* index page data visualization chart */
	var indexDataAnalysisListController = function(myIndexDataAnalysisService,
			GLOBAL_VALUES, $scope) {
		// set data array
		var current_obj = this;
		current_obj.data_ary = [];
		if(data_set_ary.length > 0){
			current_obj.data_ary = data_set_ary;
		}
		// data for testing
		
		/*current_obj.data_ary = [
		 {'id' : 'DATA-0','sub_time' : '', 'sub_model': '',
		 'sub_date' : '', 'sub_data' : [{'date' : '2014-11-1_09-12-2',
		 'sensor' : '53'},{'date' : '2014-11-1_09-12-23', 'sensor' :
		 '19'},{'date' : '2014-11-1_09-12-25', 'sensor' : '24'}]},
		 {'id' : 'DATA-1','sub_time' : '', 'sub_model': '', 'sub_date' : '', 'sub_data' : [{'date' : '2014-11-1_09-12-2', 'sensor' : '23'},{'date' :
		 '2014-11-1_09-12-23', 'sensor' : '29'},{'date' :
		 '2014-11-1_09-12-25', 'sensor' : '24'}]},
		 {'id' : 'DATA-2', 'sub_time' : '','sub_model': '', 'sub_date' : '', 'sub_data' : [{'date' :
		 '2014-11-1_09-12-2', 'sensor' : -83},{'date' : '2014-11-1_09-12-23',
		 'sensor' : -49},{'date' : '2014-11-1_09-12-25', 'sensor' : -74}]}];*/
		 
		 current_obj.visulaize_data = function(arg_id, arg_data_set) {
			var elem_id = '#' + arg_id;
			if ( $(elem_id).children().length > 0 ) {
				alert('Chart already exists!');
			     return false;
			}
			// device size
			var device_width = screen.width;
			var device_height = screen.height;
			var min_val = Math.min(device_width, device_height);
			var chart_width, chart_height, xAxis_format;
			if (min_val <= 767) {
				chart_width = 275;
				chart_height = 130;
				xAxis_format = "%H:%M"; // the format is not correct and should change
			} else {
				chart_width = 960;
				chart_height = 500;
				xAxis_format = "%X"; // the format is not correct and should change
			}

			// basic setting
			var margin = {
				top : 10,
				right : 50,
				bottom : 50,
				left : 30
			}, width = chart_width - margin.left - margin.right, height = chart_height
					- margin.top - margin.bottom;

			var parseDate = d3.time.format("%Y%m%d").parse;
			var parseDateTime = d3.time.format("%Y-%m-%d_%H-%M-%S").parse;

			var x = d3.time.scale().range([ 0, width ]);

			var y = d3.scale.linear().range([ height, 0 ]);

			var color = d3.scale.category10();

			var xAxis = d3.svg.axis().scale(x).ticks(d3.time.minute, 60)
					.tickFormat(d3.time.format(xAxis_format)).orient("bottom");

			var yAxis = d3.svg.axis().scale(y).ticks(6).orient("left");

			var line = d3.svg.line().interpolate("basis").x(function(d) {
				return x(d.date);
			}).y(function(d) {
				return y(d.temperature);
			});

			var svg = d3.select("[id='" + arg_id + "']").append("svg").attr("width",
					width + margin.left + margin.right).attr("height",
					height + margin.top + margin.bottom).append("g").attr(
					"transform",
					"translate(" + margin.left + "," + margin.top + ")");

			//
			function make_x_axis(){
				return d3.svg.axis().scale(x).orient("bottom").ticks(5);
			}
			
			//
			function make_y_axis(){
				return d3.svg.axis().scale(y).orient("left").ticks(5);
			}
			
			var data = arg_data_set[0][0];
			color.domain(d3.keys(data[0]).filter(function(key) {
				return key !== "date";
			}));

			try {
				data.forEach(function(d) {
					d.date = +parseDateTime(d.date);
				});
			} catch (e) {
				console.log(e);
			}
			// console.log(JSON.stringify(data, 2, 2));

			var cities = color.domain().map(function(name) {
				return {
					name : name,
					values : data.map(function(d) {
						return {
							date : d.date,
							temperature : +d[name]
						};
					})
				};
			});

			x.domain(d3.extent(data, function(d) {
				return d.date;
			}));

			y.domain([ d3.min(cities, function(c) {
				return d3.min(c.values, function(v) {
					return v.temperature;
				});
			}), d3.max(cities, function(c) {
				return d3.max(c.values, function(v) {
					return v.temperature;
				});
			}) ]);

			svg.append("g").attr("class", "x axis").attr("transform",
					"translate(0," + height + ")").call(xAxis);

			svg.append("g").attr("class", "y axis").call(yAxis).append("text")
					.attr("transform", "rotate(-90)").attr("y", -50).attr("dy",
							".8em").style("text-anchor", "end").text(
							"Temperature (ºF)");
			
			// draw grid lines
			svg.append("g").attr("class", "grid").attr("transform", "translate(0," + height + ")").call(make_x_axis().tickSize(-height, 0, 0).tickFormat(""));
			svg.append("g").attr("class", "grid").call(make_y_axis().tickSize(-width, 0, 0).tickFormat(""));
			// end of "draw grid lines"

			var city = svg.selectAll(".city").data(cities).enter().append("g")
					.attr("class", "city");

			city.append("path").attr("class", "line").attr("d", function(d) {
				return line(d.values);
			}).style("stroke", function(d) {
				return color(d.name);
			});

			city.append("text").datum(function(d) {
				return {
					name : d.name,
					value : d.values[d.values.length - 1]
				};
			}).attr(
					"transform",
					function(d) {
						return "translate(" + x(d.value.date) + ","
								+ y(d.value.temperature) + ")";
					}).attr("x", 3).attr("dy", ".35em").text(function(d) {
				return d.name;
			});
		}

		$scope.currentPage = 1;
		$scope.pageSize = 1;
	}
	indexDataAnalysisListController.$inject = [ 'myIndexDataAnalysisService',
			'GLOBAL_VALUES', '$scope' ];
	index_page_app.controller('indexDataAnalysisListCtrl',
			indexDataAnalysisListController);

	// pagination controller for images list
	var indexDataAnalysisListPaginationController = function($scope) {
		$scope.pageChangeHandler = function(num) {
			console.log('page changed to ' + num);
		};
	}
	indexDataAnalysisListPaginationController.$inject = [ '$scope' ];
	index_page_app.controller('indexDataAnalysisListPaginationCtrl',
			indexDataAnalysisListPaginationController);
	/* end of index page data visualization chart */

	/* JQuery */
})();