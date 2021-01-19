package com.elementscience.automation.Common;
import static com.qmetry.qaf.automation.core.ConfigurationManager.getBundle;

import javax.ws.rs.core.MediaType;

import org.hamcrest.Matchers;
import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONTokener;

import com.qmetry.qaf.automation.core.MessageTypes;
import com.qmetry.qaf.automation.util.Reporter;
import com.qmetry.qaf.automation.util.Validator;
import com.qmetry.qaf.automation.ws.rest.RestTestBase;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.WebResource;

public class RestUtils extends RestTestBase{
	
	public static ClientResponse response = null;
	public static RestTestBase base;
	private static String BASE_URL = "api.env.baseurl";
	private static MediaType mediaType = MediaType.APPLICATION_JSON_TYPE;
	private static String AUTHORIZATION_VALUE = "";
	
	/**
	 * Get base test instance.
	 *
	 * @return Rest base test instance.
	 */
	public static RestTestBase getBase() {
		if (base == null) {
			base = new RestUtils();
		}
		return base;
	}
	
	public static void setBaseURL(String baseURL) {
		BASE_URL = baseURL;
	}
	
	public static String getBaseURL() {
		return BASE_URL;
	}

	/**
	 * Performs POST REST call to desired service.
	 *
	 * @param payload
	 *            Desired POST payload.
	 * @param resourcePath
	 *            Desired resource path.
	 */
	public static void post(Object payload, String resourcePath) {
		String dataTosend = payload.toString();
		Reporter.log("Method: POST", MessageTypes.Info);
		Reporter.log("Endpoint: " + resourcePath);
		Reporter.log(new JSONObject(dataTosend).toString(5), MessageTypes.Info);
		
		response = (getRequestBuilder(resourcePath, mediaType)).header("Authorization", AUTHORIZATION_VALUE).post(ClientResponse.class, dataTosend);	
		
		getResponseBodyInPrettyFormat(response);

	}
	
	/**
	 * Performs POST REST call to desired service.
	 *
	 * @param payload
	 *            Desired POST payload.
	 * @param resourcePath
	 *            Desired resource path.
	 */
	public static void get(String resourcePath) {
		Reporter.log("Method: GET", MessageTypes.Info);
		Reporter.log("Endpoint: " + resourcePath);
		
		response = (getRequestBuilder(resourcePath, mediaType)).header("Authorization", getBundle().getObject("es.authorization.id")).get(ClientResponse.class);	
		
		getResponseBodyInPrettyFormat(response);

	}
	
	/**
	 * Creates request builder for desired media type.
	 *
	 * @param url
	 *            Base url.
	 * @param mediaTypes
	 *            Desired media types.
	 * @return Request builder.
	 */
	public static WebResource.Builder getRequestBuilder(String url,
			MediaType... mediaTypes) {
		WebResource webResource = getResource(url);
		if (mediaTypes == null || mediaTypes.length <= 0)
			return webResource.type(MediaType.APPLICATION_JSON);
		else {
			return webResource.type(mediaTypes[0]);
		}
	}
	
	/**
	 * Creates request builder for sending REST calls.
	 *
	 * @param url
	 *            Base url.
	 * @return Request builder.
	 */
	private static WebResource getResource(String url) {
		WebResource webResource = getBase().getClient().resource(url);
		return webResource;
	}
	
	/**
	 * Logs response data to report.
	 */
	public static void getResponseBodyInPrettyFormat(ClientResponse response) {
		getBundle().setProperty("response", response);// Saving the response for
														// future
														// use
		Reporter.log("Response Code: " + response.getStatus(), MessageTypes.Info);
		
		if (getBase().getResponse().getMessageBody() != null) {
			String responseBody = getBase().getResponse().getMessageBody();
			Object json = new JSONTokener(getBase().getResponse().getMessageBody()).nextValue();
			if (json instanceof JSONObject) {
				// If the Response is JSON Object
				Reporter.log("Response is JSON Object", MessageTypes.Info);
				try {
					Reporter.log(
							"Response : " + new JSONObject(responseBody).toString(4), MessageTypes.Info);
				} catch (Exception e) {
					e.printStackTrace();
				}

			} else if (json instanceof JSONArray) {
				// If the Response is JSON array of Object
				Reporter.log("Response is JSON array of Object", MessageTypes.Info);
				try {
					Reporter.log("Response:" + new JSONArray(responseBody).toString(4), MessageTypes.Info);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		}
	}
	
	public static void checkStatusInfo(String code, String phrase) {
		Reporter.log("Response Code: " + response.getStatusInfo().getStatusCode(), MessageTypes.Info);
		if (Integer.parseInt(code) == response.getStatusInfo().getStatusCode()) {
			Reporter.log("Response code matching", MessageTypes.Pass);
			Validator.verifyThat(response.getStatusInfo().getStatusCode(),
					Matchers.comparesEqualTo(Integer.parseInt(code)));
		} else {
			Validator.verifyThat(response.getStatusInfo().getStatusCode(),
					Matchers.comparesEqualTo(Integer.parseInt(code)));
		}
		
		Reporter.log("Response Code Phrase: " + response.getStatusInfo().getReasonPhrase(), MessageTypes.Info);
		if (phrase.equalsIgnoreCase(response.getStatusInfo().getReasonPhrase())) {
			Reporter.log("Response code matching", MessageTypes.Pass);
			Validator.verifyThat(response.getStatusInfo().getReasonPhrase(),
					Matchers.equalToIgnoringCase(phrase));
		} else {
			Validator.verifyThat(response.getStatusInfo().getReasonPhrase(),
					Matchers.equalToIgnoringCase(phrase));
		}
	}
		
}
