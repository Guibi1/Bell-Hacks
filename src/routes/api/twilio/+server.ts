import { text } from "@sveltejs/kit";
import { twiml } from "twilio";

export async function GET({ setHeaders }) {
    const response = new twiml.VoiceResponse();

    const gather = response.gather({
        input: ["speech"],
        action: "/api/twilio/login",
        method: "GET",
    });
    gather.say("Welcome to Phone Base! Please tell us your 4 words sercret passkey to continue.");

    response.say("We didn't receive any input. Goodbye!");
    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
