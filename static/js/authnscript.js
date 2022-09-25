const { startRegistration, startAuthentication } = SimpleWebAuthnBrowser;

// Registration
const statusRegister = document.getElementById("statusRegister");
const dbgRegister = document.getElementById("dbgRegister");

// Authentication
const statusAuthenticate = document.getElementById("statusAuthenticate");
const dbgAuthenticate = document.getElementById("dbgAuthenticate");


/**
 * Helper methods
 */

function printToDebug(elemDebug, title, output) {
  if (elemDebug.innerHTML !== "") {
    elemDebug.innerHTML += "\n";
  }
  elemDebug.innerHTML += `// ${title}\n`;
  elemDebug.innerHTML += `${output}\n`;
}

function resetDebug(elemDebug) {
  elemDebug.innerHTML = "";
}

function printToStatus(elemStatus, output) {
  elemStatus.innerHTML = output;
}

function resetStatus(elemStatus) {
  elemStatus.innerHTML = "";
}

function getPassStatus() {
  return "✅";
}

function getFailureStatus(message) {
  return `🛑 (Reason: ${message})`;
}

/**
 * Register Button
 */
document
  .getElementById("btnBegin")
  .addEventListener("click", async () => {

    // Get options
		console.log("getting options (sripts.js)")
    const resp = await fetch("/generate-registration-options");
	  console.log("RESP response: ",resp);
    const opts = await resp.json();
		console.log("recieved registration response (scripts.js)");

    // Start WebAuthn Registration
    let regResp;
    try {
	  console.log("awaitingting startRegistration (scripts.js)");
      regResp = await startRegistration(opts);
	  console.log("recieved startRegistration(opts) (scripts.js)");
      
    } catch (error) {
				// Some basic error handling
				if (error.name === 'InvalidStateError') {
					elemError.innerText = 'Error: Authenticator was probably already registered by user';
				} else {
					elemError.innerText = error;
				}
		
				throw error;
			}

    // Send response to server
    const verificationResp = await fetch(
      "/api/verify-registration-response/'",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(regResp),
      }
    );

    // Report validation response
    const verificationRespJSON = await verificationResp.json();
    const { verified, msg } = verificationRespJSON;
	
    if (verified) {
      console.log("registration verified");
    } else {
      console.log("registration not verified");
    }
    
	// send data to python server
	$.ajax({
		url:"/registration",
		type:"POST",
		contentType: "application/json",
		data: JSON.stringify(verificationRespJSON)});
	// if verificationRespJSON property value == true => redirect to logged in screen
	  // else registration verification not valid
	if (verified == true){
		window.location = "/welcome";
	} else{
		console.log("Something went wrong");
	}
  });


/**
 * Authenticate Button
 */
document
  .getElementById("btnBeginAuth")
  .addEventListener("click", async () => {
    $.ajax({
			url:"/api/authentication/login",
			type:"POST",
			contentType: "application/json",
			data: JSON.stringify({"post_data":loginValue})
		});

    // Get options
    const resp = await fetch("/api/generate-authentication-options/");
    const opts = await resp.json();

    // Start WebAuthn Authentication
    let authResp;
    try {
			// begin bug
			/* bug - incredibly long wait on random devices */
			console.log("Starting Authentication")
			const opts = await authResp.json();
			console.log(opts); // DEBUG: make sure things look okay
			asseResp = await startAuthentication(opts);
		  console.log("finished Authentication")
			console.log(authResp);
    } catch (err) {
      console.log("error");
      throw new Error(err);
    }

	  // debugging
		console.log("fetching verification response");
    // Send response to server
    const verificationResp = await fetch(
      "/api/verify-authentication/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(authResp),
      }
    );
	  // debugging
		console.log("retrieved verification response")
	  // debugging
		console.log("checking verification response")
    // Report validation response
    const verificationRespJSON = await verificationResp.json();
    const { verified, msg } = verificationRespJSON;
    if (verified) {
      console.log("authentication verified");
    } else {
      console.log("authentication not verified");
    }

	  // debugging
		console.log("checked verification response")
	  // debugging
		console.log("ajax POST request")
	// send data to python server
		$.ajax({
			url:"/auth",
			type:"POST",
			contentType: "application/json",
			data: JSON.stringify(verificationRespJSON)});
		// if verificationRespJSON property value == true => redirect to logged in screen
		// else verification not valid
		if (verified == true){
			window.location = "/welcome_back";
		} else{
			console.log("Something went wrong");
		}
  });