import { text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ setHeaders }) {
    const response = new twilio.twiml.VoiceResponse();

    const gather = response.gather({
        input: ["speech"],
        action: "/api/twilio/awnser",
        method: "GET",
    });
    gather.say("Ask what you want to do.");

    response.say("We didn't receive any input. Goodbye!");
    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
