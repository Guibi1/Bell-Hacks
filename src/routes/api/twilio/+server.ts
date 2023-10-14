import { text } from "@sveltejs/kit";
import { twiml } from "twilio";

export async function POST() {
    const twilio = new twiml.VoiceResponse();

    twilio.say("Niggawatt. Niggawatt. Niggawatt. Niggawatt.");

    return text(twilio.toString());
}
