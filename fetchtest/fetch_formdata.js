var formData = new FormData();
// Fields in the post
formData.append("id", "newid");

// pictureSource is object containing image data.

pictureSource = {
	uri: 'file:///C:/users/bhbh1/desktop/slifit_logo.png',
	type: 'file',
	name: 'slifit_logo',
}

if (pictureSource) {
  var photo = {
    uri: pictureSource.uri,
    type: pictureSource.type,
    name: pictureSource.fileName,
  };
  
  formData.append('file', photo);
}

fetch( 'http://172.93.51.135/' + 'upload/' + 'ppjnew/', {
  method: 'POST',
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'multipart/form-data',
  },
  mode: 'no-cors',
  body: formData
 })
.then((response) => response.json())
.then((responseJson) => {
  // Perform success response.
  console.log(responseJson);
 })
.catch((error) => {
    console.log(error)
});