# DATA LAB FUNCTIONS ELEMENT
A Data Lab Functions project is a multi-user project that is typically set up to handle Data Lab endpoints. [For more on Data Lab Functions](https://support.seeq.com/kb/latest/cloud/data-lab-functions-vs-data-lab-projects)

A Seeq Data Lab Functions endpoint has the following structure:
```
https://<my-seeq-server>/data-lab/<project-id>/functions/notebooks/<notebook_name>/endpoints/<endpoint_path>?<query_string>
```
For more on Data Lab Functions endpoints, see the [Invoking A Data Lab Functions REST API Endpoint](https://support.seeq.com/kb/latest/cloud/invoking-a-data-lab-functions-rest-api-endpoint) documentation.

This example contains the following endpoints:

- `GET /hello` - Returns a simple JSON response with a single message.
- `GET /version` - Returns a simple JSON response with the Seeq server version.
- `GET /view-payload` - Returns the request body as a JSON response.
- `POST /combine` - Gets the signals `idA` and `idB` from the request body and the math operator `op`. Then it creates a Seeq formula and pushes the formula to Seeq. Finally, it updates the display pane to show the mathematical result of the math operation that acted on the two signals.
