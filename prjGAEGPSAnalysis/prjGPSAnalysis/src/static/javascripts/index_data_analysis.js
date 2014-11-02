(function(){
	/* JQuery */
	$('#images_for_upload')
			.change(
					function() {

						var input = document.getElementById("images_for_upload");
						var ul = document.getElementById("files_list");
						var toolarge = "";
						var maxsize = 1024000;
						while (ul.hasChildNodes()) {
							ul.removeChild(ul.firstChild);
						}
						for ( var i = 0; i < input.files.length; i++) {

							if (input.files[i].size > maxsize) {
								toolarge += input.files[i].name + "\n";
							} else {
								var li = document.createElement("li");
								li.innerHTML = input.files[i].name;
								ul.appendChild(li);
							}

						}
						if (!ul.hasChildNodes()) {
							var li = document.createElement("li");
							li.innerHTML = 'No Files Selected';
							ul.appendChild(li);
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

		if (input.files.length <= 0) {
			alert('No data for upload');
		} else {
			for ( var i = 0; i < input.files.length; i++) {

				if (input.files[i].size < maxsize) {
					var data = new FormData();
					data.append("image_for_upload", input.files[i]);
					//
					send_imgs(data);
				}
			}
		}
	});

	function send_imgs(filedata) {
		$.ajax({
			url : upload_url,
			data : filedata,
			cache : false,
			contentType : false,
			processData : false,
			type : 'POST',
			success : function(receiveddata) {
				var data = JSON.parse(receiveddata);
				imagelinks = data['img_urls'];
				console.log(imagelinks);
				for ( var i = 0; i < imagelinks.length; i++) {
					$('#photo_table').append(
							'<tr><td><img src='+imagelinks[i]+'></td></tr>');
				}
			}
		});

	}
})();