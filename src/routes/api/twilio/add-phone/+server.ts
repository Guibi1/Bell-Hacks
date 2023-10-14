import { fail, text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ url, setHeaders }) {
    const callId = url.searchParams.get("CallSid");
    const phone = url.searchParams.get("Caller");
    const digits = url.searchParams.get("Digits");
    if (!callId || !phone || !digits) throw fail(400);

    const response = new twilio.twiml.VoiceResponse();

    // TODO

    response.say("F U C K you");

    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
