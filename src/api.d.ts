/**
 * This file is generated by sveltekit-api-fetch.
 * Do not edit it, as it will be overwritten.
 * Learn more here: https://github.com/Guibi1/sveltekit-api-fetch
 */

type ProjectAPI = {
    GET: {
        "/": never;
        "/twilio": never;
        "/twilio/add-phone": never;
        "/twilio/answer": never;
        "/twilio/ask": never;
        "/twilio/login": never;
        "/twilio/register": never;
        "/twilio/status": never;
    };
    POST: {
        "/login": { body: { phone: string; privateKey: string[] } };
    };
};
