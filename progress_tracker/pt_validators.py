# it turns out validators is a python package on PYPI
# so this file is now being called as pt_validators.py
# pt stands for progress_tracker, the app which this 
# file/module is a part of
import json

# isnumeric does not work on floats
def is_int_or_float(string):
	try:
		x = float(string)
		return x
	except:
		return False

def trend_validator(trend_dict):
	trend_ignore_keys = ["csrfmiddlewaretoken"]
	trend_guranteed_keys = ["trend_name", "xaxis_field", "yaxis_title", "xaxis_title"]
	# Status codes: (-1: errors or warnings or both, 0: all ok, 1: Fatal error)
	resultant = {
		"progressibility.trend_validator.status_code": -1,
		"progressibility.trend_validator.error": "",
		"progressibility.trend_validator.warn": "",
	}

	keys_to_plot = []

	# checking if the keys added by the django forms exist or not (these keys
	# are in trend_guranteed_keys). It is possible that these fields were
	# somehow removed. For eg. (via developers tab, extrernal software, etc.)

	for guranteed_key in trend_guranteed_keys:
		if guranteed_key not in list(trend_dict.keys()):
			resultant["progressibility.trend_validator.error"] += f"'{guranteed_key}' does not exist; "
			resultant["progressibility.trend_validator.status_code"] = 1
			return resultant
		else:
			# guranteed key exists
			if guranteed_key == "trend_name":
				resultant["progressibility.title"] = trend_dict[guranteed_key][0]
				# remove it from trend_dict so that we don't loop over it will
				# handling the data to be plotted
				trend_ignore_keys.append(guranteed_key)
				continue

			if guranteed_key == "yaxis_title":
				resultant["progressibility.yaxis.title"] = trend_dict[guranteed_key][0]
				trend_ignore_keys.append(guranteed_key)
				continue

			if guranteed_key == "xaxis_title":
				resultant["progressibility.xaxis.title"] = trend_dict[guranteed_key][0]
				trend_ignore_keys.append(guranteed_key)
				continue

			if guranteed_key == "xaxis_field":
				if trend_dict[guranteed_key][0] not in list(trend_dict.keys()):
					# The specified X-axis field does not exist.
					# While this is worthy of an error,
					# it may not be valid grounds for termination of the function.
					# So, we issue a warning and ignore the specified X-Axis field
					# for now I'm assuming that plotly.js will automatically take care
					# of xaxis if we have not specified it.
					resultant["progressibility.trend_validator.error"] += f"xaxis_field specified does not exist; "
					resultant["progressibility.trend_validator.warn"] += f"xaxis_field specified does not exist; "
					continue
				resultant["progressibility.xaxis_field"] = trend_dict[guranteed_key][0]
				continue


	# extract the fields to be plotted, if the key "plot_fieldName" exists then,
	# fieldName will be plotted. Data corresponding to fieldName will be used for
	# plotting.

	for key in trend_dict:
		# ignore the keys if they are of no use to us
		if key in trend_ignore_keys:
			continue

		if key.startswith("plot_"):
			# TO-DO: Handle case in which pointed_key doesn't exist in trend_dict
			pointed_key = key[5:]
			######## to avoid reading plotting data as a description ########
			trend_ignore_keys.append(pointed_key)
			print(f"Pointed key: {pointed_key}")

			if pointed_key in list(resultant.keys()):
				resultant.pop(pointed_key)
			######## end ########

			data_to_plot_raw = trend_dict[pointed_key]

			# will be used for plotting if detected_category is labels
			raw_data_tokens = data_to_plot_raw[0].split(",")
			detected_category = None

			# will be used for plotting if detected_category is numerical
			data_to_plot = []

			for token in raw_data_tokens:
				convertedFloat = is_int_or_float(token)
				if convertedFloat:
					detected_category = "numerical"
					data_to_plot.append(convertedFloat)
				else:
					detected_category = "labels"

			# First we check whether the current field's data belongs to X-axis or 
			# Y-axis then map the data to the corresponding key.

			if detected_category == "numerical":
				if pointed_key != trend_dict["xaxis_field"][0]:
					resultant[f"progressibility.trends.{pointed_key}"] = data_to_plot
					# trend_dict.pop(pointed_key)
					continue
				else:
					resultant[f"progressibility.xaxis"] = data_to_plot
					# trend_dict.pop(pointed_key)
					continue
			else:
				# detected_category is labels
				if pointed_key != trend_dict["xaxis_field"][0]:
					resultant[f"progressibility.trends.{pointed_key}"] = raw_data_tokens
					# trend_dict.pop(pointed_key)
					continue
				else:
					resultant[f"progressibility.xaxis"] = raw_data_tokens
					# trend_dict.pop(pointed_key)
					continue

		else:
			if key != "xaxis_field":
				resultant[key] = trend_dict[key][0]
				continue

	# check if there are any errors or warnings
	if (len(resultant["progressibility.trend_validator.error"])) == 0 and (len(resultant["progressibility.trend_validator.warn"]) == 0):
		resultant["progressibility.trend_validator.status_code"] = 0
		return resultant

	return resultant

	# for key in trend_dict:
	# 	# ignore the keys if they are of no use to us
	# 	if key in trend_ignore_keys:
	# 		continue

	# 	# we determine if the value is numerical data (30,80,78.5) or text (for description)
	# 	# or comma separated labels (eg. Mon,Tue,Wed)

	# 	value = trend_dict[key]
	# 	value_tokens = value.split(",")
	# 	detected_category = None

	# 	for token in value_tokens:
	# 		if is_int_or_float(token):
	# 			detected_category = "numerical"
	# 		else:
	# 			detected_category = "text or labels"

	# 	if detected_category == "numerical":
	# 		if key != trend_dict["xaxis_field"]:
	# 			resultant[f"progressibility.trends.{key}"] = json.loads("["+value+"]")
	# 			continue
	# 		else:
	# 			resultant["progressibility.xaxis"] = json.loads("["+value+"]")
	# 			continue

	# 	# find a way to differentiate between text and labels
	# 	else:
	# 		pass