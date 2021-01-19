package com.elementscience.API.steps;

import static com.qmetry.qaf.automation.core.ConfigurationManager.getBundle;

import com.elementscience.automation.API.ElementScienceAPI;
import com.elementscience.automation.Common.RestUtils;
import com.qmetry.qaf.automation.step.QAFTestStep;

public class ElementScienceAPIStepsLibrary extends RestUtils{
	
	ElementScienceAPI esAPI = new ElementScienceAPI();
	
	@QAFTestStep(description = "user sets the url for {0}")
	public void userSetsTheUrlEndpoint(String endpointURL) {
		setBaseURL((String)getBundle().getPropertyValue(endpointURL));
	}
	
	@QAFTestStep(description = "user posts {0} username and {1} password for {2} API")
	public void postRequestForAuthentication(String username, String password, String apiEndPoint) {
		Object payload = esAPI.requestBodyForAuthentication(username, password, apiEndPoint);
		post(payload, getBaseURL());
	}	
	
	@QAFTestStep(description = "user checks the response status code as {0} and status phrase as {1}")
	public void validateStatusCodeAndPhrase(String code, String phrase) {
		checkStatusInfo(code, phrase);
	}
	
	@QAFTestStep(description = "user validates that authorization token is created")
	public void validateAuthorizationTokenCreation() {
		esAPI.validateAuthorizationTokenCreation();
	}
	
	@QAFTestStep(description = "user gets patient details for {0} ID")
	public void getPatientDetailsFromID(String id) {
		String resourcePath = getBaseURL() + id;
		get(resourcePath);
	}
	
	@QAFTestStep(description = "user gets patient report for {0} ID")
	public void getPatientReportFromID(String id) {
		String resourcePath = getBaseURL() + id;
		get(resourcePath);
	}
	
	@QAFTestStep(description = "user verifies that response contains report URL")
	public void validateResponseHasReportURL() {
		esAPI.validateResponseHasReportURL();
	}
}
