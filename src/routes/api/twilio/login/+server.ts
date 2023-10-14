import { fail, text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ url, setHeaders }) {
    const caller = url.searchParams.get("Caller");
    const speechResult = url.searchParams.get("SpeechResult");
    if (!caller || !speechResult) throw fail(400);

    const response = new twilio.twiml.VoiceResponse();

    response.say("you said");
    response.say(speechResult);

    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
