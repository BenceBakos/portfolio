const main = document.getElementsByTagName('main')[0];

function contentItem(fName, text, path) {
	let wrapper = document.createElement('section');
	wrapper.innerHTML = `
		<details>
			<summary></summary>
			<div class="editor">
				<textarea>
				</textarea>
			</div>
			<button>Save</button>
		</details>
	`;

	//append to body
	main.appendChild(wrapper);

	let fileName = wrapper.getElementsByTagName('summary')[0];

	let textarea = wrapper.getElementsByTagName('textarea')[0];

	let saveButton = wrapper.getElementsByTagName('button')[0];

	fileName.innerHTML = fName;
	textarea.innerHTML = text;
	
	saveButton.addEventListener('click',function () {
		request({
			url: '/admin/update',
			method: 'post',
			headers: {
				"content-type": "application/json"
			},
			body: JSON.stringify({
				path: path,
				text: textarea.value
			})
		}).catch(err => alert(err));
	});

}

function request(obj) {
	return new Promise((resolve, reject) => {
		let xhr = new XMLHttpRequest();
		xhr.open(obj.method || "GET", obj.url);
		if (obj.headers) {
			Object.keys(obj.headers).forEach(key => {
				xhr.setRequestHeader(key, obj.headers[key]);
			});
		}
		xhr.onload = () => {
			if (xhr.status >= 200 && xhr.status < 300) {
				resolve(xhr.response);
			} else {
				reject(xhr.statusText);
			}
		};
		xhr.onerror = () => reject(xhr.statusText);
		xhr.send(obj.body);
	});
}

document.addEventListener('DOMContentLoaded', function () {
	//get contents list in JSON format
	fetch('/admin/contents')
	.then(function (response) {
		return response.json();
	})
	.then(function (jsonRes) {
		//loads jsonRes?

		//build editor's dom && bind click event on save button
		Object.keys(jsonRes).forEach(function (key) {
			let path = key,
			content = jsonRes[key];

			contentItem(content.fileName, content.text, path);
		});
	});
}, false);
