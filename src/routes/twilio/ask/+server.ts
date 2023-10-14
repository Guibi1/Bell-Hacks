import { text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ setHeaders }) {
    const response = new twilio.twiml.VoiceResponse();

    response.gather({
        input: ["speech"],
        action: "/api/twilio/answer",
        method: "GET",
    });

    response.say("We didn't receive any input. Goodbye!");
    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
