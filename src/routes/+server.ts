import { decrypt, encrypt, generateKeyPairs, verifyPrivateKey } from "$lib/crypto";
import { json } from "@sveltejs/kit";

export async function GET({ fetch }) {
    const { publicKey, privateKey } = await generateKeyPairs(fetch);

    const verifyGood = await verifyPrivateKey(fetch, privateKey, publicKey);

    const encrypted = await encrypt(fetch, publicKey, "PASSWORD1234");
    const decrypted = await decrypt(fetch, privateKey, publicKey, encrypted);

    return json({ verifyGood, encrypted, decrypted });
}
