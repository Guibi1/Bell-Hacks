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

    response.say("You didn't say anything. Thank you for calling, goodbye!");
    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
