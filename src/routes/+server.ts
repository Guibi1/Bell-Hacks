import { askGPT } from "$lib/gpt";
import { json } from "@sveltejs/kit";

export async function GET() {
    const res = await askGPT(
        { id: "n89g3cqs86q2g622bx508ajd", publicKey: "" },
        "get me my google password"
    );
    return json(res);
}
