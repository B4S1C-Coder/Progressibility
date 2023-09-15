// this is trend.trends
const trendData = JSON.parse(document.getElementById("trend-data").textContent);
var xAxisPlotData;

for (var key in trendData) {
	const keyTokens = key.split(".");

	// if a key doesn't begin with "progressibility." it's a text field.
	if (keyTokens[0] !== "progressibility") {
		// create a normal field
		addFieldAsP('main-form-content', undefined, determineFieldName=false,
			fieldName=keyTokens[0], setFieldValue=true, fieldValue=trendData[key],
			enableAlerts=false);
		continue;
	} else {
		// keyTokens[0] is progressibility, we now need to determine the type of key
		if (keyTokens[1] === "title") {
			let trendNameInputTag = document.getElementById("id_trend_name");
			trendNameInputTag.value = trendData[key];
			continue;

		} if (keyTokens[1] === "yaxis") {
			// as of now its guranteed that there will be a third token, if the second
			// token is "yaxis"
			if (keyTokens[2] === "title") {
				let yaxisTitleInputTag = document.getElementById("id_yaxis_title");
				yaxisTitleInputTag.value = trendData[key];
				continue;
			}
			// other checks for yaxis if needed in future ...

		} if (keyTokens[1] === "xaxis") {
			// we would need an additional check, to check the length of
			// keyTokens as "progressibility.xaxis" is also a valid key
			if (keyTokens.length > 2) {
				// for now the only key that staisfies this check is 
				// "progressibility.xaxis.title"
				if (keyTokens[2] === "title") {
					var xaxisTitleInputTag = document.getElementById("id_xaxis_title");
					// xaxisTitleInputTag.value = trendData[key];
					xaxisTitleInputTag.setAttribute('value', trendData[key]);
					continue;
				}
				// other checks for long xaxis keys
			}
			// since length is less than or equal to 2, this means (atleast as of writing),
			// that the key is "progressibility.xaxis". This key maps to the data that has
			// to be plotted on xaxis
			xAxisPlotData = trendData[key].join();

			let xaxisFieldInputTag = document.getElementById("id_xaxis_field");
			xaxisFieldInputTag.setAttribute("value", trendData["progressibility.xaxis_field"]);

			addFieldAsP('main-form-content', undefined, determineFieldName=false,
				fieldName=trendData["progressibility.xaxis_field"], setFieldValue=true,
				fieldValue=xAxisPlotData, checkTheCheckbox=true,
				enableAlerts=false);

			continue;
		} if (keyTokens[1] === "trends") {
			// its guranteed that the key will be of the form "progressibility.trends.something"
			// create the field and populate it with the data of the field

			let textData = trendData[key].join();

			addFieldAsP('main-form-content', undefined, determineFieldName=false,
				fieldName=keyTokens[2], setFieldValue=true,
				fieldValue=textData, checkTheCheckbox=true,
				enableAlerts=false);

			if (textData === xAxisPlotData) {
				// we have found the x axis field name!
				let xaxisFieldInputTag = document.getElementById("id_xaxis_field");
				// xaxisFieldInputTag.value = keyTokens[2];
				xaxisFieldInputTag.setAttribute('value', trendData["progressibility.xaxis_field"]);
			}
			continue;
		}
	}
}
