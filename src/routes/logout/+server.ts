import { json } from "@sveltejs/kit";

export async function POST({ cookies }) {
    cookies.delete("userId");
    cookies.delete("privateKey");
    return json({ success: true });
}
