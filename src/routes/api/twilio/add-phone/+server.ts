import { fail, text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ locals, url, setHeaders }) {
    const phone = url.searchParams.get("Caller");
    const digits = url.searchParams.get("Digits");
    if (!locals.callId || !phone || !digits) throw fail(400);

    const response = new twilio.twiml.VoiceResponse();

    // TODO

    response.say("F U C K you");

    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
