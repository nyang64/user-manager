package com.elementscience.automation.API;

import org.json.JSONObject;

import com.elementscience.automation.Common.RestUtils;
import com.qmetry.qaf.automation.core.ConfigurationManager;
import com.qmetry.qaf.automation.core.MessageTypes;
import com.qmetry.qaf.automation.util.Reporter;

public class ElementScienceAPI extends RestUtils {
	
	public Object requestBodyForAuthentication(String username, String password, String apiEndPoint) {
		JSONObject requestBody = new JSONObject();
		switch (apiEndPoint) {
			case "es.login.authentication" :
				requestBody.put("username", username);
				requestBody.put("password", password);
				break;

			default :
				Reporter.log("Steps not yet coded for " + apiEndPoint);
				break;
		}
		return requestBody;
	}
	
	public void validateAuthorizationTokenCreation() {
		JSONObject response = null;
		response = new JSONObject(getResponse().getMessageBody());
		if(response.has("message")) {
			Reporter.log("User authentication failed with response: " + response.get("message"), MessageTypes.Info);
		} else {
			ConfigurationManager.getBundle().setProperty("es.authorization.id", response.get("id_token"));
		}
	}
	
	public void validateResponseHasReportURL() {
		JSONObject response = null;
		response = new JSONObject(getResponse().getMessageBody());
		if(response.has("report_url")) {
			Reporter.log("Patient Report URL: " + response.get("report_url"), MessageTypes.Pass);
		} else {
			Reporter.log("Patient Report URL not received: " + response, MessageTypes.Fail);
		}
	}
}
