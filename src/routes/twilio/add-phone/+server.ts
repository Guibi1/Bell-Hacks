import { addPhoneNumber } from "$lib/database.js";
import { fail, text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ locals, url, setHeaders }) {
    const phone = url.searchParams.get("Caller");
    const digits = url.searchParams.get("Digits");
    if (!locals.callId || !phone || !digits) throw fail(400);

    const response = new twilio.twiml.VoiceResponse();

    addPhoneNumber(digits, phone);

    response.say(
        "This phone has been successfully enrolled with your account. You will now be redirected to the login menu."
    );

    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
