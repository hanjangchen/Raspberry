(function() {
	/* JQuery */
	$('#images_for_upload')
			.change(
					function() {
						//
						var input = document.getElementById("images_for_upload");
						var valid_files_ul = $("#valid_files_list");
						var invalid_files_ul = $("#invalid_files_list");
						
						console.log(valid_files_ul);
						var toolarge = "";
						var maxsize = 1024000;

						//
						if (valid_files_ul.children().length > 0) {
							valid_files_ul.remove();
						}
						if (invalid_files_ul.children().length > 0) {
							invalid_files_ul.remove();
						}

						//
						for ( var i = 0; i < input.files.length; i++) {
							if (input.files[i].size > maxsize) {
								toolarge += input.files[i].name + "\n";
								invalid_files_ul.append("<li class='list-group-item'>" + input.files[i].name + "</li>");

							} else {
								valid_files_ul.append("<li class='list-group-item'>" + input.files[i].name + "</li>");
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

		if (input.files.length <= 0) {
			alert('No data for upload');
		} else {
			// popup cover
			$('#processing_cover').css({
				'display' : 'block'
			});
			for ( var i = 0; i < input.files.length; i++) {
				if (input.files[i].size < maxsize) {
					var filedata = new FormData();
					filedata.append("image_for_upload", input.files[i]);
					//
					// send_imgs(data);

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
							$('#processing_cover').css({
								'display' : 'none'
							});
							
							//
							$('#valid_files_list').remove();
							
							$('#invalid_files_list').remove();
						});
				}
			}
		}
	});
	
	function handle_successful_ajax(response){
		var data = JSON.parse(response);
		imagelinks = data['img_urls'];
		console.log(imagelinks);
		for ( var i = 0; i < imagelinks.length; i++) {
			$('#photo_table')
					.append(
							'<tr><td><img class="img-responsive" style="width: 300px;" src=' + imagelinks[i]
									+ '></td></tr>');
		}
	}
	
	function handle_failed_ajax(response){
		console.log(JSON.stringify(response,2,2));
	}

})();