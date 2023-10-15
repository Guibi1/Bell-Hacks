import { text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ setHeaders }) {
    const response = new twilio.twiml.VoiceResponse();

    response.gather({
        input: ["speech"],
        action: "/twilio/answer",
        method: "GET",
        speechModel: "experimental_conversations",
        speechTimeout: "auto",
    });

    response.say("We didn't receive any input. Goodbye!");
    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
