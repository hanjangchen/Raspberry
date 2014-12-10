/* shcedule data from google spradsheet */
spreadsheet_data = {};
spreadsheet_data_years = [];
$
		.getJSON(
				"https://spreadsheets.google.com/feeds/list/1SWwXdVpeFWi1cHcF5sUHj47qXunqCo5i1D2jeGhzHaE/od6/public/values?alt=json-in-script&callback=?",
				function(data) {
					$
							.each(
									data.feed.entry,
									function(i, entry) {
										var datetime = entry.gsx$datetime.$t;
										var date = new Date(datetime);
										var year = date.getFullYear();
										var month = (1 + date.getMonth())
												.toString();
										month = month.length > 1 ? month : '0'
												+ month;
										var day = date.getDate().toString();
										day = day.length > 1 ? day : '0' + day;
										datetime = month + "/" + day + "/"
												+ year;
										var year = entry.gsx$datetime.$t
												.slice(entry.gsx$datetime.$t
														.lastIndexOf("/") + 1);
										year = Number(year);
										//
										if (spreadsheet_data_years
												.indexOf(year) === -1) {
											spreadsheet_data_years.push(year);
										}

										//
										if (!(datetime in spreadsheet_data)) {
											spreadsheet_data[datetime] = {};
											spreadsheet_data[datetime]['count'] = 1;
											spreadsheet_data[datetime]['detail'] = [ "Schedule => "
													+ entry.gsx$schedule.$t
													+ " ; Owners => "
													+ entry.gsx$owners.$t
													+ " ; Status => "
													+ entry.gsx$status.$t ];
										} else {
											spreadsheet_data[datetime]['count'] += 1;
											spreadsheet_data[datetime]['detail']
													.push("Schedule => "
															+ entry.gsx$schedule.$t
															+ " ; Owners => "
															+ entry.gsx$owners.$t
															+ " ; Status => "
															+ entry.gsx$status.$t);
										}

										// console.log("Datetime-" +
										// entry.gsx$datetime.$t + " ;
										// Schedule-" + entry.gsx$schedule.$t);
									});
				})
		.then(
				function() {
					/* project calendar */
					var width = 990, height = 145, cellSize = 17; // cell size

					var day = d3.time.format("%w"), week = d3.time.format("%U"), current_month = d3.time
							.format("%m"), percent = d3.format(".1%"), format = d3.time
							.format("%m/%d/%Y");

					var color = d3.scale.quantize().domain([ 0, 5 ]).range(
							d3.range(11).map(function(d) {
								return "q" + d + "-11";
							}));

					var svg = d3.select("#project_calendar").selectAll("svg")
							.data(spreadsheet_data_years).enter().append("svg")
							.attr("width", width).attr("height", height).attr(
									"class", "RdYlGn").append("g").attr(
									"transform",
									"translate("
											+ ((width - cellSize * 53) / 2)
											+ "," + (height - cellSize * 7 - 1)
											+ ")");

					svg.append("text").attr("transform",
							"translate(-30," + cellSize * 3.5 + ")rotate(-90)")
							.style("text-anchor", "middle").text(function(d) {
								return d;
							});

					// not done yet
					var months = [], months_index = [], years = [ 2010, 2009 ], days = [
							"Su", "Mo", "Tu", "We", "Th", "Fr", "Sa" ];
					svg.selectAll(".month_text").data(
							function(d) {
								return d3.time.days(new Date(d, 0, 1),
										new Date(d + 1, 0, 1));
							}).enter().append("text").attr("class",
							"month_text").attr("x", function(d) {
						if (months_index.indexOf(current_month(d)) === -1) {
							return week(d) * cellSize
						}
						;
						if (months_index.length === 12) {
							months_index = []
						}
					}).attr("y", -5).text(function(d) {
						if (months.indexOf(current_month(d)) === -1) {
							months.push(current_month(d));
							return current_month(d)
						}
						;
						if (months.length === 12) {
							months = []
						}
					});
					svg.selectAll(".wday").data([ 0, 1, 2, 3, 4, 5, 6 ])
							.enter().append("text").attr("class", "wday")
							.style("text-anchor", "middle").attr("x", -12)
							.attr("y", function(d) {
								return (d + 1) * 17 - 6
							}).text(function(d) {
								return days[d]
							});
					// not done yet

					var rect = svg.selectAll(".day").data(
							function(d) {
								return d3.time.days(new Date(d, 0, 1),
										new Date(d + 1, 0, 1));
							}).enter().append("rect").attr("class", "day")
							.attr("width", cellSize).attr("height", cellSize)
							.attr("x", function(d) {
								return week(d) * cellSize;
							}).attr("y", function(d) {
								return day(d) * cellSize;
							}).datum(format).on("mouseover", mouseover).on(
									"mouseup", mouseup);

					rect.append("title").text(function(d) {
						return d;
					});

					svg.selectAll(".month").data(
							function(d) {
								return d3.time.months(new Date(d, 0, 1),
										new Date(d + 1, 0, 1));
							}).enter().append("path").attr("class", "month")
							.attr("d", monthPath);

					var data = spreadsheet_data;
					rect.filter(function(d) {
						return d in data;
					}).attr("class", function(d) {
						return "day " + color(data[d]['count']);
					}).select("title").text(
							function(d) {
								return "DateTime- " + d + " ; there is/are "
										+ data[d]['count']
										+ " thing(s) should be done today!";
							});

					function monthPath(t0) {
						var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1,
								0), d0 = +day(t0), w0 = +week(t0), d1 = +day(t1), w1 = +week(t1);
						return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
								+ "H" + w0 * cellSize + "V" + 7 * cellSize
								+ "H" + w1 * cellSize + "V" + (d1 + 1)
								* cellSize + "H" + (w1 + 1) * cellSize + "V"
								+ 0 + "H" + (w0 + 1) * cellSize + "Z";
					}

					// mouse events;
					function mouseover(d, i) {
						// alert(d);
					}

					function mouseup(d, i) {
						try {

							if (data[d]['detail'] !== undefined) {
								$("#project_daily_schedule").empty();

								for ( var item in data[d]['detail']) {
									$("#project_daily_schedule").append(
											"<span class='intro_content'>*Date-"
													+ d + " ; "
													+ data[d]['detail'][item]
													+ "</span><br>");
								}
							} else {
								alert("No Schedule is on the selected day!");
							}
						} catch (e) {
							console.log(e);
						}
					}

				});
// end of mouse events



// https://docs.google.com/spreadsheets/d/1SWwXdVpeFWi1cHcF5sUHj47qXunqCo5i1D2jeGhzHaE/pubhtml?gid=0&single=true ; spreadsheet on Gogistics Cloud
/* $.getJSON(
				"https://www.google.com/calendar/feeds/gogistics%40gogistics-tw.com/public/basic?alt=json-in-script&callback=listEvents",

				function(data) {
					$.each(data.feed.entry, function(i, entry) {
						// console.log(entry.content.$t);
						console.log(entry);
					});
				});

function listEvents(root) {
	var feed = root.feed;
	var entries = feed.entry || [];
	var html = [ '<ul>' ];

	for ( var i = 0; i < entries.length; ++i) {
		var entry = entries[i];
		var title = (entry.title.type == 'html') ? entry.title.$t
				: escape(entry.title.$t);
		var start = (entry['gd$when']) ? entry['gd$when'][0].startTime : "";

		html.push('<li>', start, ' ', title, '</li>');
	}

	html.push('</ul>');
	document.getElementById("agenda").innerHTML = html.join("");
} */

// <script type="text/javascript" src="https://www.google.com/calendar/feeds/gogistics%40gogistics-tw.com/public/basic?alt=json-in-script&callback=listEvents"></script>

