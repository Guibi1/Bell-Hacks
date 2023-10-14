import { fail, text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ url, setHeaders }) {
    const speechResult = url.searchParams.get("SpeechResult");
    if (!speechResult) throw fail(400);

    const response = new twilio.twiml.VoiceResponse();

    response.say("you said");
    response.say(speechResult);

    response.redirect({ method: "GET" }, "/api/twilio/ask");

    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
