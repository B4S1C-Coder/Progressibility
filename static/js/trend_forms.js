var existingFields = ["trend_name"];
var isFieldNameInputWindowVisible = false;

function addFieldAsP(formID,
	placeholderText="Data (enter numerical data as 42,53,69)",
	determineFieldName=true,
	fieldName="default",
	setFieldValue=false,
	fieldValue="default",
	checkTheCheckbox=false,
	enableAlerts=true) {

	if (fieldName === "") {
		console.log("rejecting possible invalid function call");
		return -1;
	}

	// take the entered field name
	if (determineFieldName) {
		fieldName = document.getElementById("field-name-input-text").value;
	}
	placeholderText = fieldName;

	// once the value is taken, clear the field-name-input
	if (determineFieldName) {
		document.getElementById("field-name-input-text").value = "";
	}

	if (existingFields.includes(fieldName, 0)) {
		// this field already exists
		if (enableAlerts === true) {
			console.log(`raising alert for '${fieldName}`);
			alert(`The field ${fieldName} already exists. Can't add it again.`);
		}
		return -1;
	}

	var form = document.getElementById(formID);
	var pTag = document.createElement("p");
	var labelTag = document.createElement("div");
	var inputTag = document.createElement("input");
	var plotCheckboxInput = document.createElement("input");
	var removeLink = document.createElement("a");
	var removeIcon = document.createElement("img");

	removeIcon.className = "subtract-icon";
	removeIcon.src = "/static/img/subtract-icon-13.png";

	removeLink.href = "#";
	removeLink.title = "Remove this field.";
	// removeLink.onclick = function() { removeFieldAsP(fieldName); };
	removeLink.setAttribute("onclick", "removeFieldAsP('"+fieldName+"');");

	inputTag.type = "text";
	inputTag.name = fieldName;
	inputTag.className = "form-input";
	inputTag.placeholder = placeholderText;
	inputTag.id = `id_${fieldName}`;
	inputTag.title = fieldName;
	inputTag.required = true;
	inputTag.setAttribute('autocomplete', 'off');

	if (setFieldValue === true) {
		inputTag.setAttribute('value', fieldValue);
	}

	plotCheckboxInput.type = "checkbox";
	plotCheckboxInput.id = `plot_${fieldName}`;
	plotCheckboxInput.name = `plot_${fieldName}`;
	plotCheckboxInput.title = `Check to treat ${fieldName} as data for plotting.`;

	if (checkTheCheckbox === true) {
		plotCheckboxInput.checked = true;
		plotCheckboxInput.setAttribute("checked", "checked");
	}

	labelTag.className = "label-text";

	removeLink.appendChild(removeIcon);

	pTag.className = "parent-ptag";

	labelTag.innerHTML += `${fieldName}:`;
	pTag.appendChild(labelTag);

	pTag.appendChild(inputTag);
	pTag.appendChild(plotCheckboxInput);

	pTag.innerHTML += "Plot";

	pTag.appendChild(removeLink);
	form.appendChild(pTag);

	if (fieldName !== "") {
		existingFields.push(fieldName);
	}
}

function removeFieldAsP(fieldName) {
	// if the field doesn't exist, do nothing
	if (existingFields.includes(fieldName, 0) == false) {return -1;}

	var inputTag = document.getElementById(`id_${fieldName}`);
	var parentPTag = inputTag.parentNode;

	parentPTag.remove();

	const fieldNameIndex = existingFields.indexOf(fieldName);
	// 1 is the number of elements to delete
	if (fieldNameIndex > -1) {existingFields.splice(fieldNameIndex, 1);}
}

function toggleFieldNameInputWindow() {
	if (isFieldNameInputWindowVisible) {
		document.getElementById('panel-container').style.display = "none";
		isFieldNameInputWindowVisible = false;
	} else {
		document.getElementById('panel-container').style.display = "block";
		isFieldNameInputWindowVisible = true;
	}
}