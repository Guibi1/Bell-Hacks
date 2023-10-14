import { findUser } from "$lib/database.js";
import { setCallUserId } from "$lib/kv.js";
import { fail, text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ locals, url, setHeaders }) {
    const phone = url.searchParams.get("Caller");
    const speechResult = url.searchParams.get("SpeechResult");
    if (!locals.callId || !phone || !speechResult) throw fail(400);

    const response = new twilio.twiml.VoiceResponse();

    const userId = await findUser(phone);
    if (userId) {
        setCallUserId(locals.callId, userId);
        response.say("Hi, what do you want to do today?");
        response.redirect({ method: "GET" }, "/api/twilio/ask");
    } else {
        response.say("You are wrong. Goodbye!");
    }

    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
