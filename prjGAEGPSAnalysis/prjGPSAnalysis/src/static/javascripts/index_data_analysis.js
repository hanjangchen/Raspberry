(function() {
	/* JQuery */
	var ary_img_description = {};
	var has_images_to_upload = false;

	var input = document.getElementById("images_for_upload");
	var valid_files_ul = $("#valid_files_list");
	var invalid_files_ul = $("#invalid_files_list");
	
	$('#images_for_upload')
			.change(
					function() {
						//
						var toolarge = "";
						var maxsize = 1024000;

						//
						if (valid_files_ul.children().length > 0) {
							valid_files_ul.empty();
						}
						if (invalid_files_ul.children().length > 0) {
							invalid_files_ul.empty();
						}

						//
						for ( var i = 0; i < input.files.length; i++) {
							if (input.files[i].size > maxsize) {
								toolarge += input.files[i].name + "\n";
								invalid_files_ul.append("<li class='list-group-item'>" + input.files[i].name + "</li>");

							} else {
								valid_files_ul.append("<li class='list-group-item'>" + input.files[i].name + "</li>");
								ary_img_description[i] = {"label" : "", "content" : "" };
								
								// update the flag
								has_images_to_upload = true;
							}
						}

						//
						if (valid_files_ul.children().length <= 0) {
							valid_files_ul.append("<li class='list-group-item'>No Files Selected</li>");
						}
						if (invalid_files_ul.children().length <= 0) {
							invalid_files_ul.append("<li class='list-group-item'>No Invalid Files</li>");
						}

						//
						if (toolarge !== "") {
							alert("These images were not uploaded due to size limit of 1MB\n"
									+ toolarge);
						}
					});

	$('#btn_upload').click(function() {
		var input = document.getElementById("images_for_upload");
		var maxsize = 1024000;
		var requests = [];
		var upload_block = $('#processing_cover');

		if (input.files.length <= 0 && has_images_to_upload) {
			alert('No data for upload');
		} else {
			// popup cover
			upload_block.css({
				'display' : 'block'
			});
			for ( var i = 0; i < input.files.length; i++) {
				if (input.files[i].size < maxsize) {
					var filedata = new FormData();
					filedata.append("image_for_upload", input.files[i]);

					//
					requests.push($.ajax({
									url : upload_url,
									data : filedata,
									cache : false,
									contentType : false,
									processData : false,
									type : 'POST',
									success : handle_successful_ajax,
									error : handle_failed_ajax
					}));
					
					// handle requests response
					$.when.apply(undefined, requests).done(function(results){
							console.log(JSON.stringify(results,2,2));
							// popup cover
							upload_block.css({
								'display' : 'none'
							});
							
							// update the flag
							has_images_to_upload = false;
							
							// update list
							valid_files_ul.empty();
							invalid_files_ul.empty();
						});
				}
			}
		}
	});
	
	function handle_successful_ajax(response){
		var data = JSON.parse(response);
		imagelinks = data['img_urls'];
		img_title = data['img_title'];
		img_description = data['img_description'];
		console.log(imagelinks);
		for ( var i = 0; i < imagelinks.length; i++) {
			$('#photo_table')
					.append(
							'<tr><td><img class="img-responsive" style="width: 400px;" src=' + imagelinks[i] + '> </td>' + '<td><h4>Image Title</h4><p style="font-size: 13px;">'+ img_title +'</p>' + '<h4>Image Description</h4><p style="font-size: 13px;">' + img_description + '</p>' +  '</td></tr>');
		}
	}
	
	function handle_failed_ajax(response){
		console.log(JSON.stringify(response,2,2));
	}
})();