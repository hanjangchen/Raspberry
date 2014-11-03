(function() {
	/* JQuery */
	$('#images_for_upload')
			.change(
					function() {

						//
						var input = document
								.getElementById("images_for_upload");
						var valid_files_ul = document
								.getElementById("valid_files_list");
						var invalid_files_ul = document
								.getElementById("invalid_files_list");

						var toolarge = "";
						var maxsize = 1024000;

						var valid_files_list = [];

						//
						while (valid_files_ul.hasChildNodes()) {
							valid_files_ul
									.removeChild(valid_files_ul.firstChild);
						}
						while (invalid_files_ul.hasChildNodes()) {
							invalid_files_ul
									.removeChild(invalid_files_ul.firstChild);
						}

						//
						for ( var i = 0; i < input.files.length; i++) {
							if (input.files[i].size > maxsize) {
								toolarge += input.files[i].name + "\n";
								var li = document.createElement("li");
								li.innerHTML = input.files[i].name;
								invalid_files_ul.appendChild(li);

							} else {
								var li = document.createElement("li");
								li.innerHTML = input.files[i].name;
								valid_files_ul.appendChild(li);
								valid_files_list.push(input.files[i]);
							}
						}

						//
						if (!valid_files_ul.hasChildNodes()) {
							var li = document.createElement("li");
							li.innerHTML = 'No Files Selected';
							valid_files_ul.appendChild(li);
						}
						if (!invalid_files_ul.hasChildNodes()) {
							var li = document.createElement("li");
							li.innerHTML = 'No Invalid Files';
							invalid_files_ul.appendChild(li);
						}

						//
						if (toolarge != "") {
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