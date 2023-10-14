import { findUser } from "$lib/database.js";
import { setCallUserId } from "$lib/kv.js";
import { fail, text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ url, setHeaders }) {
    const callId = url.searchParams.get("CallSid");
    const phone = url.searchParams.get("Caller");
    const speechResult = url.searchParams.get("SpeechResult");
    if (!callId || !phone || !speechResult) throw fail(400);

    const response = new twilio.twiml.VoiceResponse();

    response.say("you said");
    response.say(speechResult);

    const userId = await findUser(phone);
    if (userId) {
        setCallUserId(callId, userId);
        response.redirect({ method: "GET" }, "/api/twilio/ask");
    } else {
        response.say("You are wrong. Goodbye!");
    }

    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
